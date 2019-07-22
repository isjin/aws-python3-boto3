from function.aws_cloudwatch import AWSCloudWatch
from configparser import ConfigParser
import json
import os

cf=ConfigParser()
cf.read('build_resources_config.ini')
ecs_metrics = ['CPUReservation', 'CPUUtilization', 'MemoryReservation', 'MemoryUtilization']
ec2_metrics = ['CPUUtilization', 'DiskReadBytes', 'DiskReadOps', 'DiskWriteBytes', 'DiskWriteOps', 'NetworkIn', 'NetworkOut', 'StatusCheckFailed_Instance']


class GenerateMetrics(object):
    def __init__(self):
        self.cf=ConfigParser()
        self.cf.read('build_resources_config.ini')
        self.resources={}
        self.init_resources()
        self.cloudwatch = AWSCloudWatch()
        self.cloudwatch_path = self.cf.get('resource','cloudwatch')
        self.cloudwatch_data = self.read_file(self.cloudwatch_path)
        self.widgets = []
        self.instance_ids=[]
        self.ecs_clusters=[]

    def init_resources(self):
        resource_path =self.cf.get('resource','path')
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

    def get_compute_resources(self):
        instances_info=self.resources['ec2_instances']
        for key in instances_info.keys():
            self.instance_ids.append(instances_info[key])
        ecs_clusters_info=self.resources['ecs_clusters']
        for key in ecs_clusters_info.keys():
            self.ecs_clusters.append(ecs_clusters_info[key])


    def create_metrics(self, metric_file, service_metrics, service, metric_list, instances):
        for service_metric in service_metrics:
            title = service_metric + '_%s' % service
            data = self.read_file(metric_file)
            metrics = []
            for instance in instances:
                metric = metric_list.copy()
                metric[3]=instance
                metric[1]=service_metric
                metrics.append(metric)
            # print(metrics)
            data['properties']['metrics'] = metrics
            data['properties']['title'] = title
            self.widgets.append(data)

    def create_ecs_metric(self):
        metric_file = self.cf.get('resource','ecs_mertic')
        service_name = 'ECS'
        metric = ['AWS/ECS','CPUUtilization', 'ClusterName','ecs-cluster']
        self.create_metrics(metric_file, ecs_metrics, service_name, metric, self.ecs_clusters)

    def create_ec2_instance_metric(self):
        metric_file = self.cf.get('resource','ec2_mertic')
        service_name = 'EC2'
        metric = ['AWS/EC2', 'CPUUtilization','InstanceId','i-1234567']
        self.create_metrics(metric_file, ec2_metrics, service_name, metric, self.instance_ids)

    def main(self):
        self.get_compute_resources()
        self.create_ecs_metric()
        self.create_ec2_instance_metric()
        self.cloudwatch_data['DashboardBody']['widgets'] = self.widgets
        cloudwatch_save_file = self.cf.get('resource','cloudwatch_save')
        self.write_file(cloudwatch_save_file, self.cloudwatch_data)


if __name__ == '__main__':
    app = GenerateMetrics()
    app.main()
    # app.get_instance_ids()
