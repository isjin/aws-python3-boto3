import boto3


class AWSEvent(object):
    def __init__(self):
        self.event_client = boto3.client('events')

    def event_rule_put(self, rule_name, schedule_rule):
        response = self.event_client.put_rule(
            Name=rule_name,
            ScheduleExpression=schedule_rule,
            # ScheduleExpression='string',#"cron(0 20 * * ? *)" or "rate(5 minutes)"
            # EventPattern='string',
            # State='ENABLED' | 'DISABLED',
            Description=rule_name,
            # RoleArn='string',
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ],
            # EventBusName='string'
        )
        print(response)
        return response['RuleArn']

    def event_rule_describe(self, rule_name):
        response = self.event_client.describe_rule(
            Name=rule_name,
            # EventBusName='string'
        )
        print(response)

    def event_rules_list(self):
        response = self.event_client.list_rules(
            # NamePrefix='string',
            # EventBusName='string',
            # NextToken='string',
            # Limit=123
        )
        # print(response)
        return response['Rules']

    def event_targets_by_rule_list(self, rule_name):
        response = self.event_client.list_targets_by_rule(
            Rule=rule_name,
            # EventBusName='string',
            # NextToken='string',
            # Limit=123
        )
        # print(response)
        return response['Targets']

    def event_target_put(self, target_info):
        # target_info={
        #     'Rule':'test',
        #     'Targets':[
        #         {
        #             'Id': 'test',
        #             'Arn': 'arn:aws-cn:lambda:cn-northwest-1:646976741397:function:clean_cloudwatch_log_groups',
        #         },
        #     ]
        # }
        response = self.event_client.put_targets(
            Rule=target_info['Rule'],
            # EventBusName='string',
            Targets=target_info['Targets'],
            # Targets=[
            #     {
            #         'Id': '555555312',
            #         'Arn': function_arn,
            #         # 'Arn': 'string',
            #         # 'RoleArn': 'string',
            #         # 'Input': 'string',
            #         # 'InputPath': 'string',
            #         # 'InputTransformer': {
            #         #     'InputPathsMap': {
            #         #         'string': 'string'
            #         #     },
            #         #     'InputTemplate': 'string'
            #         # },
            #         # 'KinesisParameters': {
            #         #     'PartitionKeyPath': 'string'
            #         # },
            #         # 'RunCommandParameters': {
            #         #     'RunCommandTargets': [
            #         #         {
            #         #             'Key': 'string',
            #         #             'Values': [
            #         #                 'string',
            #         #             ]
            #         #         },
            #         #     ]
            #         # },
            #         # 'EcsParameters': {
            #         #     'TaskDefinitionArn': 'string',
            #         #     'TaskCount': 123,
            #         #     'LaunchType': 'EC2' | 'FARGATE',
            #         #     'NetworkConfiguration': {
            #         #         'awsvpcConfiguration': {
            #         #             'Subnets': [
            #         #                 'string',
            #         #             ],
            #         #             'SecurityGroups': [
            #         #                 'string',
            #         #             ],
            #         #             'AssignPublicIp': 'ENABLED' | 'DISABLED'
            #         #         }
            #         #     },
            #         #     'PlatformVersion': 'string',
            #         #     'Group': 'string'
            #         # },
            #         # 'BatchParameters': {
            #         #     'JobDefinition': 'string',
            #         #     'JobName': 'string',
            #         #     'ArrayProperties': {
            #         #         'Size': 123
            #         #     },
            #         #     'RetryStrategy': {
            #         #         'Attempts': 123
            #         #     }
            #         # },
            #         # 'SqsParameters': {
            #         #     'MessageGroupId': 'string'
            #         # }
            #     },
            # ]
        )
        print(response)
        return response


if __name__ == '__main__':
    app = AWSEvent()
    # app.event_rule_put('test', 'rate(24 hours)')
    # app.event_rule_describe('set_cloudwatch_status')
    # app.event_targets_by_rule_list('test')
    # app.event_target_put('target_info')
    app.event_rules_list()
