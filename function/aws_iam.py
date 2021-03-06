import boto3
import json


class AWSIAM(object):
    def __init__(self):
        self.iam_client = boto3.client('iam')

    def iam_user_create(self, username):
        response = self.iam_client.create_user(
            # Path='string',
            UserName=username,
            # PermissionsBoundary='string',
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ]
        )
        print(response)
        return response['User']['UserId']

    def iam_user_delete(self, username):
        response = self.iam_client.delete_user(
            UserName=username
        )
        print(response)

    def iam_user_get(self, username):
        response = self.iam_client.get_user(
            UserName=username
        )
        print(response)

    def iam_login_profile_create(self, username, password):
        response = self.iam_client.create_login_profile(
            UserName=username,
            Password=password,
            # PasswordResetRequired=True | False
            PasswordResetRequired=True | False
        )
        print(response)

    def iam_user_password_change(self, old_password, new_password):
        response = self.iam_client.change_password(
            OldPassword=old_password,
            NewPassword=new_password
        )
        print(response)

    def iam_user_policy_attach(self, username, policy_arn):
        response = self.iam_client.attach_user_policy(
            UserName=username,
            PolicyArn=policy_arn
        )
        print(response)

    def iam_user_policy_detach(self, username, policy_arn):
        response = self.iam_client.detach_user_policy(
            UserName=username,
            PolicyArn=policy_arn
        )
        print(response)

    def iam_role_create(self, role_info):
        # role_info = {
        #     "RoleName": "testrole",
        #     "Description": "testrole",
        #     "AssumeRolePolicyDocument": {
        #         'Version': '2008-10-17',
        #         'Statement': [
        #             {
        #                 'Sid': '',
        #                 'Effect': 'Allow',
        #                 'Principal': {
        #                     'Service': 'ec2.amazonaws.com.cn'
        #                 },
        #                 'Action': 'sts:AssumeRole'
        #             }
        #         ]
        #     }
        # }
        response = self.iam_client.create_role(
            # Path='string',
            RoleName=role_info['RoleName'],
            AssumeRolePolicyDocument=json.dumps(role_info['AssumeRolePolicyDocument']),
            Description=role_info['Description'],
            # MaxSessionDuration=123,
            # PermissionsBoundary='string',
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ]
        )
        print(response)
        return response['Role']

    def iam_role_delete(self, role_name):
        response = self.iam_client.delete_role(
            RoleName=role_name
        )
        print(response)

    def iam_role_get(self, role_name):
        response = self.iam_client.get_role(
            RoleName=role_name
        )
        print(response)

    def iam_instance_profile_create(self, intance_profile_name):
        response = self.iam_client.create_instance_profile(
            InstanceProfileName=intance_profile_name,
            # Path='string'
        )
        print(response)
        return response['InstanceProfile']['Arn']

    def iam_instance_profile_delete(self, intance_profile_name):
        response = self.iam_client.delete_instance_profile(
            InstanceProfileName=intance_profile_name,
            # Path='string'
        )
        print(response)

    def iam_instance_profile_get(self, intance_profile_name):
        response = self.iam_client.get_instance_profile(
            InstanceProfileName=intance_profile_name,
            # Path='string'
        )
        print(response)

    def iam_role_to_instance_profile_add(self, instance_profile_name, role_name):
        response = self.iam_client.add_role_to_instance_profile(
            InstanceProfileName=instance_profile_name,
            RoleName=role_name
        )
        print(response)

    def iam_role_to_instance_profile_remove(self, instance_profile_name, role_name):
        response = self.iam_client.remove_role_from_instance_profile(
            InstanceProfileName=instance_profile_name,
            RoleName=role_name
        )
        print(response)

    def iam_instance_profile_for_role_list(self, role_name):
        response = self.iam_client.list_instance_profiles_for_role(
            RoleName=role_name,
            # Marker='string',
            # MaxItems=123
        )
        print(response)

    def iam_role_policy_attach(self, role_name, policy_arn):
        response = self.iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(response)

    def iam_role_policy_detach(self, role_name, policy_arn):
        response = self.iam_client.detach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(response)

    def iam_role_policy_get(self, role_name, policy_name):
        response = self.iam_client.get_role_policy(
            RoleName=role_name,
            PolicyName=policy_name
        )
        print(response)

    def iam_policy_get(self, policy_arn):
        response = self.iam_client.get_policy(
            PolicyArn=policy_arn
        )
        print(response)

    def iam_policy_create(self, policy_info):
        # policy_info = {
        #     "PolicyName": "ecs_cloudwatch2",
        #     "PolicyDocument": {
        #         "Version": "2012-10-17",
        #         "Statement": [
        #             {
        #                 "Sid": "VisualEditor0",
        #                 "Effect": "Allow",
        #                 "Action": [
        #                     "logs:CreateLogStream",
        #                     "logs:DescribeLogStreams",
        #                     "logs:PutLogEvents"
        #                 ],
        #                 "Resource": "*"
        #             },
        #             {
        #                 "Sid": "VisualEditor1",
        #                 "Effect": "Allow",
        #                 "Action": "ec2:DescribeTags",
        #                 "Resource": "*"
        #             },
        #             {
        #                 "Sid": "VisualEditor2",
        #                 "Effect": "Allow",
        #                 "Action": [
        #                     "cloudwatch:PutMetricData",
        #                     "cloudwatch:GetMetricStatistics",
        #                     "cloudwatch:ListMetrics"
        #                 ],
        #                 "Resource": "*"
        #             },
        #             {
        #                 "Sid": "VisualEditor3",
        #                 "Effect": "Allow",
        #                 "Action": "logs:CreateLogGroup",
        #                 "Resource": "*"
        #             }
        #         ]
        #     },
        #     "Description": "ECS instance service and cloudwatch logs"
        # }
        response = self.iam_client.create_policy(
            PolicyName=policy_info['PolicyName'],
            # Path='string',
            PolicyDocument=json.dumps(policy_info['PolicyDocument']),
            Description=policy_info['Description'],
        )
        print(response)
        return response['Policy']

    def iam_policy_delete(self, policy_arn):
        response = self.iam_client.delete_policy(
            PolicyArn=policy_arn
        )
        print(response)

    def iam_access_key_create(self, user_name):
        response = self.iam_client.create_access_key(
            UserName=user_name
        )
        user_name = response['AccessKey']['UserName']
        access_key_id = response['AccessKey']['AccessKeyId']
        secret_access_key = response['AccessKey']['SecretAccessKey']
        f = open('%s_credential.txt' % user_name, 'w')
        f.write(user_name + ',' + access_key_id + ',' + secret_access_key)
        f.close()
        print(response)

    def iam_access_key_delete(self, user_name, access_key_id):
        response = self.iam_client.delete_access_key(
            AccessKeyId=access_key_id,
            UserName=user_name,
        )
        print(response)

    def iam_access_keys_list(self):
        response = self.iam_client.list_access_keys(
            # UserName='string',
            # Marker='string',
            # MaxItems=123
        )
        print(response)


if __name__ == '__main__':
    app = AWSIAM()
    # app.iam_role_create('ecsInstanceRole',)
    # app.iam_instance_profile_delete('devops-chain-ecs-instance-role')
    # app.iam_role_to_instance_profile_add('testrole','testrole')
    # app.iam_role_policy_attach('testrole','arn:aws-cn:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role')
    # app.iam_role_get('ecsAutoscaleRole')
    app.iam_access_keys_list()
