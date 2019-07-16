from function import aws_ec2, aws_iam, aws_cloudformation, aws_ecs, aws_ecr
import json
import os
import time
from datetime import datetime
from configparser import ConfigParser

cf = ConfigParser()
cf.read('build_resources_config.ini')
resource_path = cf.get('resource', 'path')


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.iam = aws_iam.AWSIAM()
        self.ecs = aws_ecs.AWSECS()
        self.ecr = aws_ecr.AWSECR()
        self.cloudformation = aws_cloudformation.AWSCloudFormation()
        self.resources = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)
        else:
            self.resources['ecs_clusters'] = {}
            self.resources['ecs_task_definitions'] = {}
            self.resources['ecr_repositories'] = {}
            self.resources['igws'] = {}
            self.resources['ngws'] = {}
            self.resources['rtbs'] = {}
            self.resources['roles'] = {}
            self.resources['nacls'] = {}
            self.resources['keypairs'] = {}
            self.resources['auto_scaling'] = {}
            self.resources['ec2_instances'] = {}
            self.resources['eips'] = {}
            self.resources['volumes'] = {}
            self.resources['snapshots'] = {}
            self.resources['images'] = {}
            self.resources['elbs'] = {}
            self.resources['security_groups'] = {}
            self.resources['subnets'] = {}
            self.resources['vpcs'] = {}
            self.resources['cloudformations'] = {}
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
                f = open(resource_path, 'w')
                f.write(json.dumps(self.resources))
                f.close()
                break
            except Exception as e:
                print(e.__str__())

    def create_vpc(self, vpc_info_path, vpc_key_name):
        vpc_info = self.read_file(vpc_info_path)
        vpc_id = self.ec2.ec2_vpc_create(vpc_info)
        self.resources['vpcs'][vpc_key_name] = vpc_id
        self.write_file()

    def create_subnet(self, subnet_info_path, subnet_key_name, vpc_key_name):
        subnet_info = self.read_file(subnet_info_path)
        subnet_info['vpc'] = self.resources['vpcs'][vpc_key_name]
        subnet_id = self.ec2.ec2_subnet_create(subnet_info)
        self.resources['subnets'][subnet_key_name] = subnet_id
        self.write_file()

    def create_igw(self, igw_info_path, igw_key_name, vpc_key_name):
        igw_info = self.read_file(igw_info_path)
        igw_id = self.ec2.ec2_internet_gateway_create(igw_info)
        self.ec2.ec2_internet_gateway_attach(igw_id, self.resources['vpcs'][vpc_key_name])
        self.resources['igws'][igw_key_name] = igw_id
        self.write_file()

    def create_default_route(self, vpc_key_name, igw_key_name, route_table_name):
        filters = [
            {
                'Name': 'vpc-id',
                'Values': [
                    self.resources['vpcs'][vpc_key_name]
                ]
            }
        ]
        routetable_id = self.ec2.ec2_route_tables_describe(filters)[0]['RouteTableId']
        route_table_tag = {
            'tag': 'Name',
            'tag_description': route_table_name
        }
        self.ec2.ec2_tag_create(routetable_id, route_table_tag)
        route_info = {
            'DestinationCidrBlock': '0.0.0.0/0',
            'GatewayId': self.resources['igws'][igw_key_name]
        }
        self.ec2.ec2_route_add_igw(routetable_id, route_info)

    def create_route(self):
        pass

    def create_keypair(self, keypair_name, keypair_key_name):
        self.ec2.ec2_key_pair_create(keypair_name)
        self.resources['keypairs'][keypair_key_name] = keypair_name
        self.write_file()

    def create_security_group(self, sg_info_path, sg_rule_info_path, sg_key_name, vpc_key_name):
        security_group_info = self.read_file(sg_info_path)
        security_group_info['vpcid'] = self.resources['vpcs'][vpc_key_name]
        security_group_id = self.ec2.ec2_security_group_create(security_group_info)
        self.resources['security_groups'][sg_key_name] = security_group_id
        self.write_file()
        security_group_rule_info = self.read_file(sg_rule_info_path)
        security_group_rule_info['securitygroupid'] = security_group_id
        self.ec2.ec2_security_group_inbound_policies_add(security_group_rule_info)

    def create_role(self, role_info_path, role_key_name):
        role_info = self.read_file(role_info_path)
        role_arn = self.iam.iam_role_create(role_info)['Arn']
        self.resources['roles'][role_key_name] = {}
        self.resources['roles'][role_key_name]['name'] = role_info['RoleName']
        self.resources['roles'][role_key_name]['arn'] = role_arn
        self.write_file()
        if role_info['InstanceProfile']:
            instance_profile_arn = self.iam.iam_instance_profile_create(role_info['RoleName'])
            self.resources['instance_profiles'][role_key_name] = {}
            self.resources['instance_profiles'][role_key_name]['name'] = role_info['RoleName']
            self.resources['instance_profiles'][role_key_name]['arn'] = instance_profile_arn
            self.write_file()
            self.iam.iam_role_to_instance_profile_add(role_info['RoleName'], role_info['RoleName'])
        for policy_arn in role_info['PolicyArns']:
            self.iam.iam_role_policy_attach(role_info['RoleName'], policy_arn)
        self.resources['policies'][role_key_name] = role_info['PolicyArns']
        self.write_file()

    def create_ecr_repository(self, repository_name, repository_keyname):
        self.ecr.repository_create(repository_name)
        self.resources['ecr_repositories'][repository_keyname] = repository_name
        self.write_file()

    def create_ecs_cluster(self, cluster_name, ecs_keyname):
        self.ecs.ecs_cluster_create(cluster_name)
        self.resources['ecs_clusters'][ecs_keyname] = cluster_name
        self.write_file()

    def create_cloudformation(self, cf_template_path, cf_stack_info, cf_stack_keyname):
        # stack_info = self.read_file(cloudformation_stack_path)
        f = open(cf_template_path, 'r')
        template_data = f.read()
        f.close()
        cf_stack_info['TemplateBody'] = template_data
        # print(stack_info)
        self.cloudformation.cloudformation_stack_create(cf_stack_info)
        self.resources['cloudformations'][cf_stack_keyname] = cf_stack_info['StackName']
        self.write_file()

    def create_ec2_instance(self, ec2_instance_path, sg_keyname, subnet_keyname, ec2_instance_keyname, eip_value):
        instance_info = self.read_file(ec2_instance_path)
        instance_info['SecurityGroupIds'] = [self.resources['security_groups'][sg_keyname]]
        instance_info['SubnetId'] = self.resources['subnets'][subnet_keyname]
        instance_id = self.ec2.ec2_instance_create(instance_info)[0]
        self.resources['ec2_instances'][ec2_instance_keyname] = instance_id
        self.write_file()
        while True:
            # status = self.ec2.ec2_instance_describe('i-0064841176315c612')['Instances'][0]['State']['Name']
            status = self.ec2.ec2_instance_describe(instance_id)['Instances'][0]['State']['Name']
            if status == "pending":
                time.sleep(5)
            else:
                break
        if eip_value == 'true':
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
        self.resources['eips'][ec2_instance_keyname] = eipid
        self.write_file()

    def register_task_definition(self, ecs_task_definition_path, ecs_task_definition_keyname):
        task_definition_info = self.read_file(ecs_task_definition_path)
        self.ecs.ecs_task_definition_register(task_definition_info)
        self.resources['ecs_tasks_definitions'][ecs_task_definition_keyname] = task_definition_info['family']
        self.write_file()

    def main(self):
        for service in cf.sections():
            service = str(service)
            if service not in ['resource', 'ecs_tasks']:
                print("%s Start create %s." % (datetime.now(), service))
                for item in cf.options(service):
                    info = str(cf.get(service, item))
                    info = info.split(',')
                    if service == 'default_routes':
                        if info[3] == "true":
                            self.create_default_route(info[0], info[1], info[2])
                        pass
                    elif info[0] not in self.resources[service].keys():
                        if service == 'vpcs':
                            self.create_vpc(info[1], info[0])
                        elif service == 'subnets':
                            self.create_subnet(info[1], info[0], info[2])
                        elif service == 'igws':
                            self.create_igw(info[1], info[0], info[2])
                        elif service == 'keypairs':
                            self.create_keypair(info[1], info[0])
                        elif service == 'security_groups':
                            self.create_security_group(info[1], info[2], info[0], info[3])
                        elif service == 'roles':
                            self.create_role(info[1], info[0])
                        elif service == 'ecr_repositories':
                            self.create_ecr_repository(info[1], info[0])
                        elif service == 'ecs_clusters':
                            self.create_ecs_cluster(info[1], info[0])
                        elif service == 'cloudformations':
                            cf_stack_info = self.read_file(info[1])
                            cf_parameters = str(info[3]).split(';')
                            subnetids_keyname = cf_parameters[0].split('=')[1].split('-')
                            subnetids_keyname_length = len(subnetids_keyname)
                            subnetids = ''
                            for i in range(subnetids_keyname_length):
                                subnet_id = self.resources['subnets'][subnetids_keyname[i]]
                                if i == subnetids_keyname_length - 1:
                                    subnetids = subnetids + subnet_id
                                else:
                                    subnetids = subnetids + subnet_id + ','
                            sg_keyname = cf_parameters[1].split('=')[1]
                            vpc_keyname = cf_parameters[2].split('=')[1]
                            parameters = []
                            for parameter in cf_stack_info['Parameters']:
                                if parameter['ParameterKey'] == 'VpcId':
                                    parameter['ParameterValue'] = self.resources['vpcs'][vpc_keyname]
                                    parameters.append(parameter)
                                elif parameter['ParameterKey'] == 'SubnetIds':
                                    parameter['ParameterValue'] = subnetids
                                    parameters.append(parameter)
                                elif parameter['ParameterKey'] == 'SecurityGroupId':
                                    parameter['ParameterValue'] = self.resources['security_groups'][sg_keyname]
                                    parameters.append(parameter)
                                else:
                                    parameters.append(parameter)
                            cf_stack_info['Parameters'] = parameters
                            self.create_cloudformation(info[2], cf_stack_info, info[0])
                        elif service == 'ecs_tasks_definitions':
                            self.register_task_definition(info[1], info[0])
                        elif service == 'ec2_instances':
                            self.create_ec2_instance(info[1], info[2], info[3], info[0], info[4])
                            pass
                        else:
                            print("%s Service %s %s does not create because it is not in scope!" % (datetime.now(), service, item))
                print("%s Service %s creation is done." % (datetime.now(), service))
        print("%s Infrastructure deployment is done." % (datetime.now()))

        # run ecs task definitions
        print('%s Start to deploy ECS tasks.' % (datetime.now()))
        for item in cf.options('ecs_tasks'):
            task_info = cf.get('ecs_tasks', item)
            task_info = str(task_info).split(',')
            ecs_cluster_name = task_info[0]
            task_definition_name = task_info[1]
            while True:
                ecs_instance_count = self.ecs.ecs_cluster_describe(ecs_cluster_name)['clusters'][0]['registeredContainerInstancesCount']
                if ecs_instance_count > 0:
                    print("%s Deploy task %s" % (datetime.now(), task_definition_name))
                    self.ecs.ecs_task_run(ecs_cluster_name, task_definition_name)
                    break
                time.sleep(5)
        print('%s Deploy ECS tasks is done.' % (datetime.now()))
        print('%s All are finished..' % (datetime.now()))


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
