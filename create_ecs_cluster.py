from function import aws_ec2, aws_iam, aws_cloudformation, aws_ecs
import json
import os
import time

key_pair = 'devopschaindemo'
record_path = 'config/devops_chain/devops_chain3.log'


class ECSDeploy(object):
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

    def main(self):
        ecs_keyname = 'ecs_test'
        if ecs_keyname not in self.record['ecs'].keys():
            self.ecs.ecs_cluster_create(ecs_keyname)
            self.record['ecs'][ecs_keyname] = ecs_keyname
            self.write_file()
        ec2_instance_ecs1_path = 'config/devops_chain/devops_chain_instance_ecs1.txt'
        ec2_instance_ecs1_info = self.read_file(ec2_instance_ecs1_path)
        ec2_instance_ecs1_info['SecurityGroupIds'] = [self.record['security_groups']['devops_chain_sg_devopschain']]
        ec2_instance_ecs1_info['SubnetId'] = self.record['subnets']['devops_chain_subnet_1a']
        ec2_instance_ecs1_keyname = 'ecs-test-ec2-1'
        if ec2_instance_ecs1_keyname not in self.record['ec2_instances'].keys():
            self.create_ec2(ec2_instance_ecs1_info, ec2_instance_ecs1_keyname)

        ec2_instance_ecs2_path = 'config/devops_chain/devops_chain_instance_ecs2.txt'
        ec2_instance_ecs2_info = self.read_file(ec2_instance_ecs2_path)
        ec2_instance_ecs2_info['SecurityGroupIds'] = [self.record['security_groups']['devops_chain_sg_devopschain']]
        ec2_instance_ecs2_info['SubnetId'] = self.record['subnets']['devops_chain_subnet_1a']
        ec2_instance_ecs2_keyname = 'ecs-test-ec2-2'
        if ec2_instance_ecs2_keyname not in self.record['ec2_instances'].keys():
            self.create_ec2(ec2_instance_ecs1_info, ec2_instance_ecs2_keyname)

        ec2_instance_windows_path = 'config/devops_chain/devops_chain_instance_windows.txt'
        ec2_instance_windows_info = self.read_file(ec2_instance_windows_path)
        ec2_instance_windows_info['SecurityGroupIds'] = [
            self.record['security_groups']['devops_chain_sg_devopschain'], ]
        ec2_instance_windows_info['SubnetId'] = self.record['subnets']['devops_chain_subnet_1a']
        ec2_instance_windows_keyname = 'windows'
        if ec2_instance_windows_keyname not in self.record['ec2_instances'].keys():
            self.create_ec2(ec2_instance_windows_info, ec2_instance_windows_keyname)


if __name__ == '__main__':
    app = ECSDeploy()
    app.main()
