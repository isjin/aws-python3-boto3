from function import aws_ec2, aws_iam, aws_cloudformation, aws_ecs, aws_ecr
import json
import os
import time

# brandedgoods
from configparser import ConfigParser

key_pair = 'devopschaindemo'
record_path = 'config/test/test.log'


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.iam = aws_iam.AWSIAM()
        self.cf = aws_cloudformation.AWSCloudFormation()
        self.ecs = aws_ecs.AWSECS()
        self.ecr = aws_ecr.AWSECR()
        self.record = {}
        self.init_record()

    def init_record(self):
        if os.path.exists(record_path):
            f = open(record_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
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

    def delete_vpcs(self):
        print("Start to delete vpcs")
        for key in list(self.record['vpcs'].keys()):
            try:
                self.ec2.ec2_vpc_delete(self.record['vpcs'][key])
                del self.record['vpcs'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete vpcs are finished.")

    def delete_subnets(self):
        print("Start to delete subnets")
        for key in list(self.record['subnets'].keys()):
            try:
                self.ec2.ec2_subnet_delete(self.record['subnets'][key])
                del self.record['subnets'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete subnets are finished.")

    def delete_igws(self):
        print("Start to delete internet gateways")
        for key in list(self.record['igws'].keys()):
            try:
                vpcid = \
                    self.ec2.ec2_internet_gateway_describe(self.record['igws'][key])['InternetGateways'][0][
                        'Attachments'][
                        0]['VpcId']
                self.ec2.ec2_internet_gateway_detach(self.record['igws'][key], vpcid)
                self.ec2.ec2_internet_gateway_delete(self.record['igws'][key])
                del self.record['igws'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete internet gateways are finished.")

    def delete_keypair(self):
        print("Start to delete keypairs")
        for key in list(self.record['keypairs'].keys()):
            try:
                self.ec2.ec2_key_pair_delete(self.record['keypairs'][key])
                del self.record['keypairs'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete keypairs are finished.")

    def delete_security_groups(self):
        print("Start to delete security groups")
        for key in list(self.record['security_groups'].keys()):
            try:
                self.ec2.ec2_security_group_delete(self.record['security_groups'][key])
                del self.record['security_groups'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete security groups are finished.")

    def delete_role(self):
        print("Start to delete roles")
        for key in list(self.record['roles'].keys()):
            try:
                if key in self.record['instance_profiles'].keys():
                    self.iam.iam_role_to_instance_profile_remove(self.record['instance_profiles'][key]['name'],
                                                                 self.record['roles'][key]['name'])
                    self.iam.iam_instance_profile_delete(self.record['instance_profiles'][key]['name'])
                    del self.record['instance_profiles'][key]
                    self.write_file()
                for policy_arn in self.record['policies'][key]:
                    self.iam.iam_role_policy_detach(self.record['roles'][key]['name'], policy_arn)
                self.iam.iam_role_delete(self.record['roles'][key]['name'])
                del self.record['policies'][key]
                self.write_file()
                del self.record['roles'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())

        print("Delete roles are finished.")

    def delete_cloudformation(self):
        print("Start to delete cloudformations")
        for key in list(self.record['cloudformations'].keys()):
            stack_name = self.record['cloudformations'][key]
            try:
                self.cf.cloudformation_stack_delete(stack_name)
                while True:
                    try:
                        self.cf.cloudformation_stack_describe(stack_name)
                        time.sleep(5)
                    except Exception:
                        print("Deleting cloudformation stack %s." % stack_name)
                        break
                del self.record['cloudformations'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete cloudformations are finished.")

    def delete_ecs(self):
        print("Start to delete ECS")
        for key in list(self.record['ecs'].keys()):
            while True:
                try:
                    self.ecs.ecs_cluster_delete(self.record['ecs'][key])
                    del self.record['ecs'][key]
                    self.write_file()
                    break
                except Exception as e:
                    print(e.__str__())
                    time.sleep(15)
        print("Delete ECS is finished.")

    def delete_ec2(self):
        print("Start to delete EC2")
        for key in list(self.record['eips'].keys()):
            try:
                eipid = self.record['eips'][key]
                association_id = self.ec2.ec2_eip_allocation_id_describe(eipid)['Addresses'][0]['AssociationId']
                self.ec2.ec2_eip_disassociate_address(association_id)
                self.ec2.ec2_eip_release(eipid)
                del self.record['eips'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())

        for key in list(self.record['ec2_instances'].keys()):
            try:
                instance_id = self.record['ec2_instances'][key]
                volumes_info = self.ec2.ec2_instance_describe(instance_id)['Instances'][0]['BlockDeviceMappings']
                self.ec2.ec2_instance_delete(instance_id)
                for volume_info in volumes_info:
                    device_name = volume_info['DeviceName']
                    if device_name not in ['/dev/sda1', '/dev/xvda']:
                        volume_id = volume_info['Ebs']['VolumeId']
                        self.ec2.ec2_volume_delete(volume_id)
                del self.record['ec2_instances'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete EC2 is finished.")

    def delete_ecr(self):
        print("Start to delete ECR")
        for key in list(self.record['ecrs'].keys()):
            try:
                self.ecr.repository_delete(self.record['ecrs'][key])
                del self.record['ecrs'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete ECR is finished.")

    def main(self):
        self.delete_ec2()
        self.delete_cloudformation()
        self.delete_ecs()
        self.delete_ecr()
        self.delete_role()
        self.delete_security_groups()
        self.delete_keypair()
        self.delete_igws()
        self.delete_subnets()
        time.sleep(60)
        self.delete_vpcs()


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
