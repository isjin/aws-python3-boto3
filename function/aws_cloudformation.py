import boto3
import json


class AWSCloudFormation(object):
    def __init__(self):
        self.cloudformation_client = boto3.client('cloudformation')

    def cloudformation_stacks_describe(self):
        response = self.cloudformation_client.describe_stacks(
            # StackName=cloudformation_name,
            # NextToken='string'
        )
        # print(response)
        return response

    def cloudformation_stack_describe(self, cloudformation_name):
        response = self.cloudformation_client.describe_stacks(
            StackName=cloudformation_name,
            # NextToken='string'
        )
        # print(response)
        return response

    def cloudformation_stack_create(self,stack_info):
        # stack_info={
        #     'StackName':'devops-chain-demo01',
        #     'TemplateBody':'body',
        #     'TemplateURL':'url',
        #     'Parameters':[
        #         {
        #             'ParameterKey': 'string',
        #             'ParameterValue': 'string',
        #             'UsePreviousValue': True | False,
        #             'ResolvedValue': 'string'
        #         },
        #     ],
        #     'Tags': [
        #         {
        #             'Key': 'string',
        #             'Value': 'string'
        #         },
        #     ]
        # }
        response = self.cloudformation_client.create_stack(
            StackName=stack_info['StackName'],
            TemplateBody=stack_info['TemplateBody'],
            # TemplateURL=stack_info['TemplateURL'],
            Parameters=stack_info['Parameters'],
            # DisableRollback=False,
            # RollbackConfiguration={
            #     'RollbackTriggers': [
            #         {
            #             'Arn': 'string',
            #             'Type': 'string'
            #         },
            #     ],
            #     'MonitoringTimeInMinutes': 123
            # },
            # TimeoutInMinutes=123,
            # NotificationARNs=[
            #     'string',
            # ],
            # Capabilities=[
            #     'CAPABILITY_IAM' | 'CAPABILITY_NAMED_IAM' | 'CAPABILITY_AUTO_EXPAND',
            # ],
            # ResourceTypes=[
            #     'string',
            # ],
            # RoleARN='string',
            # OnFailure='DO_NOTHING' | 'ROLLBACK' | 'DELETE',
            # StackPolicyBody='string',
            # StackPolicyURL='string',
            Tags=stack_info['Tags'],
            # ClientRequestToken='string',
            EnableTerminationProtection=False
        )
        print(response)

    def cloudformation_stack_delete(self,stackname):
        response = self.cloudformation_client.delete_stack(
            StackName=stackname,
            # RetainResources=[
            #     'string',
            # ],
            # RoleARN='string',
            # ClientRequestToken='string'
        )
        print(response)


if __name__ == '__main__':
    app = AWSCloudFormation()
    app.cloudformation_stacks_describe()


