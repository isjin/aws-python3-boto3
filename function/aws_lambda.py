import boto3


class AWSLambda(object):
    def __init__(self):
        self.lambda_client = boto3.client('lambda')

    def lambda_function_create(self, function_info):
        # with open('lambda_function.zip', 'rb') as f:
        #     zipped_code = f.read()
        # function_info={
        #     'FunctionName':'test',
        #     'Runtime':'python3.6',
        #     'Role':'arn:aws-cn:iam::1111111111:role/service-role/ec2_snapshot-role-ed4u0in8',
        #     'Handler':'lambda_function.lambda_handler',
        #     'ZipFile':{'ZipFile':zipped_code},
        # }
        response = self.lambda_client.create_function(
            FunctionName=function_info['FunctionName'],
            Runtime=function_info['Runtime'],
            Role=function_info['Role'],
            Handler=function_info['Handler'],
            Code=function_info['ZipFile'],
            # Code={
            # 'ZipFile': b'bytes',
            # 'S3Bucket': 'string',
            # 'S3Key': 'string',
            # 'S3ObjectVersion': 'string'
            # },
            # Description='string',
            Timeout=60,
            # MemorySize=123,
            # Publish=True | False,
            # VpcConfig={
            #     'SubnetIds': [
            #         'string',
            #     ],
            #     'SecurityGroupIds': [
            #         'string',
            #     ]
            # },
            # DeadLetterConfig={
            #     'TargetArn': 'string'
            # },
            # Environment={
            #     'Variables': {
            #         'string': 'string'
            #     }
            # },
            # KMSKeyArn='string',
            # TracingConfig={
            #     'Mode': 'Active' | 'PassThrough'
            # },
            # Tags={
            #     'string': 'string'
            # },
            # Layers=[
            #     'string',
            # ]
        )
        # print(response)
        return response

    def lambda_function_delete(self, function_name):
        response = self.lambda_client.delete_function(
            FunctionName=function_name,
        )
        print(response)

    def lambda_function_get(self, function_name):
        response = self.lambda_client.get_function(
            FunctionName=function_name,
            # Qualifier='string'
        )
        print(response)

    def lambda_functions_list(self):
        response = self.lambda_client.list_functions(
            # MasterRegion='string',
            # FunctionVersion='ALL',
            # Marker='string',
            # MaxItems=123
        )
        # print(response)
        return response['Functions']

    def lambda_permission_add(self,permission_info):
        # permission_info={
        #     'FunctionName':'clean_cloudwatch_log_groups',
        #     'StatementId':'test-Trigger-Event',
        #     'Principal':'events.amazonaws.com.cn',
        #     'SourceArn':'arn:aws-cn:events:cn-northwest-1:646976741397:rule/test',
        # }
        response = self.lambda_client.add_permission(
            FunctionName=permission_info['FunctionName'],
            StatementId=permission_info['StatementId'],
            Action='lambda:InvokeFunction',
            Principal=permission_info['Principal'],
            SourceArn=permission_info['SourceArn'],
            # SourceAccount='string',
            # EventSourceToken='string',
            # Qualifier='string',
            # RevisionId='string'
        )
        print(response)
        return response



if __name__ == '__main__':
    app = AWSLambda()
    # app.lambda_function_get('AMP_snapshot_create')
    # with open('lambda_function_snapshot_Brandgoods.zip', 'rb') as f:
    #     zipped_code = f.read()
    # function_info={
    #     'FunctionName':'Brandgoods_snapshot_create',
    #     'Runtime':'python3.6',
    #     'Role':'arn:aws-cn:iam::1111111111:role/service-role/ec2_snapshot-role-ed4u0in8',
    #     'Handler':'lambda_function_snapshot.lambda_handler',
    #     'ZipFile':{'ZipFile':zipped_code},
    # }
    # app.lambda_function_create(function_info)
    # app.lambda_function_get('confirm_subscriptions')
    app.lambda_permission_add()
