import boto3

cloudwatch_client = boto3.client('cloudwatch')
sns_client = boto3.client('sns')


def lambda_handler(event, context):
    alarms = cloudwatch_alarms_describe()
    for alarm in alarms:
        alarm_name = alarm['AlarmName']
        cloudwatch_alarm_state_set(alarm_name)


def cloudwatch_alarms_describe():
    alarms = []
    response = cloudwatch_client.describe_alarms(StateValue='ALARM')
    alarms += response['MetricAlarms']
    while 'NextToken' in response:
        response = cloudwatch_client.describe_alarms(NextToken=response['NextToken'])
        alarms += response['MetricAlarms']
    return alarms


def cloudwatch_alarm_state_set(alarmname):
    cloudwatch_client.set_alarm_state(
        AlarmName=alarmname,
        StateValue='INSUFFICIENT_DATA',
        StateReason='Reset alarm status'
    )


# lambda_handler(1, 1)
