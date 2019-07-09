from function import aws_ec2, aws_iam, aws_cloudformation, aws_ecs
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
        self.ecs = aws_ecs.AWSECS()
        self.cloudformation = aws_cloudformation.AWSCloudFormation()
        self.record = {}
        self.init_record()

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
            self.record['cloudformation'] = {}
            self.record['ecs'] = {}
            self.write_file()

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def write_file(self):
        while True:
            try:
                f = open(record_path, 'w')
                f.write(json.dumps(self.record))
                f.close()
                break
            except Exception as e:
                print(e.__str__())

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

    def create_route(self):
        pass

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
        role_arn = self.iam.iam_role_create(role_info)['Arn']
        self.record['roles'][role_key_name] = {}
        self.record['roles'][role_key_name]['name'] = role_info['RoleName']
        self.record['roles'][role_key_name]['arn'] = role_arn
        self.write_file()
        if role_info['InstanceProfile'] == True:
            instance_profile_arn = self.iam.iam_instance_profile_create(role_info['RoleName'])
            self.record['instance_profiles'][role_key_name] = {}
            self.record['instance_profiles'][role_key_name]['name'] = role_info['RoleName']
            self.record['instance_profiles'][role_key_name]['arn'] = instance_profile_arn
            self.write_file()
            self.iam.iam_role_to_instance_profile_add(role_info['RoleName'], role_info['RoleName'])
        for policy_arn in role_info['PolicyArns']:
            self.iam.iam_role_policy_attach(role_info['RoleName'], policy_arn)
        self.record['policies'][role_key_name] = role_info['PolicyArns']
        self.write_file()

    def create_cloudformation(self, cloudformation_template_path, cloudformation_stack_info,
                              cloudformation_stack_keyname):
        # stack_info = self.read_file(cloudformation_stack_path)
        f = open(cloudformation_template_path, 'r')
        template_data = f.read()
        f.close()
        cloudformation_stack_info['TemplateBody'] = template_data
        # print(stack_info)
        self.cloudformation.cloudformation_stack_create(cloudformation_stack_info)
        self.record['cloudformation'][cloudformation_stack_keyname] = cloudformation_stack_info['StackName']
        self.write_file()

    def create_ec2(self, instance_info, ec2_instance_keyname):
        instance_id = self.ec2.ec2_instance_create(instance_info)[0]
        self.record['ec2_instances'][ec2_instance_keyname] = instance_id
        self.write_file()
        while True:
            # status = self.ec2.ec2_instance_describe('i-0064841176315c612')['Instances'][0]['State']['Name']
            status = self.ec2.ec2_instance_describe(instance_id)['Instances'][0]['State']['Name']
            if status == "pending":
                time.sleep(5)
            else:
                break
        self.assign_eip(instance_id, ec2_instance_keyname)
        return

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

    def assign_eip(self, instanceid, ec2_instance_keyname):
        instance_name = self.get_instance_name(instanceid)
        eipid = self.create_eip(instance_name)
        associate_info = {
            'AllocationId': eipid,
            # 'AllocationId': 'eipalloc-0e0be917bbb463d1c',
            'InstanceId': instanceid,
        }
        self.ec2.ec2_eip_associate_address(associate_info)
        self.record['eips'][ec2_instance_keyname] = eipid
        self.write_file()

    def register_task_definition(self, ecs_task_definition_path):
        task_definition_info = self.read_file(ecs_task_definition_path)
        self.ecs.ecs_task_definition_register(task_definition_info)

    def main(self):
        # create vpc
        print("Create VPC")
        devops_chain_vpc_path = 'config/devops_chain/devops_chain_vpc.txt'
        devops_chain_vpc_keyname = 'devops_chain_vpc'
        if devops_chain_vpc_keyname not in self.record['vpcs'].keys():
            self.create_vpc(devops_chain_vpc_path, devops_chain_vpc_keyname)

        # create subnet
        print("Create subnets")
        devops_chain_subnet_1a_path = 'config/devops_chain/devops_chain_subnet_1a.txt'
        devops_chain_subnet_1a_keyname = 'devops_chain_subnet_1a'
        if devops_chain_subnet_1a_keyname not in self.record['subnets'].keys():
            self.create_subnet(devops_chain_subnet_1a_path, devops_chain_subnet_1a_keyname, devops_chain_vpc_keyname)
        devops_chain_subnet_1b_path = 'config/devops_chain/devops_chain_subnet_1b.txt'
        devops_chain_subnet_1b_keyname = 'devops_chain_subnet_1b'
        if devops_chain_subnet_1b_keyname not in self.record['subnets'].keys():
            self.create_subnet(devops_chain_subnet_1b_path, devops_chain_subnet_1b_keyname, devops_chain_vpc_keyname)
        devops_chain_subnet_1c_path = 'config/devops_chain/devops_chain_subnet_1c.txt'
        devops_chain_subnet_1c_keyname = 'devops_chain_subnet_1c'
        if devops_chain_subnet_1c_keyname not in self.record['subnets'].keys():
            self.create_subnet(devops_chain_subnet_1c_path, devops_chain_subnet_1c_keyname, devops_chain_vpc_keyname)

        # create internet gateway
        print("Create internet gateway")
        devops_chain_igw_path = 'config/devops_chain/devops_chain_igw.txt'
        devops_chain_igw_keyname = 'devops_chain_igw'
        if devops_chain_igw_keyname not in self.record['igws'].keys():
            self.create_igw(devops_chain_igw_path, devops_chain_igw_keyname, devops_chain_vpc_keyname)

        # create routetable
        print("Create route")
        filters = [
            {
                'Name': 'vpc-id',
                'Values': [
                    self.record['vpcs'][devops_chain_vpc_keyname]
                ]
            }
        ]
        routetable_id = self.ec2.ec2_route_tables_describe(filters)[0]['RouteTableId']
        route_table_info = {
            'DestinationCidrBlock': '0.0.0.0/0',
            'GatewayId': self.record['igws'][devops_chain_igw_keyname]
        }
        self.ec2.ec2_route_add_igw(routetable_id, route_table_info)

        # # create keypair
        # print("Create keypair")
        # devops_chain_keypair_name = 'devops_chain_demo'
        # devops_chain_keypair_keyname = 'devops_chain_demo'
        # if devops_chain_keypair_keyname not in self.record['keypairs'].keys():
        #     self.ec2.ec2_key_pair_create(devops_chain_keypair_name)
        #     self.record['keypairs'][devops_chain_keypair_keyname] = devops_chain_keypair_name
        #     self.write_file()
        #
        # create security_group
        print("Create security groups")
        devops_chain_sg_devopschain_path = 'config/devops_chain/devops_chain_sg_devopschain.txt'
        devops_chain_sg_devopschain_inbound_path = 'config/devops_chain/devops_chain_sg_devopschain_inbound.txt'
        devops_chain_sg_devopschain_keyname = 'devops_chain_sg_devopschain'
        if devops_chain_sg_devopschain_keyname not in self.record['security_groups'].keys():
            self.create_security_group(devops_chain_sg_devopschain_path, devops_chain_sg_devopschain_inbound_path,
                                       devops_chain_sg_devopschain_keyname, devops_chain_vpc_keyname)

        # create role
        print("Create roles")
        devops_chain_iam_ecs_instance_role_path = 'config/devops_chain/devops_chain_iam_ecs_instance_role.txt'
        devops_chain_iam_ecs_instance_role_keyname = 'ecs_instance_role'
        if devops_chain_iam_ecs_instance_role_keyname not in self.record['roles'].keys():
            self.create_role(devops_chain_iam_ecs_instance_role_path, devops_chain_iam_ecs_instance_role_keyname)
        devops_chain_iam_ecs_service_role_path = 'config/devops_chain/devops_chain_iam_ecs_service_role.txt'
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

        # create cloudformation
        print("Create cloudformation")
        cloudformation_template_path = 'cloudformation/ecs_template.json'
        cloudformation_stack_path = 'config/devops_chain/devops_chain_cloudformation_ecs.txt'
        cloudformation_stack_info = self.read_file(cloudformation_stack_path)
        ecs_cluster_name = ''
        for parameter in cloudformation_stack_info['Parameters']:
            if parameter['ParameterKey'] == 'IamRoleInstanceProfile':
                parameter['ParameterValue'] = \
                self.record['instance_profiles'][devops_chain_iam_ecs_instance_role_keyname]['arn']
            elif parameter['ParameterKey'] == 'SubnetIds':
                cf_subnets = []
                cf_subnets_id = ''
                for subnet_key in self.record['subnets'].keys():
                    cf_subnets.append(self.record['subnets'][subnet_key])
                cf_subnets_length = len(cf_subnets)
                for i in range(cf_subnets_length):
                    if i == cf_subnets_length - 1:
                        cf_subnets_id = cf_subnets_id + cf_subnets[i]
                    else:
                        cf_subnets_id = cf_subnets_id + cf_subnets[i] + ','
                parameter['ParameterValue'] = cf_subnets_id
            elif parameter['ParameterKey'] == 'SecurityGroupId':
                parameter['ParameterValue'] = self.record['security_groups'][devops_chain_sg_devopschain_keyname]
            # elif parameter['ParameterKey'] == 'KeyName':
            #     parameter['ParameterValue'] = self.record['keypairs'][devops_chain_keypair_keyname]
            elif parameter['ParameterKey'] == 'VpcId':
                parameter['ParameterValue'] = self.record['vpcs'][devops_chain_vpc_keyname]
            elif parameter['ParameterKey'] == 'EcsClusterName':
                ecs_cluster_name = parameter['ParameterValue']
        cf_stack__ecs_keyname = 'devops_chain_ecs'
        if cf_stack__ecs_keyname not in self.record['cloudformation'].keys():
            ecs_cluster_key_name='devops_chain_ecs'
            if ecs_cluster_key_name not in self.record['ecs'].keys():
                self.ecs.ecs_cluster_create(ecs_cluster_name)
                self.record['ecs'][ecs_cluster_key_name]=ecs_cluster_name
                self.write_file()
            self.create_cloudformation(cloudformation_template_path, cloudformation_stack_info, cf_stack__ecs_keyname)

        # register ecs tasks definition
        print("Register ecs tasks definition")
        ecs_task_definition_hello_world_path='config/devops_chain/devops_chain_ecs_task_hello_world.txt'
        self.register_task_definition(ecs_task_definition_hello_world_path)
        ecs_task_definition_gitlab_path='config/devops_chain/devops_chain_ecs_task_gitlab.txt'
        self.register_task_definition(ecs_task_definition_gitlab_path)
        ecs_task_definition_jenkins_path='config/devops_chain/devops_chain_ecs_task_jenkins.txt'
        self.register_task_definition(ecs_task_definition_jenkins_path)
        ecs_task_definition_jira_path='config/devops_chain/devops_chain_ecs_task_jira.txt'
        self.register_task_definition(ecs_task_definition_jira_path)

        # create windows ec2
        print("Create EC2 Windows server")
        ec2_instance_windows_path = 'config/devops_chain/devops_chain_instance_windows.txt'
        ec2_instance_windows_info = self.read_file(ec2_instance_windows_path)
        ec2_instance_windows_info['SecurityGroupIds'] = [self.record['security_groups'][devops_chain_sg_devopschain_keyname], ]
        ec2_instance_windows_info['SubnetId'] = self.record['subnets'][devops_chain_subnet_1a_keyname]
        ec2_instance_windows_keyname = 'windows'
        if ec2_instance_windows_keyname not in self.record['ec2_instances'].keys():
            self.create_ec2(ec2_instance_windows_info, ec2_instance_windows_keyname)
        print("Devops chain environment deployment is Done.")


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
