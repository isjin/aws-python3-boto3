import boto3
import json


# from datetime import datetime


def lambda_handler(event, context):
    app = GetResources()
    app.main()


class GetResources(object):
    def __init__(self):
        self.rds = boto3.client('rds')
        self.s3 = boto3.resource('s3')
        # self.file_path = '/tmp/instances_information.txt'
        self.file_path = 'rds_information.txt'
        self.s3_bucket = 'services.information'
        self.s3_file_path = 'rds_information.txt'
        self.filter = [
            # {
            #     'Name': 'tag:System',
            #     'Values': [
            #         'OP',
            #     ]
            # },
        ]

    @staticmethod
    def write_file(path, data):
        data = json.dumps(data, sort_keys=False, indent=4)
        f = open(path, 'w', encoding='utf-8')
        f.write(data)
        f.close()
        return

    def rds_instances_describe(self):
        response = self.rds.describe_db_instances(
        )
        return response['DBInstances']

    def main(self):
        new_rdss_infos = []
        rdss_infos = self.rds_instances_describe()
        for rds_info in rdss_infos:
            # print(rds_info)
            rds_name = rds_info['DBInstanceIdentifier']
            rds_endpoint = rds_info['Endpoint']
            rds_engine = rds_info['Engine']
            rds_instance_type = rds_info['DBInstanceClass']
            rds_subnet_group_name = rds_info['DBSubnetGroup']['DBSubnetGroupName']
            rds_subnets = []
            rds_subnets_info = rds_info['DBSubnetGroup']['Subnets']
            for rds_subnet_info in rds_subnets_info:
                subnet_id = rds_subnet_info['SubnetIdentifier']
                # subnet_az = rds_subnet_info['Name']
                rds_subnets.append(subnet_id)
            rds_backup_window = rds_info['PreferredBackupWindow']
            rds_backup_retention_period= rds_info['BackupRetentionPeriod']
            del rds_endpoint['HostedZoneId']
            new_rdss_infos.append(
                {
                    'DBName':rds_name,
                    'Endpoint':rds_endpoint,
                    'Engine':rds_engine,
                    'DBInstanceType':rds_instance_type,
                    'DBSubnetGroupName':rds_subnet_group_name,
                    'DBSubnets':rds_subnets,
                    'BackupWindow':rds_backup_window,
                    'BackupRetentionPeriod':rds_backup_retention_period,
                }
            )
        # print(instances_infos)
        self.write_file(self.file_path, new_rdss_infos)
        # self.s3.meta.client.upload_file(self.file_path, self.s3_bucket, self.s3_file_path)


if __name__ == '__main__':
    app = GetResources()
    app.main()
