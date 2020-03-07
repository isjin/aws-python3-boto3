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
        data = json.dumps(data, sort_keys=False, indent=4)
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
        filters = [
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcid,
                ]
            },
        ]
        subnets_info = self.ec2_subnets_describe(filters)
        new_subnets_info = []
        for subnet_info in subnets_info:
            ec2_subnet_id = subnet_info['SubnetId']
            ec2_subnet_cidrblock = subnet_info['CidrBlock']
            # ec2_subnet_availability_zone = subnet_info['AvailabilityZone']
            ec2_subnet_name = None
            if "Tags" in subnet_info.keys():
                for tag in subnet_info['Tags']:
                    if tag['Key'] == 'Name':
                        ec2_subnet_name = tag['Value']
            new_subnets_info.append(
                {
                    'SubnetId': ec2_subnet_id,
                    'SubnetName': ec2_subnet_name,
                    'CidrBlock': ec2_subnet_cidrblock,
                    # 'AvailabilityZone': ec2_subnet_availability_zone,
                }
            )
        return new_subnets_info

    def get_nat_gateways_info(self):
        pass

    def get_internet_gateways_info(self):
        pass

    def ec2_route_tables_describe(self, filters):
        response = self.ec2.describe_route_tables(
            Filters=filters
        )
        return response['RouteTables']

    def get_route_tables_info(self, vpcid):
        new_route_tables_info = []
        filters = [
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcid,
                ]
            },
        ]
        route_tables_info = self.ec2_route_tables_describe(filters)
        for route_table_info in route_tables_info:
            print(route_table_info)
            ec2_route_table_id = route_table_info['RouteTableId']
            ec2_route_table_name=None
            if "Tags" in route_table_info.keys():
                for tag in route_table_info['Tags']:
                    if tag['Key'] == 'Name':
                        ec2_route_table_name = tag['Value']
            new_route_tables_info.append(
                {
                    'RouteTableId':ec2_route_table_id,
                    'RouteTableName':ec2_route_table_name,
                }
            )
        return new_route_tables_info

    def get_peering_connection_info(self):
        pass

    def main(self):
        total_infos = []
        vpcs_info = self.ec2_vpcs_describe(self.filter)
        for vpc_info in vpcs_info:
            ec2_vpc_id = vpc_info['VpcId']
            ec2_vpc_cidr = vpc_info['CidrBlock']
            ec2_vpc_name = None
            if "Tags" in vpc_info.keys():
                for tag in vpc_info['Tags']:
                    if tag['Key'] == 'Name':
                        ec2_vpc_name = tag['Value']
            subnets_info = self.get_subnets_info(ec2_vpc_id)
            route_tables_info = self.get_route_tables_info(ec2_vpc_id)
            total_infos.append(
                {
                    'VpcId': ec2_vpc_id,
                    'VpcName': ec2_vpc_name,
                    'CidrBlock': ec2_vpc_cidr,
                    'Subnets': subnets_info,
                    'RouteTables': route_tables_info
                }
            )
        # print(total_infos)
        self.write_file(self.file_path, total_infos)
        # self.s3.meta.client.upload_file(self.file_path, self.s3_bucket, self.s3_file_path)


if __name__ == '__main__':
    app = GetResources()
    app.main()
