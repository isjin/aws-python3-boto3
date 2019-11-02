import boto3
import json


def lambda_handler(event, context):
    app = MetricEC2()
    app.main()


class MetricEC2(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.ec2_client = boto3.client('ec2')
        self.metric_data_template = 'metric/metric_template.txt'
        self.metric_count_template = 'metric/metric_put_count.txt'
        self.metric_data = []

    def set_metric_data(self, file_path, metricname, dimension_value, value_value):
        metric_data = self.read_file(file_path)
        metric_data['MetricName'] = metricname
        metric_data['Dimensions'][0]['Value'] = dimension_value
        metric_data['Value'] = value_value
        self.metric_data.append(metric_data)

    def cloudwatch_metric_data_put(self, metric_data_info):
        self.cloudwatch_client.put_metric_data(
            Namespace=metric_data_info['Namespace'],
            MetricData=metric_data_info['MetricData']
        )

    def ec2_instances_describe(self):
        response = self.ec2_client.describe_instances(
        )
        return response['Reservations']

    def ec2_instance_describe(self, instanceid):
        response = self.ec2_client.describe_instances(
            InstanceIds=[
                instanceid,
            ],
        )
        return response['Reservations']

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def main(self):
        metric_data_put = self.read_file(self.metric_data_template)
        metric_data_put['Namespace'] = 'EC2'
        ec2_instances_info = self.ec2_instances_describe()
        ec2_instances_other = ['i-03e49820693fec5dc', 'i-0a21499fb0912a33e']
        for instanceid in ec2_instances_other:
            try:
                instance_info = self.ec2_instance_describe(instanceid)
                ec2_instances_info = ec2_instances_info+instance_info
            except Exception as e:
                print(e.__str__())
        ec2_instance_count = len(ec2_instances_info)
        ec2_instance_running_count = 0
        ec2_instance_stopped_count = 0

        for ec2_instance_info in ec2_instances_info:
            status = ec2_instance_info['Instances'][0]['State']['Name']
            if status == "running":
                ec2_instance_running_count += 1
            elif status == "stopped":
                ec2_instance_stopped_count += 1
        self.set_metric_data(self.metric_count_template, 'EC2InstanceCount', 'EC2Instance', ec2_instance_count)
        self.set_metric_data(self.metric_count_template, 'EC2InstanceRunningCount', 'EC2InstanceRunning', ec2_instance_running_count)
        self.set_metric_data(self.metric_count_template, 'EC2InstanceStoppedCount', 'EC2InstanceStopped', ec2_instance_stopped_count)
        for metric_data in self.metric_data:
            metric_data_put['MetricData'] = [metric_data]
            self.cloudwatch_metric_data_put(metric_data_put)


if __name__ == '__main__':
    app = MetricEC2()
    app.main()
