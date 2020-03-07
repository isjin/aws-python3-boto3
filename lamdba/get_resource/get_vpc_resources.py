import boto3
import json


def lambda_handler(event, context):
    app = GetResources()
    app.main()


class GetResources(object):
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.resource('s3')
        # self.file_path = '/tmp/vpc_information.txt'
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
            # print(subnet_info)
            ec2_subnet_id = subnet_info['SubnetId']
            ec2_subnet_cidrblock = subnet_info['CidrBlock']
            # ec2_subnet_availability_zone = subnet_info['AvailabilityZone']
            ec2_subnet_available_ip_address_count = subnet_info['AvailableIpAddressCount']
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
                    'Available IPv4 IPs': ec2_subnet_available_ip_address_count,
                    # 'AvailabilityZone': ec2_subnet_availability_zone,
                }
            )
        return new_subnets_info

    def ec2_nat_gateways_describe(self, filters):
        response = self.ec2.describe_nat_gateways(
            Filters=filters
        )
        return response['NatGateways']

    def get_nat_gateways_info(self, vpcid):
        filters = [
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcid,
                ]
            },
        ]
        new_nat_gateways_info = []
        nat_gateways_info = self.ec2_nat_gateways_describe(filters)
        for nat_gateway_info in nat_gateways_info:
            # print(nat_gateway_info)
            ec2_nat_gateway_id = nat_gateway_info['NatGatewayId']
            ec2_nat_gateway_private_ip = nat_gateway_info['NatGatewayAddresses'][0]['PrivateIp']
            ec2_nat_gateway_public_ip = nat_gateway_info['NatGatewayAddresses'][0]['PublicIp']
            new_nat_gateways_info.append(
                {
                    'NatGatewayId': ec2_nat_gateway_id,
                    'NatGatewayPublicIp': ec2_nat_gateway_public_ip,
                    'NatGatewayPrivateIp': ec2_nat_gateway_private_ip,
                }
            )
        return new_nat_gateways_info

    def ec2_internet_gateways_describe(self, filters):
        response = self.ec2.describe_internet_gateways(
            Filters=filters,
        )
        return response['InternetGateways']

    def get_internet_gateways_info(self, vpcid):
        filters = [
            {
                'Name': 'attachment.vpc-id',
                'Values': [
                    vpcid,
                ]
            },
        ]
        internet_gateway_info = self.ec2_internet_gateways_describe(filters)[0]
        ec2_internet_gateway_id = internet_gateway_info['InternetGatewayId']
        ec2_internet_gateway_name = None
        if "Tags" in internet_gateway_info.keys():
            for tag in internet_gateway_info['Tags']:
                if tag['Key'] == 'Name':
                    ec2_internet_gateway_name = tag['Value']
        return ec2_internet_gateway_id, ec2_internet_gateway_name

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
            # print(route_table_info)
            ec2_route_table_id = route_table_info['RouteTableId']
            ec2_route_table_name = None
            if "Tags" in route_table_info.keys():
                for tag in route_table_info['Tags']:
                    if tag['Key'] == 'Name':
                        ec2_route_table_name = tag['Value']
            associated_subnets = []
            ec2_route_table_associations = route_table_info['Associations']
            if len(ec2_route_table_associations) > 0:
                for association in ec2_route_table_associations:
                    if "SubnetId" in association.keys():
                        associated_subnets.append(association['SubnetId'])
            routes = []
            ec2_routes = route_table_info['Routes']
            for ec2_route in ec2_routes:
                del ec2_route['Origin']
                del ec2_route['State']
                routes.append(ec2_route)
            new_route_tables_info.append(
                {
                    'RouteTableId': ec2_route_table_id,
                    'RouteTableName': ec2_route_table_name,
                    'AssociatedSubnets': associated_subnets,
                    'Routes': routes,
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
            ec2_internet_gateway_id, ec2_internet_gateway_name = self.get_internet_gateways_info(ec2_vpc_id)
            nat_gateways_info = self.get_nat_gateways_info(ec2_vpc_id)
            total_infos.append(
                {
                    'VpcId': ec2_vpc_id,
                    'VpcName': ec2_vpc_name,
                    'CidrBlock': ec2_vpc_cidr,
                    'InternetGatewaysId': ec2_internet_gateway_id,
                    'InternetGatewaysName': ec2_internet_gateway_name,
                    'Subnets': subnets_info,
                    'RouteTables': route_tables_info,
                    'NatGateways': nat_gateways_info,
                }
            )
        # print(total_infos)
        self.write_file(self.file_path, total_infos)
        self.s3.meta.client.upload_file(self.file_path, self.s3_bucket, self.s3_file_path)


if __name__ == '__main__':
    app = GetResources()
    app.main()
