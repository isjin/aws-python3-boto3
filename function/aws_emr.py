import boto3


class AWSS3(object):
    def __init__(self):
        self.emr_client = boto3.client('emr')

    def emr_cluster_describe(self, clusterid):
        response = self.emr_client.describe_cluster(
            ClusterId=clusterid
        )
        print(response)
        return response

    def emr_cluster_create(self, emr_info):
        # emr_info={
        #     'Name':'aidatagov',
        #     'LogUri':'s3://aidatagov.emr01/aidatagov-logs/',
        #     'ReleaseLabel':'emr-5.24.0',
        #     'Instances':{
        #         'InstanceType':'m3.xlarge',
        #         'Ec2KeyName':'aidatagov',
        #         'Ec2SubnetIds':['subnet-8f3baceb',],
        #     },
        #     'Applications':[
        #         {
        #             'Name': 'Hadoop',
        #             'Version': '2.8.5'
        #         },
        #         {
        #             'Name': 'Hive',
        #             'Version': '2.3.4'
        #         },
        #         {
        #             'Name': 'Hue',
        #             'Version': '4.4.0'
        #         }
        #     ],
        #     'JobFlowRole': 'EMR_EC2_DefaultRole',
        #     'ServiceRole': 'EMR_DefaultRole',
        #     'Tags': [
        #         # {
        #         #     'Key': 'string',
        #         #     'Value': 'string'
        #         # },
        #     ]
        # }
        response = self.emr_client.run_job_flow(
            Name=emr_info['Name'],
            LogUri=emr_info['LogUri'],
            # AdditionalInfo='string',
            # AmiVersion='string',
            ReleaseLabel=emr_info['ReleaseLabel'],
            Instances={
                'MasterInstanceType': emr_info['Instances']['InstanceType'],
                'SlaveInstanceType': emr_info['Instances']['InstanceType'],
                'InstanceCount': 3,
                # 'InstanceGroups': [
                #     {
                #         'Name': 'string',
                #         'Market': 'ON_DEMAND' | 'SPOT',
                #         'InstanceRole': 'MASTER' | 'CORE' | 'TASK',
                #         'BidPrice': 'string',
                #         'InstanceType': 'string',
                #         'InstanceCount': 123,
                #         'Configurations': [
                #             {
                #                 'Classification': 'string',
                #                 'Configurations': {'... recursive ...'},
                #                 'Properties': {
                #                     'string': 'string'
                #                 }
                #             },
                #         ],
                #         'EbsConfiguration': {
                #             'EbsBlockDeviceConfigs': [
                #                 {
                #                     'VolumeSpecification': {
                #                         'VolumeType': 'string',
                #                         'Iops': 123,
                #                         'SizeInGB': 123
                #                     },
                #                     'VolumesPerInstance': 123
                #                 },
                #             ],
                #             'EbsOptimized': True | False
                #         },
                #         'AutoScalingPolicy': {
                #             'Constraints': {
                #                 'MinCapacity': 123,
                #                 'MaxCapacity': 123
                #             },
                #             'Rules': [
                #                 {
                #                     'Name': 'string',
                #                     'Description': 'string',
                #                     'Action': {
                #                         'Market': 'ON_DEMAND' | 'SPOT',
                #                         'SimpleScalingPolicyConfiguration': {
                #                             'AdjustmentType': 'CHANGE_IN_CAPACITY' | 'PERCENT_CHANGE_IN_CAPACITY' | 'EXACT_CAPACITY',
                #                             'ScalingAdjustment': 123,
                #                             'CoolDown': 123
                #                         }
                #                     },
                #                     'Trigger': {
                #                         'CloudWatchAlarmDefinition': {
                #                             'ComparisonOperator': 'GREATER_THAN_OR_EQUAL' | 'GREATER_THAN' | 'LESS_THAN' | 'LESS_THAN_OR_EQUAL',
                #                             'EvaluationPeriods': 123,
                #                             'MetricName': 'string',
                #                             'Namespace': 'string',
                #                             'Period': 123,
                #                             'Statistic': 'SAMPLE_COUNT' | 'AVERAGE' | 'SUM' | 'MINIMUM' | 'MAXIMUM',
                #                             'Threshold': 123.0,
                #                             'Unit': 'NONE' | 'SECONDS' | 'MICRO_SECONDS' | 'MILLI_SECONDS' | 'BYTES' | 'KILO_BYTES' | 'MEGA_BYTES' | 'GIGA_BYTES' | 'TERA_BYTES' | 'BITS' | 'KILO_BITS' | 'MEGA_BITS' | 'GIGA_BITS' | 'TERA_BITS' | 'PERCENT' | 'COUNT' | 'BYTES_PER_SECOND' | 'KILO_BYTES_PER_SECOND' | 'MEGA_BYTES_PER_SECOND' | 'GIGA_BYTES_PER_SECOND' | 'TERA_BYTES_PER_SECOND' | 'BITS_PER_SECOND' | 'KILO_BITS_PER_SECOND' | 'MEGA_BITS_PER_SECOND' | 'GIGA_BITS_PER_SECOND' | 'TERA_BITS_PER_SECOND' | 'COUNT_PER_SECOND',
                #                             'Dimensions': [
                #                                 {
                #                                     'Key': 'string',
                #                                     'Value': 'string'
                #                                 },
                #                             ]
                #                         }
                #                     }
                #                 },
                #             ]
                #         }
                #     },
                # ],
                # 'InstanceFleets': [
                #     {
                #         'Name': 'string',
                #         'InstanceFleetType': 'MASTER' | 'CORE' | 'TASK',
                #         'TargetOnDemandCapacity': 123,
                #         'TargetSpotCapacity': 123,
                #         'InstanceTypeConfigs': [
                #             {
                #                 'InstanceType': 'string',
                #                 'WeightedCapacity': 123,
                #                 'BidPrice': 'string',
                #                 'BidPriceAsPercentageOfOnDemandPrice': 123.0,
                #                 'EbsConfiguration': {
                #                     'EbsBlockDeviceConfigs': [
                #                         {
                #                             'VolumeSpecification': {
                #                                 'VolumeType': 'string',
                #                                 'Iops': 123,
                #                                 'SizeInGB': 123
                #                             },
                #                             'VolumesPerInstance': 123
                #                         },
                #                     ],
                #                     'EbsOptimized': True | False
                #                 },
                #                 'Configurations': [
                #                     {
                #                         'Classification': 'string',
                #                         'Configurations': {'... recursive ...'},
                #                         'Properties': {
                #                             'string': 'string'
                #                         }
                #                     },
                #                 ]
                #             },
                #         ],
                #         'LaunchSpecifications': {
                #             'SpotSpecification': {
                #                 'TimeoutDurationMinutes': 123,
                #                 'TimeoutAction': 'SWITCH_TO_ON_DEMAND' | 'TERMINATE_CLUSTER',
                #                 'BlockDurationMinutes': 123
                #             }
                #         }
                #     },
                # ],
                'Ec2KeyName': emr_info['Instances']['Ec2KeyName'],
                # 'Placement': {
                #     'AvailabilityZone': 'string',
                #     'AvailabilityZones': [
                #         'string',
                #     ]
                # },
                'KeepJobFlowAliveWhenNoSteps': False,
                'TerminationProtected': False,
                # 'HadoopVersion': emr_info['Instances']['HadoopVersion'],
                # 'Ec2SubnetId': 'string',
                'Ec2SubnetIds': emr_info['Instances']['Ec2SubnetIds'],
                # 'EmrManagedMasterSecurityGroup': 'string',
                # 'EmrManagedSlaveSecurityGroup': 'string',
                # 'ServiceAccessSecurityGroup': 'string',
                # 'AdditionalMasterSecurityGroups': [
                #     'string',
                # ],
                # 'AdditionalSlaveSecurityGroups': [
                #     'string',
                # ]
            },
            # Steps=[
            #             #     {
            #             #         'Name': 'string',
            #             #         'ActionOnFailure': 'TERMINATE_JOB_FLOW' | 'TERMINATE_CLUSTER' | 'CANCEL_AND_WAIT' | 'CONTINUE',
            #             #         'HadoopJarStep': {
            #             #             'Properties': [
            #             #                 {
            #             #                     'Key': 'string',
            #             #                     'Value': 'string'
            #             #                 },
            #             #             ],
            #             #             'Jar': 'string',
            #             #             'MainClass': 'string',
            #             #             'Args': [
            #             #                 'string',
            #             #             ]
            #             #         }
            #             #     },
            #             # ],
            # BootstrapActions=[
            #     {
            #         'Name': 'string',
            #         'ScriptBootstrapAction': {
            #             'Path': 'string',
            #             'Args': [
            #                 'string',
            #             ]
            #         }
            #     },
            # ],
            # SupportedProducts=[
            #     'string',
            # ],
            # NewSupportedProducts=[
            #     {
            #         'Name': 'string',
            #         'Args': [
            #             'string',
            #         ]
            #     },
            # ],
            Applications=emr_info['Applications'],
            # Configurations=[
            #     {
            #         'Classification': 'string',
            #         'Configurations': {'... recursive ...'},
            #         'Properties': {
            #             'string': 'string'
            #         }
            #     },
            # ],
            VisibleToAllUsers=True,
            JobFlowRole=emr_info['JobFlowRole'],
            ServiceRole=emr_info['ServiceRole'],
            Tags=emr_info['Tags'],
            # SecurityConfiguration='string',
            # AutoScalingRole='string',
            # ScaleDownBehavior='TERMINATE_AT_INSTANCE_HOUR' | 'TERMINATE_AT_TASK_COMPLETION',
            # CustomAmiId='string',
            # EbsRootVolumeSize=123,
            # RepoUpgradeOnBoot='SECURITY' | 'NONE',
            # KerberosAttributes={
            #     'Realm': 'string',
            #     'KdcAdminPassword': 'string',
            #     'CrossRealmTrustPrincipalPassword': 'string',
            #     'ADDomainJoinUser': 'string',
            #     'ADDomainJoinPassword': 'string'
            # }
        )
        print(response)
        return


if __name__ == '__main__':
    app = AWSS3()
    app.emr_cluster_describe('j-1D42XBDMWY41Y')
