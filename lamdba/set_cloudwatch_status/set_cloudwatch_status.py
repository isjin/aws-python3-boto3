import boto3


def lambda_handler(event, context):
    app = ResetCloudState()
    app.main()


class ResetCloudState(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.sns_client = boto3.client('sns')

    def cloudwatch_alarms_describe(self):
        alarms = []
        response = self.cloudwatch_client.describe_alarms(StateValue='ALARM')
        alarms += response['MetricAlarms']
        while 'NextToken' in response:
            response = self.cloudwatch_client.describe_alarms(NextToken=response['NextToken'])
            alarms += response['MetricAlarms']
        return alarms

    def cloudwatch_alarm_state_set(self, alarmname):
        self.cloudwatch_client.set_alarm_state(
            AlarmName=alarmname,
            StateValue='OK',
            StateReason='Reset alarm status'
        )

    def main(self):
        alarms = self.cloudwatch_alarms_describe()
        for alarm in alarms:
            alarm_name = alarm['AlarmName']
            self.cloudwatch_alarm_state_set(alarm_name)
