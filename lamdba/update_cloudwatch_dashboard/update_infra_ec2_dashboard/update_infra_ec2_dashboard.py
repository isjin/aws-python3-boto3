import boto3
import json


def lambda_handler(event, context):
    app = CreateCloudwatch()
    app.main()


class CreateCloudwatch(object):
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.dashboard_file = 'cloudwatch_dashboard.txt'
        self.ec2_metric_file = 'metric_ec2.txt'
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

    def genarate_service_metrics(self, service_metrics, view_type, instanceids):
        widgets = []
        for service_metric in service_metrics:
            metrics_list = []
            widget_title = service_metric + '-' + 'EC2'
            service_content = self.read_file(self.ec2_metric_file)
            serivce_metric = ['AWS/EC2', 'CPUUtilization', 'InstanceId', 'i-1234567']
            for instanceid in instanceids:
                metric = serivce_metric.copy()
                metric[1] = service_metric
                metric[3] = instanceid
                metrics_list.append(metric)
            service_content['properties']['metrics'] = metrics_list
            service_content['properties']['title'] = widget_title
            service_content['properties']['view'] = view_type
            widgets.append(service_content)
        return widgets

    def main(self):
        instanceids = self.get_instanceids()
        dashboard_info = self.read_file(self.dashboard_file)
        # print(dashboard_info)
        widgets = []
        metrics = ['CPUUtilization', 'DiskReadBytes', 'DiskReadOps', 'DiskWriteBytes', 'DiskWriteOps', 'NetworkIn', 'NetworkOut', 'NetworkPacketsIn', 'NetworkPacketsOut', 'StatusCheckFailed',
                   'StatusCheckFailed_Instance', 'StatusCheckFailed_System']
        ec2_widgets = self.genarate_service_metrics(metrics, 'timeSeries', instanceids)
        widgets = widgets + ec2_widgets
        dashboard_info['DashboardName'] = 'Sanofi_Infra_EC2'
        # dashboard_info['DashboardName']='test01'
        dashboard_info['DashboardBody']['widgets'] = widgets
        # print(dashboard_info)
        self.create_cloudwatch_dashboard(dashboard_info)

# if __name__ == '__main__':
#     app = CreateCloudwatch()
#     app.main()
