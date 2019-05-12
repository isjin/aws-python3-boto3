from function import aws_ec2
from function.aws_rds import AWSRDS
from function.aws_elasticache import AWSElastiCache
from assign_eip import ASSIGNEIP
import json
import os

# Brandgoods


key_pair_uat = 'brandgoods_uat_ssh'
key_pair_prod = 'brandgoods_prod_ssh'
record_path = 'config/brandgoods/brandgoods.log'


class BrandGoods(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.rds = AWSRDS()
        self.elasticache = AWSElastiCache()
        self.assign = ASSIGNEIP()
        self.record = {}
        self.init_record()
        self.vpc_cidr = '10.20.2.0/24'
        self.vpcid = self.record['vpcid']
        # self.vpcid = 'vpc-06e5e4b230542de7b'
        self.subnetid_uat_a = self.record['subnetid_uat_a']
        self.subnetid_prod_b = self.record['subnetid_prod_b']
        self.sg_uat_application_id = self.record['sg_uat_application_id']
        self.sg_prod_application_id = self.record['sg_prod_application_id']
        self.sg_prod_db_id = self.record['sg_prod_db_id']
        self.sg_access_id = self.record['sg_access_id']
        # self.sg_uat_applicatioon_id = 'subnet-0b88d4d63456d0dad'
        # self.subnetid_prod_b = 'subnet-0149d87e3bae5f6a5'
        self.igwid = self.record['igwid']
        # self.igwid = 'igw-07c7878cae15f2ac8'
        self.rds_db_parameter_group_name = self.record['rds_db_parameter_group_name']
        self.rds_option_group_name = self.record['rds_option_group_name']
        self.rds_mysql_identifier = self.record['rds_mysql_identifier']
        self.elasticache_subnet_group = self.record['elasticache_subnet_group']
        self.elasticache_redis_id = self.record['elasticache_redis_id']
        print(self.record, type(self.record))

    def init_record(self):
        if os.path.exists(record_path):
            f = open(record_path, 'r')
            data = f.read()
            f.close()
            self.record = json.loads(data)

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def write_file(self):
        f = open(record_path, 'w')
        f.write(json.dumps(self.record))
        f.close()

    def create_vpc(self):
        vpc_config_path = 'config/brandgoods/vpc.txt'
        vpc_info = self.read_file(vpc_config_path)
        self.vpcid = self.ec2.ec2_vpc_create(vpc_info)
        self.record['vpcid'] = self.vpcid

    def create_subnet(self):
        subnet_uat_config_path = 'config/brandgoods/subnet_uat.txt'
        subnet_prod_config_path = 'config/brandgoods/subnet_prod.txt'
        subnet_uat_info = self.read_file(subnet_uat_config_path)
        subnet_uat_info['vpc'] = self.vpcid
        self.subnetid_uat_a = self.ec2.ec2_subnet_create(subnet_uat_info)
        self.record['subnetid_uat_a'] = self.subnetid_uat_a
        subnet_prod_info = self.read_file(subnet_prod_config_path)
        subnet_prod_info['vpc'] = self.vpcid
        self.subnetid_prod_b = self.ec2.ec2_subnet_create(subnet_prod_info)
        self.record['subnetid_prod_b'] = self.subnetid_prod_b

    def create_internet_gateway(self):
        igw_config_path = 'config/brandgoods/internetgateway.txt'
        igw_tags = self.read_file(igw_config_path)
        self.igwid = self.ec2.ec2_internet_gateway_create(igw_tags)
        self.record['igwid'] = self.igwid
        self.ec2.ec2_internet_gateway_attach(self.igwid, self.vpcid)

    def create_key_pair(self):
        self.ec2.ec2_key_pair_create(key_pair_uat)
        self.ec2.ec2_key_pair_create(key_pair_prod)

    def create_security_group(self):
        sg_uat_application_path = 'config/brandgoods/securitygroup_uat.txt'
        sg_uat_application = self.read_file(sg_uat_application_path)
        sg_uat_application['vpcid'] = self.vpcid
        self.sg_uat_application_id = self.ec2.ec2_security_group_create(sg_uat_application)
        self.record['sg_uat_application_id'] = self.sg_uat_application_id

        sg_prod_application_path = 'config/brandgoods/securitygroup_prod_app.txt'
        sg_prod_application_inbound_path = 'config/brandgoods/sg_inbound_prod_app.txt'
        sg_prod_application = self.read_file(sg_prod_application_path)
        sg_prod_application['vpcid'] = self.vpcid
        self.sg_prod_application_id = self.ec2.ec2_security_group_create(sg_prod_application)
        self.record['sg_prod_application_id'] = self.sg_prod_application_id

        sg_prod_db_path = 'config/brandgoods/securitygroup_prod_db.txt'
        sg_prod_db_inbound_path = 'config/brandgoods/sg_inbound_prod_db.txt'
        sg_prod_db = self.read_file(sg_prod_db_path)
        sg_prod_db['vpcid'] = self.vpcid
        self.sg_prod_db_id = self.ec2.ec2_security_group_create(sg_prod_db)
        self.record['sg_prod_db_id'] = self.sg_prod_db_id

        sg_access_path = 'config/brandgoods/securitygroup_access.txt'
        sg_access_inbound_path = 'config/brandgoods/sg_inbound_access.txt'
        sg_access = self.read_file(sg_access_path)
        sg_access['vpcid'] = self.vpcid
        self.sg_access_id = self.ec2.ec2_security_group_create(sg_access)
        self.record['sg_access_id'] = self.sg_access_id

        # sg_uat_application_inbound_path = 'config/brandgoods/sg_inbound_uat.txt'
        # sg_uat_application_inbound = self.read_file(sg_uat_application_inbound_path)
        # sg_uat_application_inbound['securitygroupid'] = self.sg_uat_application_id
        # self.ec2.ec2_security_group_inbound_policies_add(sg_uat_application_inbound)

        sg_prod_application_inbound = self.read_file(sg_prod_application_inbound_path)
        sg_prod_application_inbound['securitygroupid'] = self.sg_prod_application_id
        sg_prod_application_inbound['policy'][0]['UserIdGroupPairs']['GroupId'] = self.sg_prod_db_id
        self.ec2.ec2_security_group_inbound_policies_add(self.sg_prod_application_id)

        sg_prod_db_inbound = self.read_file(sg_prod_db_inbound_path)
        sg_prod_db_inbound['securitygroupid'] = self.sg_prod_db_id
        sg_prod_application_inbound['policy'][0]['UserIdGroupPairs']['GroupId'] = self.sg_prod_application_id
        sg_prod_application_inbound['policy'][1]['UserIdGroupPairs']['GroupId'] = self.sg_prod_application_id
        self.ec2.ec2_security_group_inbound_policies_add(self.sg_prod_db_id)

        sg_access_inbound = self.read_file(sg_access_inbound_path)
        sg_access_inbound['securitygroupid'] = self.sg_access_id
        self.ec2.ec2_security_group_inbound_policies_add(self.sg_access_id)

    def create_ec2(self):
        instance_uat_path = 'config/brandgoods/instance_app_uat.txt'
        instance_prod_path = 'config/brandgoods/instance_app_prod.txt'
        instance_uat_info = self.read_file(instance_uat_path)
        instance_uat_info['SecurityGroupIds'] = [self.sg_uat_application_id, ]
        instance_prod_info = self.read_file(instance_prod_path)
        instance_prod_info['SecurityGroupIds'] = [self.sg_prod_application_id, ]
        instance_uat_id = self.ec2.ec2_instance_create(instance_uat_info)
        self.record['instance_uat_id'] = instance_uat_id
        instance_prod_id = self.ec2.ec2_instance_create(instance_prod_info)
        self.record['instance_prod_id'] = instance_prod_id
        self.assign.assign_eip(instance_uat_id)
        self.assign.assign_eip(instance_prod_id)

    def create_route_table(self):
        route_table_uat_path = 'config/brandgoods/route_table_uat.txt'
        route_table_prod_path = 'config/brandgoods/route_table_prod.txt'
        route_table_uat_info = self.read_file(route_table_uat_path)
        route_table_uat_info['VpcId'] = self.vpcid
        route_table_prod_info = self.read_file(route_table_prod_path)
        route_table_prod_info['VpcId'] = self.vpcid
        route_table_uat_id = self.ec2.ec2_route_table_create(route_table_uat_info)
        self.record['route_table_uat_id'] = route_table_uat_id
        route_table_igw = {
            'DestinationCidrBlock': '0.0.0.0/0',
            'EgressOnlyInternetGatewayId': self.igwid,
        }
        self.ec2.ec2_route_add_internet_gw(route_table_uat_id, route_table_igw)
        self.ec2.ec2_route_table_subnet_associate(route_table_uat_id, self.subnetid_uat_a)
        route_table_prod_id = self.ec2.ec2_route_table_create(route_table_prod_info)
        self.record['route_table_prod_id'] = route_table_prod_id
        self.ec2.ec2_route_add_internet_gw(route_table_prod_id, route_table_igw)
        self.ec2.ec2_route_table_subnet_associate(route_table_prod_id, self.subnetid_prod_b)

    def create_rds_parameter_group(self):
        rds_parameter_group_path = 'config/brandgoods/rds_parameter_group.txt'
        rds_parameter_group_info = self.read_file(rds_parameter_group_path)
        self.rds_db_parameter_group_name = self.rds.rds_parameter_group_create(rds_parameter_group_info)
        self.record['rds_db_parameter_group_name'] = self.rds_db_parameter_group_name

    def create_rds_option_group(self):
        rds_option_group_path = 'config/brandgoods/rds_option_group.txt'
        rds_option_group_info = self.read_file(rds_option_group_path)
        self.rds_option_group_name = self.rds.rds_option_group_create(rds_option_group_info)

    def create_rds_mysql(self):
        rds_mysql_path = 'config/brandgoods/rds_mysql.txt'
        rds_mysql_info = self.read_file(rds_mysql_path)
        rds_mysql_info['DBParameterGroupName'] = self.rds_db_parameter_group_name
        rds_mysql_info['OptionGroupName'] = self.rds_option_group_name
        rds_mysql_info['VpcSecurityGroupIds'] = [self.sg_prod_db_id, ]
        self.rds_mysql_identifier = self.rds.rds_instance_create(rds_mysql_info)
        self.record['rds_mysql_identifier'] = self.rds_mysql_identifier

    def create_elasticache_subnet_group(self):
        subnet_group_path = 'config/brandgoods/elasticache_subnet_group.txt'
        subnet_group_info = self.read_file(subnet_group_path)
        subnet_group_info['SubnetIds'] = [self.subnetid_prod_b, ]
        self.elasticache_subnet_group = self.elasticache.elasticache_subnet_group_create(subnet_group_info)
        self.record['elasticache_subnet_group'] = self.elasticache_subnet_group

    def create_elasticache_redis(self):
        redis_path = 'config/brandgoods/elasticache_subnet_group.txt'
        redis_info = self.read_file(redis_path)
        redis_info['CacheSubnetGroupName'] = self.elasticache_subnet_group
        redis_info['SecurityGroupIds'] = [self.sg_prod_db_id, ]
        self.elasticache_redis_id = self.elasticache.elasticache_cache_cluster_create(redis_info)
        self.record['elasticache_redis_id'] = self.elasticache_redis_id

    def main(self):
        try:
            if self.vpcid == None:
                self.create_key_pair()
                self.create_vpc()
            if self.subnetid_uat_a == None or self.subnetid_prod_b == None:
                self.create_subnet()
            if self.igwid == None:
                self.create_internet_gateway()
                self.create_route_table()
            self.create_security_group()
            self.create_ec2()
            self.create_rds_parameter_group()
            self.create_rds_option_group()
            self.create_rds_mysql()
            self.create_elasticache_subnet_group()
            self.create_elasticache_redis()
        except Exception as e:
            print(e.__str__())
            self.write_file()
        finally:
            self.write_file()


if __name__ == '__main__':
    app = BrandGoods()
    # app.main()
    # app.create_elasticache_subnet_group()
