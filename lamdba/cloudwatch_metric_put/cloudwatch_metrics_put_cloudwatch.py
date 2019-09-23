import boto3
import json

cloudwatch_client = boto3.client('cloudwatch')
metric_data_template = 'metric/metric_template.txt'
metric_count_template = 'metric/metric_put_count.txt'
metric_data_put = None
metric_data = []


def lambda_handler(event, context):
    metric_data_put = read_file(metric_data_template)
    metric_data_put['Namespace'] = 'Custom/CloudWatch'
    alarms = cloudwatch_alarms_describe()
    alarms_count = len(alarms)
    alarms_alarm_count = 0
    alarms_ok_count = 0
    alarms_insufficient_count = 0
    for alarm in alarms:
        state_value = alarm['StateValue']
        if state_value == 'OK':
            alarms_ok_count += 1
        elif state_value == 'ALARM':
            alarms_insufficient_count += 1
        else:
            alarms_alarm_count += 1
    set_metric_data(metric_count_template, 'AlarmsTotalCount', 'AlarmsTotal', alarms_count)
    set_metric_data(metric_count_template, 'AlarmsOKCount', 'AlarmsOK', alarms_ok_count)
    set_metric_data(metric_count_template, 'AlarmsAlarmCount', 'AlarmsAlarm', alarms_alarm_count)
    set_metric_data(metric_count_template, 'AlarmsInsufficentCount', 'AlarmsInsufficent', alarms_insufficient_count)
    metric_data_put['MetricData'] = metric_data
    cloudwatch_metric_data_put(metric_data_put)


def set_metric_data(file_path, MetricName, dimension_value, value_value):
    metric_data1 = read_file(file_path)
    metric_data1['MetricName'] = MetricName
    metric_data1['Dimensions'][0]['Value'] = dimension_value
    metric_data1['Value'] = value_value
    metric_data.append(metric_data1)


def cloudwatch_metric_data_put(metric_data_info):
    cloudwatch_client.put_metric_data(
        Namespace=metric_data_info['Namespace'],
        MetricData=metric_data_info['MetricData']
    )


def cloudwatch_alarms_describe():
    alarms = []
    response = cloudwatch_client.describe_alarms()
    alarms += response['MetricAlarms']
    while 'NextToken' in response:
        response = cloudwatch_client.describe_alarms(NextToken=response['NextToken'])
        alarms += response['MetricAlarms']
    return alarms


def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)
    return data


# lambda_handler(1, 1)
