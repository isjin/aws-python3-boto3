from function.aws_cloudwatch import AWSCloudWatch
from function.aws_sns import AWSSNS
import json

instance_ids = ['i-004a96c77deedf4da', 'i-0281ab6b8c52e8fd9']
ec2_metrics=['CPUUtilization', 'DiskReadBytes', 'DiskReadOps', 'DiskWriteBytes', 'DiskWriteOps', 'NetworkIn', 'NetworkOut', 'StatusCheckFailed_Instance']
ecs_clusters = ['ecs_test']


class CreateAlarms(object):
    def __init__(self):
        self.cloudwatch = AWSCloudWatch()
        self.sns = AWSSNS()
        self.topic_name = 'alarm_email2'
        self.endpoints = ['isjin1@163.com', 'isjin2@163.com']
        self.subscription_arns = []

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def create_topic(self):
        topic_arn = self.sns.sns_topic_create(self.topic_name)
        return topic_arn

    def create_subscriptions(self, topic_arn):
        for endpoint in self.endpoints:
            subscription_arn = self.sns.sns_subscription_create(topic_arn, 'email', endpoint)
            self.subscription_arns.append(subscription_arn)

    def create_alarms(self, topic_arn):
        for instance_id in instance_ids:
            alarm_info = self.read_file('config/test/cloudwatch/alarm_ec2_cpu.txt')
            for metric in ec2_metrics:
                alarm_name = instance_id + '_'+metric
                alarm_info['AlarmName'] = alarm_name
                alarm_info['MetricName'] = metric
                alarm_info['AlarmActions'] = [self.topic_name]
                alarm_info['Dimensions'][0]['Value'] = instance_id
                alarm_info['AlarmActions'] = [topic_arn]
                self.cloudwatch.cloudwatch_alarm_create(alarm_info)

    def main(self):
        topic_arn = self.create_topic()
        self.create_subscriptions(topic_arn)
        self.create_alarms(topic_arn)


if __name__ == '__main__':
    app = CreateAlarms()
    app.main()
