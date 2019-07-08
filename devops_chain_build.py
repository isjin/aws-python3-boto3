from function import aws_ec2, aws_iam
import json
import os
import time

# brandedgoods


key_pair = 'devopschaindemo'
record_path = 'config/devops_chain/devops_chain2.log'


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.iam = aws_iam.AWSIAM()
        self.record = {}
        self.init_record()
        # self.vpcid = self.record['vpcid']
        # self.vpcid = 'vpc-09bc1660'
        # self.subnetid_1 = self.record['subnetid_1']
        # self.subnetid_1 = 'subnet-1af53661'
        # self.sg_devopschain_application_id = self.record['sg_devopschain_application_id']
        # self.igwid = self.record['igwid']
        # self.igwid = 'igw-69578f00'

    def init_record(self):
        if os.path.exists(record_path):
            f = open(record_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.record = json.loads(data)
        else:
            self.record['vpcs'] = {}
            self.record['subnets'] = {}
            self.record['security_groups'] = {}
            self.record['ec2_instances'] = {}
            self.record['igws'] = {}
            self.record['ngws'] = {}
            self.record['eips'] = {}
            self.record['keypairs'] = {}
            self.record['roles'] = {}
            self.record['instance_profiles'] = {}
            self.record['policies'] = {}
            self.write_file()

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

    # def create_key_pair(self):
    #     self.ec2.ec2_key_pair_create(key_pair_uat)
    #     self.ec2.ec2_key_pair_create(key_pair_prod)

    def create_vpc(self, vpc_info_path, vpc_key_name):
        vpc_info = self.read_file(vpc_info_path)
        vpc_id = self.ec2.ec2_vpc_create(vpc_info)
        self.record['vpcs'][vpc_key_name] = vpc_id
        self.write_file()

    def create_subnet(self, subnet_info_path, subnet_key_name, vpc_key_name):
        subnet_info = self.read_file(subnet_info_path)
        subnet_info['vpc'] = self.record['vpcs'][vpc_key_name]
        subnet_id = self.ec2.ec2_subnet_create(subnet_info)
        self.record['subnets'][subnet_key_name] = subnet_id
        self.write_file()

    def create_igw(self, igw_info_path, igw_key_name, vpc_key_name):
        igw_info = self.read_file(igw_info_path)
        igw_id = self.ec2.ec2_internet_gateway_create(igw_info)
        self.ec2.ec2_internet_gateway_attach(igw_id, self.record['vpcs'][vpc_key_name])
        self.record['igws'][igw_key_name] = igw_id
        self.write_file()

    def create_security_group(self, security_group_info_path, security_group_rule_info_path, security_group_key_name,
                              vpc_key_name):
        security_group_info = self.read_file(security_group_info_path)
        security_group_info['vpcid'] = self.record['vpcs'][vpc_key_name]
        security_group_id = self.ec2.ec2_security_group_create(security_group_info)
        self.record['security_groups'][security_group_key_name] = security_group_id
        self.write_file()
        security_group_rule_info = self.read_file(security_group_rule_info_path)
        security_group_rule_info['securitygroupid'] = security_group_id
        self.ec2.ec2_security_group_inbound_policies_add(security_group_rule_info)

    def create_role(self, role_info_path, role_key_name):
        role_info = self.read_file(role_info_path)
        self.iam.iam_role_create(role_info)
        self.record['roles'][role_key_name] = role_info['RoleName']
        self.write_file()
        if role_info['InstanceProfile'] == True:
            self.iam.iam_instance_profile_create(role_info['RoleName'])
            self.record['instance_profiles'][role_key_name] = role_info['RoleName']
            self.write_file()
            self.iam.iam_role_to_instance_profile_add(role_info['RoleName'], role_info['RoleName'])
        # print("Attach policies")
        for policy_arn in role_info['PolicyArns']:
            # print(role_info['RoleName'],policy_arn)
            self.iam.iam_role_policy_attach(role_info['RoleName'], policy_arn)
        self.record['policies'][role_key_name] = role_info['PolicyArns']
        self.write_file()

    # def create_instance_profile(self,instance_profile_info_path,instance_profile_key_name):
    #     instance_profiel_info=self.read_file(instance_profile_info_path)
    #     self.iam.iam_role_create(instance_profiel_info)
    #     self.record['instance_profiles'][instance_profile_key_name]=instance_profiel_info['RoleName']
    #     self.write_file()
    #     return instance_profiel_info['RoleName']

    # def attache_role_to_instance_profile(self,instance_profile_name,role_name):
    #     self.iam.iam_role_to_instance_profile_add(instance_profile_name,role_name)

    def create_ecs_roles(self):
        pass

    def create_ec2(self, config_path):
        # instance_1_path = 'config/devops_chain/instance_1.txt'
        instance_path = config_path
        instance_info = self.read_file(instance_path)
        instance_info['SecurityGroupIds'] = [self.sg_devopschain_application_id, ]
        instance_info['SubnetId'] = self.subnetid_1
        instance_id = self.ec2.ec2_instance_create(instance_info)[0]
        # self.record['instance_1_id'] = instance_id
        # self.assign.assign_eip(instance_uat_id)
        # self.assign.assign_eip(instance_prod_id)
        return instance_id

    def get_instance_name(self, instanceid):
        instance_info = self.ec2.ec2_instance_describe(instanceid)
        tags = instance_info['Instances'][0]['Tags']
        instance_name = ''
        for tag in tags:
            if tag['Key'] == "Name":
                instance_name = tag['Value']
                break
        return instance_name

    def create_eip(self, instance_name):
        tags = [
            {
                'Key': 'Name',
                'Value': instance_name
            }
        ]
        eipid = self.ec2.ec2_eip_allocate(tags)
        return eipid

    def assign_eip(self, instanceid):
        instance_name = self.get_instance_name(instanceid)
        eipid = self.create_eip(instance_name)
        associate_info = {
            'AllocationId': eipid,
            # 'AllocationId': 'eipalloc-0e0be917bbb463d1c',
            'InstanceId': instanceid,
        }
        response = self.ec2.ec2_eip_associate_address(associate_info)
        if 'error' in response:
            count = 0
            while True:
                time.sleep(2)
                self.ec2.ec2_eip_associate_address(associate_info)
                count += 1
                if count > 2:
                    break

    def main(self):
        # # create vpc
        # devops_chain_vpc_path = 'config/devops_chain/devops_chain_vpc.txt'
        # devops_chain_vpc_keyname = 'devops_chain_vpc'
        # if devops_chain_vpc_keyname not in self.record['vpcs'].keys():
        #     self.create_vpc(devops_chain_vpc_path, devops_chain_vpc_keyname)
        # # create subnet
        # devops_chain_subnet_1a_path = 'config/devops_chain/devops_chain_subnet_1a.txt'
        # devops_chain_subnet_1a_keyname = 'devops_chain_subnet_1a'
        # if devops_chain_subnet_1a_keyname not in self.record['subnets'].keys():
        #     self.create_subnet(devops_chain_subnet_1a_path, devops_chain_subnet_1a_keyname, devops_chain_vpc_keyname)
        # devops_chain_subnet_1b_path = 'config/devops_chain/devops_chain_subnet_1b.txt'
        # devops_chain_subnet_1b_keyname = 'devops_chain_subnet_1b'
        # if devops_chain_subnet_1b_keyname not in self.record['subnets'].keys():
        #     self.create_subnet(devops_chain_subnet_1b_path, devops_chain_subnet_1b_keyname, devops_chain_vpc_keyname)
        # devops_chain_subnet_1c_path = 'config/devops_chain/devops_chain_subnet_1c.txt'
        # devops_chain_subnet_1c_keyname = 'devops_chain_subnet_1c'
        # if devops_chain_subnet_1c_keyname not in self.record['subnets'].keys():
        #     self.create_subnet(devops_chain_subnet_1c_path, devops_chain_subnet_1c_keyname, devops_chain_vpc_keyname)
        # # create internet gateway
        # devops_chain_igw_path = 'config/devops_chain/devops_chain_igw.txt'
        # devops_chain_igw_keyname = 'devops_chain_igw'
        # if devops_chain_igw_keyname not in self.record['igws'].keys():
        #     self.create_igw(devops_chain_igw_path, devops_chain_igw_keyname, devops_chain_vpc_keyname)
        # # create keypair
        # devops_chain_keypair_name = 'devops_chain_demo'
        # devops_chain_keypair_keyname = 'devops_chain_demo'
        # if devops_chain_keypair_keyname not in self.record['keypairs'].keys():
        #     self.ec2.ec2_key_pair_create(devops_chain_keypair_name)
        #     self.record['keypairs'][devops_chain_keypair_keyname] = devops_chain_keypair_name
        #     self.write_file()
        # # create security_group
        # devops_chain_sg_devopschain_path = 'config/devops_chain/devops_chain_sg_devopschain.txt'
        # devops_chain_sg_devopschain_inbound_path = 'config/devops_chain/devops_chain_sg_devopschain_inbound.txt'
        # devops_chain_sg_devopschain_keyname = 'devops_chain_sg_devopschain'
        # if devops_chain_sg_devopschain_keyname not in self.record['security_groups'].keys():
        #     self.create_security_group(devops_chain_sg_devopschain_path, devops_chain_sg_devopschain_inbound_path,
        #                                devops_chain_sg_devopschain_keyname, devops_chain_vpc_keyname)

        # create role
        devops_chain_iam_ecs_instance_role_path = 'config/devops_chain/devops_chain_iam_ecs_instance_role.txt'
        devops_chain_iam_ecs_instance_role_keyname = 'ecs_instance_role'
        if devops_chain_iam_ecs_instance_role_keyname not in self.record['roles'].keys():
            self.create_role(devops_chain_iam_ecs_instance_role_path, devops_chain_iam_ecs_instance_role_keyname)
        devops_chain_iam_ecs_service_role_path='config/devops_chain/devops_chain_iam_ecs_service_role.txt'
        devops_chain_iam_ecs_service_role_keyname = 'ecs_service_role'
        if devops_chain_iam_ecs_service_role_keyname not in self.record['roles'].keys():
            self.create_role(devops_chain_iam_ecs_service_role_path, devops_chain_iam_ecs_service_role_keyname)
        devops_chain_iam_ecs_task_role_path = 'config/devops_chain/devops_chain_iam_ecs_task_role.txt'
        devops_chain_iam_ecs_task_role_keyname = 'ecs_task_role'
        if devops_chain_iam_ecs_task_role_keyname not in self.record['roles'].keys():
            self.create_role(devops_chain_iam_ecs_task_role_path, devops_chain_iam_ecs_task_role_keyname)
        devops_chain_iam_ecs_autoscale_role_path = 'config/devops_chain/devops_chain_iam_ecs_autoscale_role.txt'
        devops_chain_iam_ecs_autoscale_role_keyname = 'ecs_autoscale_role'
        if devops_chain_iam_ecs_autoscale_role_keyname not in self.record['roles'].keys():
            self.create_role(devops_chain_iam_ecs_autoscale_role_path, devops_chain_iam_ecs_autoscale_role_keyname)



if __name__ == '__main__':
    app = DevopsChain()
    app.main()
