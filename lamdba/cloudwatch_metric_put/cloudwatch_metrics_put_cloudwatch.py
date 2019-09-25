import boto3
import json


def lambda_handler(event, context):
    app = MetricCLoudWatch()
    app.main()


class MetricCLoudWatch(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')
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

    def cloudwatch_alarms_describe(self):
        alarms = []
        response = self.cloudwatch_client.describe_alarms()
        alarms += response['MetricAlarms']
        while 'NextToken' in response:
            response = self.cloudwatch_client.describe_alarms(NextToken=response['NextToken'])
            alarms += response['MetricAlarms']
        return alarms

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def main(self):
        metric_data_put = self.read_file(self.metric_data_template)
        metric_data_put['Namespace'] = 'CloudWatch'
        alarms = self.cloudwatch_alarms_describe()
        alarms_count = len(alarms)
        alarms_alarm_count = 0
        alarms_ok_count = 0
        alarms_insufficient_count = 0
        for alarm in alarms:
            state_value = alarm['StateValue']
            if state_value == 'OK':
                alarms_ok_count += 1
            elif state_value == 'ALARM':
                alarms_alarm_count += 1
            else:
                alarms_insufficient_count += 1
        self.set_metric_data(self.metric_count_template, 'AlarmsTotalCount', 'AlarmsTotal', alarms_count)
        self.set_metric_data(self.metric_count_template, 'AlarmsOKCount', 'AlarmsOK', alarms_ok_count)
        self.set_metric_data(self.metric_count_template, 'AlarmsAlarmCount', 'AlarmsAlarm', alarms_alarm_count)
        self.set_metric_data(self.metric_count_template, 'AlarmsInsufficentCount', 'AlarmsInsufficent', alarms_insufficient_count)
        metric_data_put['MetricData'] = self.metric_data
        self.cloudwatch_metric_data_put(metric_data_put)
