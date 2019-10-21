import boto3


class AWSAutoScaling(object):
    def __init__(self):
        self.autoscaling_client = boto3.client('autoscaling')

    def autoscaling_auto_scaling_group_create(self, auto_scaling_group_info):
        # auto_scaling_group_info = {
        #     'AutoScalingGroupName': 'test',
        #     'LaunchConfigurationName': 'duduecs-ECSLaunchConfiguration-v2',
        #     'MinSize': 0,
        #     'MaxSize': 0,
        #     'DesiredCapacity': 0,
        #     'AvailabilityZones': ['cn-northwest-1b', 'cn-northwest-1a'],
        #     'LoadBalancerNames': [],
        #     'TargetGroupARNs': [],
        #     'HealthCheckType': 'EC2',
        #     'HealthCheckGracePeriod': 900,
        #     'VPCZoneIdentifier': 'subnet-02c381dfd8ac365ce,subnet-0dd642e5edfba9083',
        #     'Tags': [
        #         {
        #             'ResourceId': 'test',
        #             'ResourceType': 'auto-scaling-group',
        #             'Key': 'Name',
        #             'Value': 'test',
        #             'PropagateAtLaunch': True
        #         },
        #     ],
        #     'ServiceLinkedRoleARN': 'arn:aws-cn:iam::646976741397:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling'
        # }
        response = self.autoscaling_client.create_auto_scaling_group(
            AutoScalingGroupName=auto_scaling_group_info['AutoScalingGroupName'],
            LaunchConfigurationName=auto_scaling_group_info['LaunchConfigurationName'],
            # LaunchTemplate={
            #     'LaunchTemplateId': 'string',
            #     'LaunchTemplateName': 'string',
            #     'Version': 'string'
            # },
            # MixedInstancesPolicy={
            #     'LaunchTemplate': {
            #         'LaunchTemplateSpecification': {
            #             'LaunchTemplateId': 'string',
            #             'LaunchTemplateName': 'string',
            #             'Version': 'string'
            #         },
            #         'Overrides': [
            #             {
            #                 'InstanceType': 'string'
            #             },
            #         ]
            #     },
            #     'InstancesDistribution': {
            #         'OnDemandAllocationStrategy': 'string',
            #         'OnDemandBaseCapacity': 123,
            #         'OnDemandPercentageAboveBaseCapacity': 123,
            #         'SpotAllocationStrategy': 'string',
            #         'SpotInstancePools': 123,
            #         'SpotMaxPrice': 'string'
            #     }
            # },
            # InstanceId='string',
            MinSize=auto_scaling_group_info['MinSize'],
            MaxSize=auto_scaling_group_info['MaxSize'],
            DesiredCapacity=auto_scaling_group_info['DesiredCapacity'],
            # DefaultCooldown=123,
            AvailabilityZones=auto_scaling_group_info['AvailabilityZones'],
            LoadBalancerNames=auto_scaling_group_info['LoadBalancerNames'],
            TargetGroupARNs=auto_scaling_group_info['TargetGroupARNs'],
            HealthCheckType=auto_scaling_group_info['HealthCheckType'],
            HealthCheckGracePeriod=auto_scaling_group_info['HealthCheckGracePeriod'],
            # PlacementGroup='string',
            VPCZoneIdentifier=auto_scaling_group_info['VPCZoneIdentifier'],
            # TerminationPolicies=[
            #     'string',
            # ],
            # NewInstancesProtectedFromScaleIn=True | False,
            # LifecycleHookSpecificationList=[
            #     {
            #         'LifecycleHookName': 'string',
            #         'LifecycleTransition': 'string',
            #         'NotificationMetadata': 'string',
            #         'HeartbeatTimeout': 123,
            #         'DefaultResult': 'string',
            #         'NotificationTargetARN': 'string',
            #         'RoleARN': 'string'
            #     },
            # ],
            # Tags=[
            Tags=auto_scaling_group_info['Tags'],
            #     {
            #         'ResourceId': 'string',
            #         'ResourceType': 'string',
            #         'Key': 'string',
            #         'Value': 'string',
            #         'PropagateAtLaunch': True | False
            #     },
            # ],
            ServiceLinkedRoleARN=auto_scaling_group_info['ServiceLinkedRoleARN'],
        )
        print(response)
        return response

    def autoscaling_auto_scaling_group_delete(self, autoscaling_group_name):
        response = self.autoscaling_client.delete_auto_scaling_group(
            AutoScalingGroupName=autoscaling_group_name,
            # ForceDelete=True | False
        )
        print(response)

    def autoscaling_auto_scaling_group_update(self, autoscaling_group_info):
        auto_scaling_group_info = {
            'AutoScalingGroupName': 'test',
            'LaunchConfigurationName': 'duduecs-ECSLaunchConfiguration-v2',
            'MinSize': 0,
            'MaxSize': 0,
            'DesiredCapacity': 0,
            'AvailabilityZones': ['cn-northwest-1b', 'cn-northwest-1a'],
            'LoadBalancerNames': [],
            'TargetGroupARNs': [],
            'HealthCheckType': 'EC2',
            'HealthCheckGracePeriod': 900,
            'VPCZoneIdentifier': 'subnet-02c381dfd8ac365ce,subnet-0dd642e5edfba9083',
            'ServiceLinkedRoleARN': 'arn:aws-cn:iam::646976741397:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling'
        }
        response = self.autoscaling_client.update_auto_scaling_group(
            AutoScalingGroupName=auto_scaling_group_info['AutoScalingGroupName'],
            LaunchConfigurationName=auto_scaling_group_info['AutoScalingGroupName'],
            # LaunchTemplate={
            #     'LaunchTemplateId': 'string',
            #     'LaunchTemplateName': 'string',
            #     'Version': 'string'
            # },
            # MixedInstancesPolicy={
            #     'LaunchTemplate': {
            #         'LaunchTemplateSpecification': {
            #             'LaunchTemplateId': 'string',
            #             'LaunchTemplateName': 'string',
            #             'Version': 'string'
            #         },
            #         'Overrides': [
            #             {
            #                 'InstanceType': 'string'
            #             },
            #         ]
            #     },
            #     'InstancesDistribution': {
            #         'OnDemandAllocationStrategy': 'string',
            #         'OnDemandBaseCapacity': 123,
            #         'OnDemandPercentageAboveBaseCapacity': 123,
            #         'SpotAllocationStrategy': 'string',
            #         'SpotInstancePools': 123,
            #         'SpotMaxPrice': 'string'
            #     }
            # },
            MinSize=auto_scaling_group_info['MinSize'],
            MaxSize=auto_scaling_group_info['MaxSize'],
            DesiredCapacity=auto_scaling_group_info['DesiredCapacity'],
            DefaultCooldown=auto_scaling_group_info['DefaultCooldown'],
            AvailabilityZones=auto_scaling_group_info['AvailabilityZones'],
            HealthCheckType=auto_scaling_group_info['HealthCheckType'],
            HealthCheckGracePeriod=auto_scaling_group_info['HealthCheckGracePeriod'],
            # PlacementGroup='string',
            VPCZoneIdentifier=auto_scaling_group_info['VPCZoneIdentifier'],
            # TerminationPolicies=[
            #     'string',
            # ],
            # NewInstancesProtectedFromScaleIn=True | False,
            ServiceLinkedRoleARN=auto_scaling_group_info['ServiceLinkedRoleARN'],
        )
        print(response)

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

    def autoscaling_launch_configuration_create(self, launch_configuration_info):
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

    def autoscaling_tags_create_update(self,tags):
        # tags=[
        #     {
        #         'ResourceId': 'duduecs-ECSAutoScalingGroup-1EDDAPCMEZVZ1',
        #         'ResourceType': 'auto-scaling-group',
        #         'Key': 'test',
        #         'Value': 'test',
        #         'PropagateAtLaunch': True
        #     },
        # ]
        response = self.autoscaling_client.create_or_update_tags(
            Tags=tags
        )
        print(response)

    def autoscaling_tags_delete(self,tags):
        # tags=[
        #     {
        #         'ResourceId': 'duduecs-ECSAutoScalingGroup-1EDDAPCMEZVZ1',
        #         'ResourceType': 'auto-scaling-group',
        #         'Key': 'test',
        #         'Value': 'test',
        #         'PropagateAtLaunch': True
        #     },
        # ]
        response = self.autoscaling_client.delete_tags(
            Tags=tags
        )
        print(response)


if __name__ == '__main__':
    app = AWSAutoScaling()
    # app.autoscaling_auto_scaling_groups_describe()
    # app.autoscaling_auto_launch_configurations_describe()
    # app.autoscaling_launch_configuration_describe('duduecs-ECSLaunchConfiguration-v2')
    # app.autoscaling_auto_scaling_group_describe('duduecs-ECSAutoScalingGroup-1EDDAPCMEZVZ1')
    # app.autoscaling_tags_delete(1)
    # app.autoscaling_auto_scaling_group_delete('test')
