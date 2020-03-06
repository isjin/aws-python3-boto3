import boto3
import json
from datetime import datetime


def lambda_handler(event, context):
    app = GetResources()
    app.main()


class GetResources(object):
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.resource('s3')
        # self.file_path = '/tmp/instances_information.txt'
        self.file_path = 'instances_information.txt'
        self.s3_bucket = 'services.information'
        self.s3_file_path = 'instances_information.txt'
        self.filter = [
            # {
            #     'Name': 'tag:System',
            #     'Values': [
            #         'OP',
            #     ]
            # },
        ]

    @staticmethod
    def write_file(path,data):
        data = json.dumps(data,sort_keys=True,indent=4)
        f = open(path, 'w',encoding='utf-8')
        f.write(data)
        f.close()
        return

    def ec2_instances_describe(self):
        response = self.ec2.describe_instances(
            Filters=self.filter,
        )
        # print(response)
        return response['Reservations']

    def get_instanceids(self):
        instanceids = []
        instances_info = self.ec2_instances_describe()
        for instance_info in instances_info:
            instanceids.append(instance_info['Instances'][0]['InstanceId'])
        return instanceids

    def ec2_instance_describe(self, instanceid):
        response = self.ec2.describe_instances(
            InstanceIds=[
                instanceid,
            ],
        )
        return response['Reservations']

    def ec2_volume_describe(self, volumeid):
        response = self.ec2.describe_volumes(
            VolumeIds=[
                volumeid,
            ],
        )
        return response['Volumes'][0]

    def ec2_security_group_describe(self, sgid):
        response = self.ec2.describe_security_groups(
            GroupIds=[
                sgid,
            ],
        )
        return response['SecurityGroups'][0]

    def main(self):
        instances_infos = []
        ec2_instances_info = self.ec2_instances_describe()
        for ec2_instance_info in ec2_instances_info:
            ec2_instance_info = ec2_instance_info['Instances'][0]
            # print(ec2_instance)
            ec2_image_id = ec2_instance_info['ImageId']
            ec2_instance_id = ec2_instance_info['InstanceId']
            ec2_keyname = ec2_instance_info['KeyName']
            ec2_launch_time = ec2_instance_info['LaunchTime']
            ec2_state = ec2_instance_info['State']['Name']
            ec2_monitoring = ec2_instance_info['Monitoring']['State']
            ec2_launch_time = datetime.strftime(ec2_launch_time, '%Y-%m-%d %H:%M:%S')
            if 'Platform' in ec2_instance_info:
                ec2_platform = ec2_instance_info['Platform']
            else:
                ec2_platform = 'Linux'
            ec2_private_ip = ec2_instance_info['PrivateIpAddress']
            ec2_subnet_id = ec2_instance_info['SubnetId']
            ec2_vpc_id = ec2_instance_info['VpcId']
            ec2_architecture = ec2_instance_info['Architecture']
            ec2_ebs_optimized = ec2_instance_info['EbsOptimized']
            ec2_ena_support = ec2_instance_info['EnaSupport']
            ec2_hypervisor = ec2_instance_info['Hypervisor']
            ec2_virtualizationtype = ec2_instance_info['VirtualizationType']
            ec2_instance_name = ''
            for tag in ec2_instance_info['Tags']:
                if tag['Key'] == 'Name':
                    ec2_instance_name = tag['Value']
            ec2_cpu_count = int(ec2_instance_info['CpuOptions']['CoreCount']) * int(ec2_instance_info['CpuOptions']['ThreadsPerCore'])
            ec2_az = ec2_instance_info['Placement']['AvailabilityZone']
            if 'PublicIpAddress' in ec2_instance_info.keys():
                ec2_public_ip = ec2_instance_info['PublicIpAddress']
            else:
                ec2_public_ip = None
            ec2_sg_ids_info = []
            ec2_sg_infos = ec2_instance_info['NetworkInterfaces'][0]['Groups']
            for sg_info in ec2_sg_infos:
                ec2_sg_id = sg_info['GroupId']
                ec2_sg_id_info = self.ec2_security_group_describe(ec2_sg_id)

                def format_data(data):
                    for each_data in data:
                        # print(each_data)
                        for key in list(each_data.keys()):
                            key_data = each_data[key]
                            # print(each_data[key])
                            if each_data[key] == "-1":
                                each_data[key] = "All"
                            if type(key_data) is list:
                                if len(key_data) == 0:
                                    del each_data[key]
                                else:
                                    format_data(key_data)
                    return data

                ec2_sg_id_inbound_infos = ec2_sg_id_info['IpPermissions']
                ec2_sg_id_inbound_infos = format_data(ec2_sg_id_inbound_infos)
                ec2_sg_id_outbound_infos = ec2_sg_id_info['IpPermissionsEgress']
                ec2_sg_id_outbound_infos = format_data(ec2_sg_id_outbound_infos)
                ec2_sg_ids_info.append(
                    {'SecurityGroupID': ec2_sg_id, 'InboundRules': ec2_sg_id_inbound_infos, 'OutboundRules': ec2_sg_id_outbound_infos})
            ec2_role = ''
            if 'IamInstanceProfile' in ec2_instance_info.keys():
                ec2_role = ec2_instance_info['IamInstanceProfile']['Arn']
            ec2_ebs_ids_info = []
            ec2_ebs_infos = ec2_instance_info['BlockDeviceMappings']
            for ebs_info in ec2_ebs_infos:
                ec2_ebs_id = ebs_info['Ebs']['VolumeId']
                ec2_ebs_info = self.ec2_volume_describe(ec2_ebs_id)
                ec2_ebs_encrypted = ec2_ebs_info['Encrypted']
                ec2_ebs_size = ec2_ebs_info['Size']
                ec2_ebs_volume_type = ec2_ebs_info['VolumeType']
                ec2_ebs_ids_info.append(
                    {'VolumeId': ec2_ebs_id, 'Encrypted': ec2_ebs_encrypted, 'Size': ec2_ebs_size, 'VolumeType': ec2_ebs_volume_type})
            # print(ec2_instance_id, ec2_image_id, ec2_platform, ec2_keyname, ec2_private_ip, ec2_public_ip, ec2_subnet_id, ec2_vpc_id,
            #       ec2_architecture, ec2_ebs_optimized, ec2_ena_support, ec2_hypervisor, ec2_virtualizationtype, ec2_instance_name, ec2_cpu_count,
            #       ec2_az, ec2_sg_ids_info, ec2_role,ec2_ebs_ids_info, ec2_launch_time)
            instances_infos.append(
                {
                    'InstanceId': ec2_instance_id,
                    'ImageId': ec2_image_id,
                    'Platform': ec2_platform,
                    'KeyName': ec2_keyname,
                    'PrivateIpAddress': ec2_private_ip,
                    'PublicIpAddress': ec2_public_ip,
                    'SubnetId': ec2_subnet_id,
                    'VpcId': ec2_vpc_id,
                    'Architecture': ec2_architecture,
                    'EbsOptimized': ec2_ebs_optimized,
                    'EnaSupport': ec2_ena_support,
                    'Hypervisor': ec2_hypervisor,
                    'VirtualizationType': ec2_virtualizationtype,
                    'Name': ec2_instance_name,
                    'CPUCore': ec2_cpu_count,
                    'AvailabilityZone': ec2_az,
                    'SecurityGroup': ec2_sg_ids_info,
                    'IamInstanceProfile': ec2_role,
                    'Volumes': ec2_ebs_ids_info,
                    'LaunchTime': ec2_launch_time,
                    'State': ec2_state,
                    'Monitoring': ec2_monitoring,
                }
            )
        # print(instances_infos)
        self.write_file(self.file_path,instances_infos)
        self.s3.meta.client.upload_file(self.file_path, self.s3_bucket, self.s3_file_path)



# if __name__ == '__main__':
#     app = GetResources()
#     app.main()
