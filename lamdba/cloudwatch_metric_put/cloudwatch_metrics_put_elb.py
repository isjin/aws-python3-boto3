import boto3
import json


def lambda_handler(event, context):
    app = MetricRDS()
    app.main()


class MetricRDS(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.elbv2_client = boto3.client('elbv2')
        self.metric_data_template = 'metric/metric_template.txt'
        self.metric_count_template = 'metric/metric_put_count.txt'
        self.metric_data = []

    def set_metric_data(self, file_path, MetricName, dimension_value, value_value):
        metric_data = self.read_file(file_path)
        metric_data['MetricName'] = MetricName
        metric_data['Dimensions'][0]['Value'] = dimension_value
        metric_data['Value'] = value_value
        self.metric_data.append(metric_data)

    def cloudwatch_metric_data_put(self, metric_data_info):
        self.cloudwatch_client.put_metric_data(
            Namespace=metric_data_info['Namespace'],
            MetricData=metric_data_info['MetricData']
        )

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def elb_load_balancers_describe(self):
        response = self.elbv2_client.describe_load_balancers(
        )
        return response['LoadBalancers']

    def elb_target_groups_describe(self):
        response = self.elbv2_client.describe_target_groups(
        )
        return response['TargetGroups']

    def elbv2_target_healthy_describe(self, target_group_arn):
        response = self.elbv2_client.describe_target_health(
            TargetGroupArn=target_group_arn,
        )
        return response['TargetHealthDescriptions']

    def main(self):
        metric_data_put = self.read_file(self.metric_data_template)
        metric_data_put['Namespace'] = 'ELB'
        elbs_info = self.elb_load_balancers_describe()
        elb_tgs_info = self.elb_target_groups_describe()
        active_tg_count = 0
        inactive_tg_count = 0
        healthy_tg_count = 0
        unhealthy_tg_count = 0
        elb_count = len(elbs_info)
        tg_count = len(elb_tgs_info)
        for elb_tg_info in elb_tgs_info:
            associated_elb_info = elb_tg_info['LoadBalancerArns']
            tg_arn = elb_tg_info['TargetGroupArn']
            tg_healthy_infos = self.elbv2_target_healthy_describe(tg_arn)
            if len(tg_healthy_infos) > 0:
                health_count = 0
                for tg_healthy_info in tg_healthy_infos:
                    healthy_value = tg_healthy_info['TargetHealth']['State']
                    if healthy_value == 'healthy':
                        health_count += 1
                if health_count > 0:
                    healthy_tg_count += 1
                else:
                    unhealthy_tg_count += 1
            if len(associated_elb_info) == 0:
                inactive_tg_count += 1
            else:
                active_tg_count += 1
        self.set_metric_data(self.metric_count_template, 'ELBCount', 'ELB', elb_count)
        self.set_metric_data(self.metric_count_template, 'ELBTargetGroupCount', 'ELBTargetGroup', tg_count)
        self.set_metric_data(self.metric_count_template, 'ELBInactiveTargetGroupCount', 'ELBInactiveTargetGroup', inactive_tg_count)
        self.set_metric_data(self.metric_count_template, 'ELBActiveTargetGroupCount', 'ELBActiveTargetGroup', active_tg_count)
        self.set_metric_data(self.metric_count_template, 'ELBHealthyTargetGroupCount', 'ELBHealthyTargetGroup', healthy_tg_count)
        self.set_metric_data(self.metric_count_template, 'ELBUnhealthyTargetGroupCount', 'ELBUnhealthyTargetGroup', unhealthy_tg_count)
        for metric_data in self.metric_data:
            metric_data_put['MetricData'] = [metric_data]
            self.cloudwatch_metric_data_put(metric_data_put)


# lambda_handler(1, 1)
