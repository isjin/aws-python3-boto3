import boto3


class AWSAutoScaling(object):
    def __init__(self):
        self.autoscaling_client = boto3.client('autoscaling')

    def autoscaling_auto_scaling_group_describe(self, autoscaling_group_name):
        response = self.autoscaling_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                autoscaling_group_name,
            ],
            # NextToken='string',
            # MaxRecords=123
        )
        print(response)
        return response

    def autoscaling_auto_scaling_groups_describe(self):
        response = self.autoscaling_client.describe_auto_scaling_groups(
            # AutoScalingGroupNames=[
            #     'string',
            # ],
            # NextToken='string',
            # MaxRecords=123
        )
        # print(response)
        return response['AutoScalingGroups']

    def autoscaling_auto_scaling_instances_describe(self):
        response = self.autoscaling_client.describe_auto_scaling_instances(
            # InstanceIds=[
            #     'string',
            # ],
            # MaxRecords=123,
            # NextToken='string'
        )
        instancesids = []
        for instance in response['AutoScalingInstances']:
            instancesids.append(instance['InstanceId'])
        return instancesids

    def autoscaling_auto_scaling_tags_describe(self):
        response = self.autoscaling_client.describe_tags(
            # Filters=[
            #     {
            #         'Name': 'string',
            #         'Values': [
            #             'string',
            #         ]
            #     },
            # ],
            # NextToken='string',
            # MaxRecords=123
        )
        print(response)

    def autoscaling_launch_configurations_describe(self):
        response = self.autoscaling_client.describe_launch_configurations(
            # LaunchConfigurationNames=[
            #     'string',
            # ],
            # NextToken='string',
            # MaxRecords=123
        )
        # print(response)
        return response['LaunchConfigurations']

    def autoscaling_launch_configuration_describe(self, launch_configuration_name):
        response = self.autoscaling_client.describe_launch_configurations(
            LaunchConfigurationNames=[
                launch_configuration_name,
            ]
        )
        print(response)
        return response['LaunchConfigurations']

    def autoscaling_launch_configuration_create(self,launch_configuration_info):
        # launch_configuration_info = {
        #     'LaunchConfigurationName': 'test01',
        #     'ImageId': 'ami-0b14657cdc08ba6a2',
        #     'KeyName': 'dudu-ecs-key',
        #     'SecurityGroups': ['sg-0bc02e80466875096'],
        #     'UserData': '',
        #     'InstanceType': 'm5.2xlarge',
        #     'BlockDeviceMappings': [
        #         {
        #             'DeviceName': '/dev/xvdcz',
        #             'Ebs': {
        #                 'VolumeSize': 22,
        #                 'VolumeType': 'gp2',
        #                 'DeleteOnTermination': True,
        #                 'Encrypted': False
        #             }
        #         },
        #         {
        #             'DeviceName': '/dev/xvda',
        #             'Ebs': {
        #                 # 'SnapshotId': 'snap-0638f6f44c5e6b07d',
        #                 'VolumeSize': 8,
        #                 'VolumeType': 'gp2',
        #                 'DeleteOnTermination': True
        #             }
        #         }
        #     ],
        #     'InstanceMonitoring': {
        #         'Enabled': True
        #     },
        #     'IamInstanceProfile': 'duduecs-ECSInstanceProfile-XO58MTXI7QDZ',
        # }
        response = self.autoscaling_client.create_launch_configuration(
            LaunchConfigurationName=launch_configuration_info['LaunchConfigurationName'],
            ImageId=launch_configuration_info['ImageId'],
            KeyName=launch_configuration_info['KeyName'],
            SecurityGroups=launch_configuration_info['SecurityGroups'],
            # SecurityGroups=[
            #     'string',
            # ],
            # ClassicLinkVPCId='string',
            # ClassicLinkVPCSecurityGroups=[
            #     'string',
            # ],
            UserData=launch_configuration_info['UserData'],
            # InstanceId='string',
            InstanceType=launch_configuration_info['InstanceType'],
            # KernelId='string',
            # RamdiskId='string',
            BlockDeviceMappings=launch_configuration_info['BlockDeviceMappings'],
            # BlockDeviceMappings=[
            #     {
            #         'VirtualName': 'string',
            #         'DeviceName': 'string',
            #         'Ebs': {
            #             'SnapshotId': 'string',
            #             'VolumeSize': 123,
            #             'VolumeType': 'string',
            #             'DeleteOnTermination': True | False,
            #             'Iops': 123,
            #             'Encrypted': True | False
            #         },
            #         'NoDevice': True | False
            #     },
            # ],
            InstanceMonitoring=launch_configuration_info['InstanceMonitoring'],
            # InstanceMonitoring={
            #     'Enabled': True | False
            # },
            # SpotPrice='string',
            IamInstanceProfile=launch_configuration_info['IamInstanceProfile'],
            # EbsOptimized=True | False,
            # AssociatePublicIpAddress=True | False,
            # PlacementTenancy='string'
        )
        print(response)

    def autoscaling_launch_configuration_delete(self, launch_configuration_name):
        response = self.autoscaling_client.delete_launch_configuration(
            LaunchConfigurationName=launch_configuration_name
        )
        print(response)



if __name__ == '__main__':
    app = AWSAutoScaling()
    # app.autoscaling_auto_scaling_groups_describe()
    # app.autoscaling_auto_launch_configurations_describe()
    # app.autoscaling_launch_configuration_describe('duduecs-ECSLaunchConfiguration-v2')
    # app.autoscaling_launch_configuration_delete('test01')
