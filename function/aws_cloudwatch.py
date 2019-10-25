import boto3
import json


class AWSCloudWatch(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')

    def cloudwatch_metrics_list(self):
        response = self.cloudwatch_client.list_metrics(
            # Namespace='string',
            # MetricName='string',
            # Dimensions=[
            #     {
            #         'Name': 'string',
            #         'Value': 'string'
            #     },
            # ],
            # NextToken='string'
        )
        print(response)

    def cloudwatch_dashboard_create(self, dashboard_info):
        # dashboard_info={
        #     'DashboardName':'test2',
        #     'DashboardBody':{
        #         "widgets": [
        #
        #         ]
        #     }
        # }
        response = self.cloudwatch_client.put_dashboard(
            DashboardName=dashboard_info['DashboardName'],
            DashboardBody=json.dumps(dashboard_info['DashboardBody'])
        )
        print(response)

    def cloudwatch_dashboard_get(self, dashboard_name):
        response = self.cloudwatch_client.get_dashboard(
            DashboardName=dashboard_name
        )
        print(response)
        return response

    def cloudwatch_dashboards_list(self):
        response = self.cloudwatch_client.list_dashboards(
            # DashboardNamePrefix='string',
            # NextToken='string'
        )
        # print(response)
        return response['DashboardEntries']

    def cloudwatch_dashboard_delete(self, dashboard_name):
        response = self.cloudwatch_client.delete_dashboards(
            DashboardNames=[
                dashboard_name,
            ]
        )
        print(response)

    def cloudwatch_metric_list(self):
        response = self.cloudwatch_client.list_metrics(
            # Namespace='string',
            MetricName='CPUUtilization',
            # Dimensions=[
            #     {
            #         'Name': 'string',
            #         'Value': 'string'
            #     },
            # ],
            # NextToken='string'
        )
        print(response)

    def cloudwatch_alarms_describe(self):
        alarms = []
        response = self.cloudwatch_client.describe_alarms()
        alarms += response['MetricAlarms']
        while 'NextToken' in response:
            response = self.cloudwatch_client.describe_alarms(NextToken=response['NextToken'])
            alarms += response['MetricAlarms']
        return alarms

    def cloudwatch_alarm_describe(self, alarm_name):
        response = self.cloudwatch_client.describe_alarms(
            AlarmNames=[
                alarm_name,
            ],
            # AlarmNamePrefix='string',
            # StateValue='OK' | 'ALARM' | 'INSUFFICIENT_DATA',
            # ActionPrefix='string',
            # MaxRecords=123,
            # NextToken='string'
        )
        print(response)
        return response['MetricAlarms'][0]

    def cloudwatch_alarm_create(self, alarm_info):
        # alarm_info = {
        #     'AlarmName': 'test3',
        #     'AlarmActions': ['arn:aws-cn:sns:cn-northwest-1:952375741452:test'],
        #     'MetricName': 'CPUUtilization',
        #     'Namespace': 'AWS/ECS',
        #     'Statistic': 'Average',
        #     'Dimensions': [
        #         {
        #             'Name': 'ClusterName',
        #             'Value': 'ecs_test'
        #         },
        #     ],
        #     'Period': 300,
        #     'EvaluationPeriods': 1,
        #     'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
        #     'Threshold': 70,
        # }
        response = self.cloudwatch_client.put_metric_alarm(
            AlarmName=alarm_info['AlarmName'],
            # AlarmDescription='string',
            # ActionsEnabled=True | False,
            OKActions=alarm_info['OKActions'],
            AlarmActions=alarm_info['AlarmActions'],
            InsufficientDataActions=alarm_info['InsufficientDataActions'],
            MetricName=alarm_info['MetricName'],
            Namespace=alarm_info['Namespace'],
            # Statistic='SampleCount' | 'Average' | 'Sum' | 'Minimum' | 'Maximum',
            Statistic=alarm_info['Statistic'],
            # ExtendedStatistic='string',
            Dimensions=alarm_info['Dimensions'],
            Period=alarm_info['Period'],
            # Unit='Seconds' | 'Microseconds' | 'Milliseconds' | 'Bytes' | 'Kilobytes' | 'Megabytes' | 'Gigabytes' | 'Terabytes' | 'Bits' | 'Kilobits' | 'Megabits' | 'Gigabits' | 'Terabits' | 'Percent' | 'Count' | 'Bytes/Second' | 'Kilobytes/Second' | 'Megabytes/Second' | 'Gigabytes/Second' | 'Terabytes/Second' | 'Bits/Second' | 'Kilobits/Second' | 'Megabits/Second' | 'Gigabits/Second' | 'Terabits/Second' | 'Count/Second' | 'None',
            EvaluationPeriods=alarm_info['EvaluationPeriods'],
            # DatapointsToAlarm=123,
            Threshold=alarm_info['Threshold'],
            # ComparisonOperator='GreaterThanOrEqualToThreshold' | 'GreaterThanThreshold' | 'LessThanThreshold' | 'LessThanOrEqualToThreshold' | 'LessThanLowerOrGreaterThanUpperThreshold' | 'LessThanLowerThreshold' | 'GreaterThanUpperThreshold',
            ComparisonOperator=alarm_info['ComparisonOperator'],
            # TreatMissingData='string',
            # EvaluateLowSampleCountPercentile='string',
            # Metrics=[
            #     {
            #         'Id': alarm_info['Metrics']['Id'],
            #         'MetricStat': {
            #             'Metric': {
            #                 'Namespace': alarm_info['Metrics']['Namespace'],
            #                 'MetricName': alarm_info['Metrics']['MetricName'],
            #                 'Dimensions': [
            #                                 {
            #                                     'Name': 'string',
            #                                     'Value': 'string'
            #                                 },
            #                             ]
            #             },
            #             'Period': 123,
            #             'Stat': 'string',
            #             'Unit': 'Seconds' | 'Microseconds' | 'Milliseconds' | 'Bytes' | 'Kilobytes' | 'Megabytes' | 'Gigabytes' | 'Terabytes' | 'Bits' | 'Kilobits' | 'Megabits' | 'Gigabits' | 'Terabits' | 'Percent' | 'Count' | 'Bytes/Second' | 'Kilobytes/Second' | 'Megabytes/Second' | 'Gigabytes/Second' | 'Terabytes/Second' | 'Bits/Second' | 'Kilobits/Second' | 'Megabits/Second' | 'Gigabits/Second' | 'Terabits/Second' | 'Count/Second' | 'None'
            #         },
            #         'Expression': 'string',
            #         'Label': 'string',
            #         'ReturnData': True | False
            #     },
            # ],
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ],
            # ThresholdMetricId='string'
        )
        print(response)
        return response

    def cloudwatch_alarm_delete(self, alarmname):
        response = self.cloudwatch_client.delete_alarms(
            AlarmNames=[
                alarmname,
            ]
        )
        print(response)

    def cloudwatch_alarms_delete(self, alarmnames_list):
        response = self.cloudwatch_client.delete_alarms(
            AlarmNames=alarmnames_list
        )
        print(response)

    def cloudwatch_metric_data_put(self, metric_data_info):
        # metric_data_info={
        #     'Namespace':'Custom/S3',
        #     'MetricData':[
        #         {
        #             'MetricName':'BucketCount',
        #             'Dimensions': [
        #                 {
        #                     'Name': 'Count',
        #                     'Value': 'Bucket'
        #                 },
        #             ],
        #             'Value': 8,
        #             'Unit': 'Count',
        #         }
        #     ]
        # }
        response = self.cloudwatch_client.put_metric_data(
            Namespace=metric_data_info['Namespace'],
            MetricData=metric_data_info['MetricData']
            # MetricData=[
            #     {
            #         'MetricName': 'string',
            #         'Dimensions': [
            #             {
            #                 'Name': 'string',
            #                 'Value': 'string'
            #             },
            #         ],
            #         # 'Timestamp': datetime(2015, 1, 1),
            #         'Value': 123.0,
            #         # 'StatisticValues': {
            #         #     'SampleCount': 123.0,
            #         #     'Sum': 123.0,
            #         #     'Minimum': 123.0,
            #         #     'Maximum': 123.0
            #         # },
            #         # 'Values': [
            #         #     123.0,
            #         # ],
            #         # 'Counts': [
            #         #     123.0,
            #         # ],
            #         # 'Unit': 'Seconds' | 'Microseconds' | 'Milliseconds' | 'Bytes' | 'Kilobytes' | 'Megabytes' | 'Gigabytes' | 'Terabytes' | 'Bits' | 'Kilobits' | 'Megabits' | 'Gigabits' | 'Terabits' | 'Percent' | 'Count' | 'Bytes/Second' | 'Kilobytes/Second' | 'Megabytes/Second' | 'Gigabytes/Second' | 'Terabytes/Second' | 'Bits/Second' | 'Kilobits/Second' | 'Megabits/Second' | 'Gigabits/Second' | 'Terabits/Second' | 'Count/Second' | 'None',
            #         'Unit': 'Seconds' | 'Microseconds' | 'Milliseconds' | 'Bytes' | 'Kilobytes' | 'Megabytes' | 'Gigabytes' | 'Terabytes' | 'Bits' | 'Kilobits' | 'Megabits' | 'Gigabits' | 'Terabits' | 'Percent' | 'Count' | 'Bytes/Second' | 'Kilobytes/Second' | 'Megabytes/Second' | 'Gigabytes/Second' | 'Terabytes/Second' | 'Bits/Second' | 'Kilobits/Second' | 'Megabits/Second' | 'Gigabits/Second' | 'Terabits/Second' | 'Count/Second' | 'None',
            #         # 'StorageResolution': 123
            #     },
            # ]
        )
        print(response)

    def cloudwatch_alarm_action(self, alarm_name):
        response = self.cloudwatch_client.enable_alarm_actions(
            AlarmNames=[
                alarm_name,
            ]
        )
        print(response)

    def cloudwatch_alarm_state_set(self, alarm_name, state_value, state_reason):
        response = self.cloudwatch_client.set_alarm_state(
            AlarmName=alarm_name,
            # StateValue='OK' | 'ALARM' | 'INSUFFICIENT_DATA',
            StateValue=state_value,
            StateReason=state_reason,
            # StateReasonData='string'
        )
        print(response)


if __name__ == '__main__':
    app = AWSCloudWatch()
    # app.cloudwatch_metric_data_put()
    # app.cloudwatch_alarms_for_metric_describe()
    # app.cloudwatch_alarm_describe('test')
    # infos=app.cloudwatch_alarms_describe()
    # for info in infos:
    #     print(info['AlarmName'],info['MetricName'],info['ComparisonOperator'],info['Threshold'])
    info=app.cloudwatch_dashboard_get('Sanofi_Infra_ALB')
    print(info['DashboardBody'])
    # app.cloudwatch_alarm_state_set('rds_dudu-nxprod-sql_FreeableMemory', 'OK', 'resend')
