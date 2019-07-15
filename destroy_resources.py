from function import aws_ec2, aws_iam, aws_cloudformation, aws_ecs, aws_ecr
import json
import os
import time
from datetime import datetime
from configparser import ConfigParser

resouces_conf_path = 'resouces_config.ini'
resource_log_path = 'resources.log'
cf = ConfigParser()
cf.read(resouces_conf_path)


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.iam = aws_iam.AWSIAM()
        self.cf = aws_cloudformation.AWSCloudFormation()
        self.ecs = aws_ecs.AWSECS()
        self.ecr = aws_ecr.AWSECR()
        self.resources = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resource_log_path):
            f = open(resource_log_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)

    def write_file(self):
        f = open(resource_log_path, 'w')
        f.write(json.dumps(self.resources))
        f.close()

    def delete_vpc(self, vpc_id, keyname):
        try:
            self.ec2.ec2_vpc_delete(vpc_id)
            del self.resources['vpcs'][keyname]
            self.write_file()
            print("%s VPC %s has deleted." % (datetime.now(), vpc_id))
        except Exception as e:
            print(e.__str__())

    def delete_subnet(self, subnet_id, keyname):
        try:
            self.ec2.ec2_subnet_delete(subnet_id)
            del self.resources['subnets'][keyname]
            self.write_file()

        except Exception as e:
            print(e.__str__())

    def delete_igws(self, igw_id, keyname):
        try:
            igw_info = self.ec2.ec2_internet_gateway_describe(igw_id)
            attachments_length = len(igw_info[0]['Attachments'])
            if attachments_length > 0:
                vpcid = igw_info[0]['Attachments'][0]['VpcId']
                self.ec2.ec2_internet_gateway_detach(igw_id, vpcid)
            self.ec2.ec2_internet_gateway_delete(igw_id)
            del self.resources['igws'][keyname]
            print("%s Internet gateway %s has deleted." % (datetime.now(), igw_id))
            self.write_file()
        except Exception as e:
            print(e.__str__())

    def delete_keypair(self, keypair_name, keyname):
        try:
            self.ec2.ec2_key_pair_delete(keypair_name)
            del self.resources['keypairs'][keyname]
            self.write_file()
        except Exception as e:
            print(e.__str__())

    def delete_security_group(self, sg_id, keyname):
        try:
            self.ec2.ec2_security_group_delete(sg_id)
            del self.resources['security_groups'][keyname]
            self.write_file()
            print("%s Security group %s has deleted." % (datetime.now(), sg_id))
        except Exception as e:
            print(e.__str__())

    def delete_cloudformation(self, stack_name, keyname):
        try:
            self.cf.cloudformation_stack_delete(stack_name)
            while True:
                try:
                    self.cf.cloudformation_stack_describe(stack_name)
                    time.sleep(5)
                except Exception:
                    print("%s Cloudformation stack %s has deleted." % (datetime.now(), stack_name))
                    break
            del self.resources['cloudformations'][keyname]
            self.write_file()
        except Exception as e:
            print(e.__str__())

    def delete_ecs_cluster(self, cluster_name, keyname):
        try:
            self.ecs.ecs_cluster_delete(cluster_name)
            del self.resources['ecs_clusters'][keyname]
            self.write_file()
            print("%s ECS cluster %s has deleted." % (datetime.now(), cluster_name))
        except Exception as e:
            print(e.__str__())

    def delete_eip(self, public_ip, keyname):
        try:
            self.ec2.ec2_eip_release_public_ip(public_ip)
            del self.resources['eips'][keyname]
            print("%s Elastic IP %s has deleted." % (datetime.now(), public_ip))
        except Exception as e:
            print(e.__str__())

    def delete_ec2_instance(self, instance_id, keyname):
        try:
            instance_info = self.ec2.ec2_instance_describe(instance_id)['Instances'][0]
            if 'PublicIpAddress' in instance_info.keys():
                public_ip = instance_info['PublicIpAddress']
                self.ec2.ec2_eip_release_public_ip(public_ip)
            volumes_info = instance_info['BlockDeviceMappings']
            self.ec2.ec2_instance_delete(instance_id)
            for volume_info in volumes_info:
                device_name = volume_info['DeviceName']
                if device_name not in ['/dev/sda1', '/dev/xvda']:
                    volume_id = volume_info['Ebs']['VolumeId']
                    self.ec2.ec2_volume_delete(volume_id)
            del self.resources['ec2_instances'][keyname]
            print("%s EC2 instance %s has deleted." % (datetime.now(), instance_id))
            self.write_file()
        except Exception as e:
            print(e.__str__())

    def delete_ecr_repository(self, repository_name, keyname):
        try:
            self.ecr.repository_delete(repository_name)
            del self.resources['ecr_repositories'][keyname]
            self.write_file()
            print("%s ECR repository %s has deleted." % (datetime.now(), repository_name))
        except Exception as e:
            print(e.__str__())

    def delete_volume(self, volume_id, keyname):
        try:
            self.ec2.ec2_volume_delete(volume_id)
            del self.resources['volumes'][keyname]
            self.write_file()
            print("%s Volume %s has deleted." % (datetime.now(), volume_id))
        except Exception as e:
            print(e.__str__())

    def deregister_task_definition(self, task_definition_arn, keyname):
        try:
            self.ecs.ecs_task_definition_deregister(task_definition_arn)
            del self.resources['task_definition_arn'][keyname]
            self.write_file()
            print("%s ECS task definition %s has deleted." % (datetime.now(), task_definition_arn))
        except Exception as e:
            print(e.__str__())

    def delete_rtb(self, rtb_id, keyname):
        try:
            rtb_info = self.ec2.ec2_route_table_describe(rtb_id)
            associations_length = len(rtb_info['Associations'])
            if associations_length > 0:
                for i in range(associations_length):
                    association_id = rtb_info['Associations'][i]['RouteTableAssociationId']
                    self.ec2.ec2_route_table_subnet_disassociate(association_id)
            self.ec2.ec2_route_table_delete(rtb_id)
            del self.resources['rtbs'][keyname]
            self.write_file()
            print("%s Route table %s has deleted." % (datetime.now(), rtb_id))
        except Exception as e:
            print(e.__str__())

    def main(self):
        # self.delete_ec2()
        # self.delete_keypair()
        # time.sleep(60)
        for service in cf.sections():
            print("%s Start to delete %s" % (datetime.now(), service))
            for option in cf.options(service):
                item = cf.get(service, option)
                if service == 'cloudformations':
                    self.delete_cloudformation(item, option)
                elif service == 'vpcs':
                    self.delete_vpc(item, option)
                elif service == 'security_groups':
                    self.delete_security_group(item, option)
                elif service == 'subnets':
                    self.delete_subnet(item, option)
                elif service == 'volumes':
                    self.delete_volume(item, option)
                elif service == 'ecs_clusters':
                    self.delete_ecs_cluster(item, option)
                elif service == 'ecs_task_definitions':
                    self.deregister_task_definition(item, option)
                elif service == 'ecr_repositories':
                    self.delete_ecr_repository(item, option)
                elif service == 'igws':
                    self.delete_igws(item, option)
                elif service == 'ngws':
                    pass
                elif service == 'rtbs':
                    self.delete_rtb(item, option)
                elif service == 'nacls':
                    pass
                elif service == 'roles':
                    pass
                elif service == 'keypairs':
                    self.delete_keypair(item, option)
                elif service == 'auto_scaling':
                    pass
                elif service == 'ec2_instances':
                    self.delete_ec2_instance(item, option)
                elif service == 'eips':
                    self.delete_eip(item, option)
                elif service == 'snapshots':
                    pass
                elif service == 'images':
                    pass
            print("%s Delete %s are finished." % (datetime.now(), service))
        # os.system("python get_resouces.py")
        # os.system("python generate_resources_config.py")


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
