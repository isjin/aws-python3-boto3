import boto3


class AWSRDS(object):
    def __init__(self):
        self.rds_client = boto3.client('rds')

    def rds_subnet_group_create(self,rds_subnet_group_info):
        # rds_subnet_group_info = {
        #     'DBSubnetGroupName': 'bpm-prod-rds-mysql-subnet-group',
        #     'DBSubnetGroupDescription': 'bpm-prod-rds-mysql-subnet-group',
        #     'SubnetIds': ['subnet-08858afacc0b207f6', 'subnet-081ec6dcfe3e57414'],
        # }
        response = self.rds_client.create_db_subnet_group(
            DBSubnetGroupName=rds_subnet_group_info['DBSubnetGroupName'],
            DBSubnetGroupDescription=rds_subnet_group_info['DBSubnetGroupDescription'],
            SubnetIds=rds_subnet_group_info['SubnetIds'],
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ]
        )
        print(response)
        return response['DBSubnetGroup']['DBSubnetGroupName']


    def rds_parameter_group_create(self,rds_parameter_group):
        # rds_parameter_group = {
        #     'DBParameterGroupName': 'bpm-prod-rds-mysql-parameter-group',
        #     'DBParameterGroupFamily': 'mysql5.7',
        #     'Description': 'bpm-prod-rds-mysql-parameter-group',
        # }
        response = self.rds_client.create_db_parameter_group(
            DBParameterGroupName=rds_parameter_group['DBParameterGroupName'],
            DBParameterGroupFamily=rds_parameter_group['DBParameterGroupFamily'],
            Description=rds_parameter_group['Description'],
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ]
        )
        print(response)
        return response['DBParameterGroup']['DBParameterGroupName']

    def rds_option_group_create(self,rds_option_group):
        # rds_option_group = {
        #     'OptionGroupName': 'bpm-prod-rds-mysql-option-group',
        #     'EngineName': 'mysql',
        #     'MajorEngineVersion': '5.7',
        #     'OptionGroupDescription': 'bpm-prod-rds-mysql-option-group',
        # }
        response = self.rds_client.create_option_group(
            OptionGroupName=rds_option_group['OptionGroupName'],
            EngineName=rds_option_group['EngineName'],
            MajorEngineVersion=rds_option_group['MajorEngineVersion'],
            OptionGroupDescription=rds_option_group['OptionGroupDescription'],
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ]
        )
        print(response)
        return response['OptionGroup']['OptionGroupName']

    def rds_instance_create(self,rds_info):
        # rds_info = {
        #     'DBInstanceIdentifier': 'brandgoods-prod-rds-mysql',
        #     'AllocatedStorage': 200,
        #     'DBInstanceClass': 'db.m4.large',
        #     'Engine': 'mysql',
        #     'EngineVersion': '5.6.43',
        #     'MasterUsername': 'brandgoodssys',
        #     'MasterUserPassword': 'NzoRnS}%',
        #     'DBSubnetGroupName': 'bpm-prod-rds-mysql-subnet-group',
        #     'DBParameterGroupName': 'bpm-prod-rds-mysql-parameter-group',
        #     'OptionGroupName': 'bpm-prod-rds-mysql-option-group',
        #     'VpcSecurityGroupIds': ['sg-0e72915b04b73fd44'],
        #     'AvailabilityZone': 'cn-north-1b',
        #     'StorageType': 'gp2',
        #     'Tags': [
        #         {
        #             'Key': 'Name',
        #             'Value': 'prod-bpm-paicore-mysql'
        #         },
        #         {
        #             'Key': 'System',
        #             'Value': 'BPM'
        #         },
        #     ],
        #
        # }
        response = self.rds_client.create_db_instance(
            # DBName=rds_info['DBName'],
            DBInstanceIdentifier=rds_info['DBInstanceIdentifier'],
            AllocatedStorage=rds_info['AllocatedStorage'],
            DBInstanceClass=rds_info['DBInstanceClass'],
            Engine=rds_info['Engine'],
            MasterUsername=rds_info['MasterUsername'],
            MasterUserPassword=rds_info['MasterUserPassword'],
            # DBSecurityGroups=[
            #     'string',
            # ],
            VpcSecurityGroupIds=rds_info['VpcSecurityGroupIds'],
            AvailabilityZone=rds_info['AvailabilityZone'],
            DBSubnetGroupName=rds_info['DBSubnetGroupName'],
            # PreferredMaintenanceWindow='string',
            DBParameterGroupName=rds_info['DBParameterGroupName'],
            # BackupRetentionPeriod=123,
            # PreferredBackupWindow='string',
            # Port=123,
            EngineVersion=rds_info['EngineVersion'],
            # AutoMinorVersionUpgrade=True | False,
            # LicenseModel='string',
            # Iops=123,
            OptionGroupName=rds_info['OptionGroupName'],
            # CharacterSetName='string',
            PubliclyAccessible=False,
            Tags=rds_info['Tags'],
            # DBClusterIdentifier='string',
            StorageType=rds_info['StorageType'],
            # TdeCredentialArn='string',
            # TdeCredentialPassword='string',
            # StorageEncrypted=True | False,
            # KmsKeyId='string',
            # Domain='string',
            # CopyTagsToSnapshot=True | False,
            # MonitoringInterval=123,
            # MonitoringRoleArn='string',
            # DomainIAMRoleName='string',
            # PromotionTier=123,
            # Timezone='string',
            # EnableIAMDatabaseAuthentication=True | False,
            # EnablePerformanceInsights=True | False,
            # PerformanceInsightsKMSKeyId='string',
            # PerformanceInsightsRetentionPeriod=123,
            # EnableCloudwatchLogsExports=[
            #     'string',
            # ],
            # ProcessorFeatures=[
            #     {
            #         'Name': 'string',
            #         'Value': 'string'
            #     },
            # ],
            DeletionProtection=True
        )
        print(response)
        return response['DBInstance']['DBInstanceIdentifier']

    def rds_instance_describe(self, instance):
        response = self.rds_client.describe_db_instances(
            DBInstanceIdentifier=instance,
            # Filters=[
            #     {
            #         'Name': 'string',
            #         'Values': [
            #             'string',
            #         ]
            #     },
            # ],
            # MaxRecords=123,
            # Marker='string'
        )
        return response

    def rds_instances_describe(self):
        response = self.rds_client.describe_db_instances(
            # DBInstanceIdentifier=instance,
            # Filters=[
            #     {
            #         'Name': 'string',
            #         'Values': [
            #             'string',
            #         ]
            #     },
            # ],
            # MaxRecords=123,
            # Marker='string'
        )
        # print(response)
        return response['DBInstances']


if __name__ == '__main__':
    app = AWSRDS()
    # app.rds_instance_describe('dev-brand-apps-mysql')
    app.rds_instances_describe()
    # app.rds_subnet_group_create()
    # app.rds_parameter_group_create()
    # app.rds_option_group_create()
    # app.rds_instance_create()
