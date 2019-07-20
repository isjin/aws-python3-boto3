from function import aws_ec2, aws_iam, aws_cloudformation, aws_ecs, aws_ecr, aws_cloudwatch
import json
import os
import time

key_pair = 'devopschaindemo'
resources_path = 'config/test/test.log'


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.iam = aws_iam.AWSIAM()
        self.cf = aws_cloudformation.AWSCloudFormation()
        self.ecs = aws_ecs.AWSECS()
        self.ecr = aws_ecr.AWSECR()
        self.cloudwatch = aws_cloudwatch.AWSCloudWatch()
        self.resources = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resources_path):
            f = open(resources_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def write_file(self):
        f = open(resources_path, 'w')
        f.write(json.dumps(self.resources))
        f.close()

    def delete_vpcs(self):
        print("Start to delete vpcs")
        for key in list(self.resources['vpcs'].keys()):
            try:
                self.ec2.ec2_vpc_delete(self.resources['vpcs'][key])
                del self.resources['vpcs'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete vpcs are finished.")

    def delete_subnets(self):
        print("Start to delete subnets")
        for key in list(self.resources['subnets'].keys()):
            try:
                self.ec2.ec2_subnet_delete(self.resources['subnets'][key])
                del self.resources['subnets'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete subnets are finished.")

    def delete_igws(self):
        print("Start to delete internet gateways")
        for key in list(self.resources['igws'].keys()):
            try:
                igw_id = self.resources['igws'][key]
                igw_info = self.ec2.ec2_internet_gateway_describe(igw_id)
                attachments_length = len(igw_info[0]['Attachments'])
                if attachments_length > 0:
                    vpcid = igw_info[0]['Attachments'][0]['VpcId']
                    self.ec2.ec2_internet_gateway_detach(igw_id, vpcid)
                self.ec2.ec2_internet_gateway_delete(igw_id)
                del self.resources['igws'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete internet gateways are finished.")

    def delete_keypairs(self):
        print("Start to delete keypairs")
        for key in list(self.resources['keypairs'].keys()):
            try:
                self.ec2.ec2_key_pair_delete(self.resources['keypairs'][key])
                del self.resources['keypairs'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete keypairs are finished.")

    def delete_security_groups(self):
        print("Start to delete security groups")
        for key in list(self.resources['security_groups'].keys()):
            try:
                self.ec2.ec2_security_group_delete(self.resources['security_groups'][key])
                del self.resources['security_groups'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete security groups are finished.")

    def delete_roles(self):
        print("Start to delete roles")
        for key in list(self.resources['roles'].keys()):
            try:
                if key in self.resources['instance_profiles'].keys():
                    self.iam.iam_role_to_instance_profile_remove(self.resources['instance_profiles'][key]['name'],
                                                                 self.resources['roles'][key]['name'])
                    self.iam.iam_instance_profile_delete(self.resources['instance_profiles'][key]['name'])
                    del self.resources['instance_profiles'][key]
                    self.write_file()
                for policy_arn in self.resources['policies'][key]:
                    self.iam.iam_role_policy_detach(self.resources['roles'][key]['name'], policy_arn)
                self.iam.iam_role_delete(self.resources['roles'][key]['name'])
                del self.resources['policies'][key]
                self.write_file()
                del self.resources['roles'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())

        print("Delete roles are finished.")

    def delete_cloudformations(self):
        print("Start to delete cloudformations")
        for key in list(self.resources['cloudformations'].keys()):
            stack_name = self.resources['cloudformations'][key]
            try:
                self.cf.cloudformation_stack_delete(stack_name)
                while True:
                    try:
                        self.cf.cloudformation_stack_describe(stack_name)
                        time.sleep(5)
                    except Exception:
                        print("Deleting cloudformation stack %s." % stack_name)
                        break
                del self.resources['cloudformations'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete cloudformations are finished.")

    def delete_ecs_clusters(self):
        print("Start to delete ECS")
        for key in list(self.resources['ecs_clusters'].keys()):
            while True:
                try:
                    self.ecs.ecs_cluster_delete(self.resources['ecs_clusters'][key])
                    del self.resources['ecs_clusters'][key]
                    self.write_file()
                    break
                except Exception as e:
                    print(e.__str__())
                    time.sleep(15)
        print("Delete ECS is finished.")

    def delete_ec2_instances(self):
        print("Start to delete EC2")
        for key in list(self.resources['eips'].keys()):
            try:
                eipid = self.resources['eips'][key]
                association_id = self.ec2.ec2_eip_allocation_id_describe(eipid)['AssociationId']
                self.ec2.ec2_eip_disassociate_address(association_id)
                self.ec2.ec2_eip_release_allocation_id(eipid)
                del self.resources['eips'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())

        for key in list(self.resources['ec2_instances'].keys()):
            try:
                instance_id = self.resources['ec2_instances'][key]
                volumes_info = self.ec2.ec2_instance_describe(instance_id)['Instances'][0]['BlockDeviceMappings']
                self.ec2.ec2_instance_delete(instance_id)
                for volume_info in volumes_info:
                    device_name = volume_info['DeviceName']
                    if device_name not in ['/dev/sda1', '/dev/xvda']:
                        volume_id = volume_info['Ebs']['VolumeId']
                        self.ec2.ec2_volume_delete(volume_id)
                del self.resources['ec2_instances'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete EC2 is finished.")

    def delete_ecr_repositories(self):
        print("Start to delete ECR repositories")
        for key in list(self.resources['ecr_repositories'].keys()):
            try:
                self.ecr.repository_delete(self.resources['ecr_repositories'][key])
                del self.resources['ecr_repositories'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
        print("Delete ECR is finished.")

    def main(self):
        self.delete_ec2_instances()
        self.delete_cloudformations()
        self.delete_ecs_clusters()
        self.delete_ecr_repositories()
        self.delete_roles()
        self.delete_security_groups()
        self.delete_keypairs()
        self.delete_igws()
        self.delete_subnets()
        time.sleep(60)
        self.delete_vpcs()


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
