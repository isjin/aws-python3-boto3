import boto3
import json
import re
import os


def lambda_handler(event, context):
    app = CreateCloudwatch()
    app.main()


class CreateCloudwatch(object):
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.resource('s3')
        self.file_path = '/tmp/op_instanceids.txt'
        # self.file_path = 'op_instanceids.txt'
        self.s3_bucket = 'cloudwatchlog'
        self.s3_file_path = 'op_instanceids.txt'
        self.sns_topic = ['arn:aws-cn:sns:cn-northwest-1:646976741397:cloudwatch-email-alarm']
        self.filter = [
            {
                'Name': 'tag:System',
                'Values': [
                    'OP',
                ]
            },
            {
                'Name': 'instance-state-code',
                'Values': [
                    'running','pending'
                ]
            },
        ]

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
        print(response)
        return response['Reservations']

    def get_instanceids(self):
        instanceids = []
        instances_info = self.ec2_instances_describe()
        for instance_info in instances_info:
            instanceids.append(instance_info['Instances'][0]['InstanceId'])
        return instanceids

    def create_cloudwatch_alarm(self, alarm_path, instanceid):
        alarm_info = self.read_file(alarm_path)
        alarm_path_split = re.split(r'[_.]', str(alarm_path))
        metric = alarm_path_split[-2]
        alarm_info['AlarmActions'] = self.sns_topic
        alarm_info['OKActions'] = self.sns_topic
        alarm_info['InsufficientDataActions'] = self.sns_topic
        alarm_name = 'ec2' + '_' + instanceid + '_' + metric
        alarm_dimension = instanceid
        alarm_info['AlarmName'] = alarm_name
        # alarm_info['AlarmName'] = 'test'
        if metric == 'DiskSpaceUtilization':
            alarm_info['Dimensions'][1]['Value'] = alarm_dimension
        else:
            alarm_info['Dimensions'][0]['Value'] = alarm_dimension
        response = self.cloudwatch.put_metric_alarm(
            AlarmName=alarm_info['AlarmName'],
            OKActions=alarm_info['OKActions'],
            AlarmActions=alarm_info['AlarmActions'],
            InsufficientDataActions=alarm_info['InsufficientDataActions'],
            MetricName=alarm_info['MetricName'],
            Namespace=alarm_info['Namespace'],
            Statistic=alarm_info['Statistic'],
            Dimensions=alarm_info['Dimensions'],
            Period=alarm_info['Period'],
            EvaluationPeriods=alarm_info['EvaluationPeriods'],
            Threshold=alarm_info['Threshold'],
            ComparisonOperator=alarm_info['ComparisonOperator'],
        )
        print(response)

    def delete_cloudwatch_alarm(self, alarm_path, instanceid):
        alarm_path_split = re.split(r'[_.]', str(alarm_path))
        metric = alarm_path_split[-2]
        alarm_name = 'ec2' + '_' + instanceid + '_' + metric
        response = self.cloudwatch.delete_alarms(
            AlarmNames=[
                alarm_name,
            ]
        )
        print(response)

    def main(self):
        instanceids = self.get_instanceids()
        metric_files = os.listdir('template')
        # compare instanceid and delete old alarm
        self.s3.meta.client.download_file(self.s3_bucket, self.s3_file_path, self.file_path)
        f = open(self.file_path, 'r')
        data = f.readlines()
        f.close()
        old_instanceids = []
        for old_instanceid in data:
            old_instanceid = old_instanceid.replace('\n', '')
            old_instanceids.append(old_instanceid)
            if old_instanceid not in instanceids:
                for metric_file in metric_files:
                    file_path = os.path.join('template', metric_file)
                    self.delete_cloudwatch_alarm(file_path, old_instanceid)

        # upload instanceids to s3
        f = open(self.file_path, 'w')
        for instanceid in instanceids:
            f.write(instanceid + '\n')
        f.close()
        self.s3.meta.client.upload_file(self.file_path, self.s3_bucket, self.s3_file_path)

        # create alarm
        for instanceid in instanceids:
            if instanceid not in old_instanceids:
                for metric_file in metric_files:
                    file_path = os.path.join('template', metric_file)
                    self.create_cloudwatch_alarm(file_path, instanceid)

# if __name__ == '__main__':
#     app = CreateCloudwatch()
#     app.main()
