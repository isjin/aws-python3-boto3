from function.aws_cloudwatch import AWSCloudWatch
from function.aws_elb import AWSELB
from function.aws_ecs import AWSECS
from configparser import ConfigParser
import json
import os

cf = ConfigParser()
cf.read('cloudwatch_dashboard.ini')


class CloudWatchMetrics(object):
    def __init__(self):
        self.cloudwatch = AWSCloudWatch()
        self.dashboard_list = cf.options('dashboard')
        self.resources = {}
        self.init_resources()
        self.elb = AWSELB()
        self.ecs = AWSECS()
        self.dashboard_content = self.read_file(cf.get('template', 'dashboard_template'))
        self.ec2_content = self.read_file(cf.get('template', 'ec2_template'))

    def init_resources(self):
        resource_path = cf.get('template', 'resource_path')
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    @staticmethod
    def write_file(path, data):
        f = open(path, 'w')
        f.write(json.dumps(data))
        f.close()

    def genarate_service_metrics(self, service_type, service_metrics, view_type, instances_list):
        widgets = []
        for service_metric in service_metrics:
            metrics_list = []
            service_metric2 = None
            service_content = None
            widget_title = service_metric + '-' + service_type
            if service_type == 'ECS_Cluster':
                service_content = self.read_file(cf.get('template', 'ecs_cluster_template'))
                service_metric2 = ['AWS/ECS', 'CPUUtilization', 'ClusterName', 'ecs-cluster']
            elif service_type == 'ECS_Service':
                service_content = self.read_file(cf.get('template', 'ecs_service_template'))
                service_metric2 = ['AWS/ECS', 'CPUUtilization', 'ServiceName', 'cloud-watch-log-service', 'ClusterName', 'ecs-cluster']
            elif service_type == "EC2":
                service_content = self.read_file(cf.get('template', 'ec2_template'))
                if service_metric == 'MemoryUtilization':
                    service_metric2 = ['System/Linux', 'MemoryUtilization', 'InstanceId', 'i-1234567']
                else:
                    service_metric2 = ['AWS/EC2', 'CPUUtilization', 'InstanceId', 'i-1234567']
            elif service_type == "RDS":
                service_content = self.read_file(cf.get('template', 'rds_template'))
                service_metric2 = ['AWS/RDS', 'CPUUtilization', 'DBInstanceIdentifier', 'dudu-nxprod-sql']
            elif service_type == "ElastiCache":
                service_content = self.read_file(cf.get('template', 'elasticache_template'))
                service_metric2 = ['AWS/ElastiCache', 'CPUUtilization', 'CacheClusterId', 'op-prd-redis-001']
            elif service_type == "ALB":
                service_content = self.read_file(cf.get('template', 'alb_template'))
                service_metric2 = ['AWS/ApplicationELB', 'ActiveConnectionCount', 'LoadBalancer', 'app/dudu-nxprod-api-alb/a39d5961edbce933']
            elif service_type == "ALB_TG":
                service_content = self.read_file(cf.get('template', 'alb_template'))
                service_metric2 = ['AWS/ApplicationELB', 'HealthyHostCount', 'TargetGroup', 'targetgroup/dudu-nxprod-api-tg/63fb802d0ba4bfdf', 'LoadBalancer',
                                  'app/dudu-nxprod-api-alb/a39d5961edbce933']
            for instance in instances_list:
                if service_type == 'ECS_Service':
                    ecs_services=[]
                    ecs_service_arns=self.ecs.ecs_services_list(instance)
                    for ecs_service_arn in ecs_service_arns:
                        ecs_service_name = str(ecs_service_arn).split('/')[1]
                        ecs_services.append(ecs_service_name)
                    for ecs_service in ecs_services:
                        metric = service_metric2.copy()
                        metric[1] = service_metric
                        metric[3] = ecs_service
                        metric[5] = instance
                        metrics_list.append(metric)
                else:
                    metric = service_metric2.copy()
                    if service_type == "ALB_TG":
                        alb_tg_info = self.elb.elbv2_target_group_describe(instance)
                        alb_arn = alb_tg_info['LoadBalancerArns'][0]
                        alb_instance = str(alb_arn).split('loadbalancer/')[1]
                        metric[5] = alb_instance
                        instance = str(instance).split(':')[-1]
                    elif service_type == "ECS_Service":
                        pass
                    metric[1] = service_metric
                    metric[3] = instance
                    metrics_list.append(metric)
            service_content['properties']['metrics'] = metrics_list
            service_content['properties']['title'] = widget_title
            service_content['properties']['view'] = view_type
            widgets.append(service_content)
        return widgets

    def get_instances_list(self, resource_key, instances_keys):
        instances = []
        if instances_keys[0] == 'all':
            for key in self.resources[resource_key].keys():
                instance = self.resources[resource_key][key]
                instance = self.__format_instance(resource_key, instance)
                instances.append(instance)
        else:
            for key in instances_keys:
                instance = self.resources[resource_key][key]
                instance = self.__format_instance(resource_key, instance)
                instances.append(instance)
        return instances

    @staticmethod
    def __format_instance(resource_key, instance):
        if resource_key == 'elbs':
            instance = str(instance).split('loadbalancer/')[1]
        # elif resource_key == 'elb_target_groups':
        #     instance = str(instance).split(':')[-1]
        return instance

    def main(self):
        for dashboard in self.dashboard_list:
            file_path = cf.get(dashboard, 'file_path')
            dashboard_name = cf.get(dashboard, 'dashboard_name')
            self.dashboard_content['DashboardName'] = dashboard_name
            widgets = []
            for option in cf.options(dashboard):
                def get_service_info():
                    service_info = str(cf.get(dashboard, option)).split(',')
                    service_metric_option = service_info[0]
                    metrics = str(cf.get('metrics', service_metric_option)).split(',')
                    viewtype = service_info[1]
                    resource_key = service_info[2]
                    instances_keys = service_info[3].split(';')
                    instances = self.get_instances_list(resource_key, instances_keys)
                    return metrics, viewtype, instances

                if option == 'ec2':
                    service_metrics, view_type, instances_list = get_service_info()
                    ec2_widgets = self.genarate_service_metrics('EC2', service_metrics, view_type, instances_list)
                    widgets = widgets + ec2_widgets
                elif option == 'ecs_cluster':
                    service_metrics, view_type, instances_list = get_service_info()
                    ecs_widgets = self.genarate_service_metrics('ECS_Cluster', service_metrics, view_type, instances_list)
                    widgets = widgets + ecs_widgets
                elif option == 'ecs_service':
                    service_metrics, view_type, instances_list = get_service_info()
                    ecs_widgets = self.genarate_service_metrics('ECS_Service', service_metrics, view_type, instances_list)
                    widgets = widgets + ecs_widgets
                elif option == 'rds':
                    service_metrics, view_type, instances_list = get_service_info()
                    rds_widgets = self.genarate_service_metrics('RDS', service_metrics, view_type, instances_list)
                    widgets = widgets + rds_widgets
                elif option == 'elasticache':
                    service_metrics, view_type, instances_list = get_service_info()
                    elasticache_widgets = self.genarate_service_metrics('ElastiCache', service_metrics, view_type, instances_list)
                    widgets = widgets + elasticache_widgets
                elif option == 'alb':
                    service_metrics, view_type, instances_list = get_service_info()
                    alb_widgets = self.genarate_service_metrics('ALB', service_metrics, view_type, instances_list)
                    widgets = widgets + alb_widgets
                elif option == 'alb_tg':
                    service_metrics, view_type, instances_list = get_service_info()
                    alb_tg_widgets = self.genarate_service_metrics('ALB_TG', service_metrics, view_type, instances_list)
                    widgets = widgets + alb_tg_widgets
            self.dashboard_content['DashboardBody']['widgets'] = widgets
            self.write_file(file_path, self.dashboard_content)
            f = open(file_path, 'w')
            f.write(json.dumps(self.dashboard_content))
            f.close()


if __name__ == '__main__':
    app = CloudWatchMetrics()
    app.main()
