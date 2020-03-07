import boto3
import json


def lambda_handler(event, context):
    app = GetResources()
    app.main()


class GetResources(object):
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.resource('s3')
        # self.file_path = '/tmp/instances_information.txt'
        self.file_path = 'vpc_information.txt'
        self.s3_bucket = 'services.information'
        self.s3_file_path = 'vpc_information.txt'
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
        data = json.dumps(data, sort_keys=True, indent=4)
        f = open(path, 'w', encoding='utf-8')
        f.write(data)
        f.close()
        return

    def ec2_vpcs_describe(self, filters):
        response = self.ec2.describe_vpcs(
            Filters=filters,
        )
        return response['Vpcs']

    def ec2_subnets_describe(self, filters):
        response = self.ec2.describe_subnets(
            Filters=filters,
        )
        return response['Subnets']

    def get_subnets_info(self, vpcid):
        filter = [
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcid,
                ]
            },
        ]
        subnets_info = self.ec2_subnets_describe(filter)
        total_subnets_info = []
        for subnet_info in subnets_info:
            ec2_subnet_id = subnet_info['SubnetId']
            ec2_subnet_CidrBlock = subnet_info['CidrBlock']
            ec2_subnet_availability_zone = subnet_info['AvailabilityZone']
            ec2_subnet_name = ""
            if "Tags" in subnet_info.keys():
                for tag in subnet_info['Tags']:
                    if tag['Key'] == 'Name':
                        ec2_subnet_name = tag['Value']
            total_subnets_info.append(
                {
                    'SubnetId': ec2_subnet_id,
                    'CidrBlock': ec2_subnet_CidrBlock,
                    'AvailabilityZone': ec2_subnet_availability_zone,
                    'Name': ec2_subnet_name,
                }
            )
        return total_subnets_info

    def get_nat_gateways_info(self):
        pass

    def get_internet_gateways_info(self):
        pass

    def get_route_tables_info(self):
        pass

    def get_peering_connection_info(self):
        pass

    def main(self):
        total_infos = []
        vpcs_info = self.ec2_vpcs_describe(self.filter)
        for vpc_info in vpcs_info:
            ec2_vpc_id = vpc_info['VpcId']
            ec2_vpc_cidr = vpc_info['CidrBlock']
            ec2_vpc_name = ''
            if "Tags" in vpc_info.keys():
                for tag in vpc_info['Tags']:
                    if tag['Key'] == 'Name':
                        ec2_vpc_name = tag['Value']
            subnets_info = self.get_subnets_info(ec2_vpc_id)
            total_infos.append(
                {
                    'VpcId': ec2_vpc_id,
                    'CidrBlock': ec2_vpc_cidr,
                    'Name': ec2_vpc_name,
                    'subnets': subnets_info,
                }
            )
        print(total_infos)
        # self.write_file(self.file_path,total_infos)
        # self.s3.meta.client.upload_file(self.file_path, self.s3_bucket, self.s3_file_path)


if __name__ == '__main__':
    app = GetResources()
    app.main()
