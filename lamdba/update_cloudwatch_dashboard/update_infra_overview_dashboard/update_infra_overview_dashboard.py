import boto3
import json


def lambda_handler(event, context):
    app = CreateCloudwatch()
    app.main()


class CreateCloudwatch(object):
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.dashboard_file = 'cloudwatch_dashboard_infra_overview.txt'
        self.ec2 = boto3.client('ec2')
        self.filter = []

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def ec2_instances_describe(self):
        response = self.ec2.describe_instances(
            Filters=self.filter,
        )
        return response['Reservations']

    def get_instanceids(self):
        instanceids = []
        instances_info = self.ec2_instances_describe()
        for instance_info in instances_info:
            instanceids.append(instance_info['Instances'][0]['InstanceId'])
        return instanceids

    def create_cloudwatch_dashboard(self, dashboard_info):
        response = self.cloudwatch.put_dashboard(
            DashboardName=dashboard_info['DashboardName'],
            DashboardBody=json.dumps(dashboard_info['DashboardBody'])
        )
        print(response)

    def main(self):
        instanceids = self.get_instanceids()
        dashboard_info = self.read_file(self.dashboard_file)
        print(dashboard_info)
        ec2_cpu_utilization_metrics_info = []
        metric = ["AWS/EC2", "CPUUtilization", "InstanceId", "i-0edd92757939e7bb8"]
        for instanceid in instanceids:
            metric2 = metric.copy()
            metric2[3] = instanceid
            ec2_cpu_utilization_metrics_info.append(metric2)
        dashboard_info['DashboardBody']['widgets'][7]['properties']['metrics'] = ec2_cpu_utilization_metrics_info
        # dashboard_info['DashboardName']='test01'
        self.create_cloudwatch_dashboard(dashboard_info)

# if __name__ == '__main__':
#     app = CreateCloudwatch()
#     app.main()
