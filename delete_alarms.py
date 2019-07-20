from function.aws_cloudwatch import AWSCloudWatch


class DeleteAlarms(object):
    def __init__(self):
        self.cloudwatch = AWSCloudWatch()

    def main(self):
        alarms=self.cloudwatch.cloudwatch_alarms_describe()
        for alarm in alarms:
            # print(alarm)
            alarm_name=alarm['AlarmName']
            self.cloudwatch.cloudwatch_alarm_delete(alarm_name)



if __name__ == '__main__':
    app=DeleteAlarms()
    app.main()