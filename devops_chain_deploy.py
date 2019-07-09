from function import aws_ec2
import json
import os
import time

# brandedgoods


key_pair = 'devopschaindemo'
record_path = 'config/devops_chain/devops_chain.log'


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.record = {}
        self.init_record()
        self.vpcid = self.record['vpcid']
        # self.vpcid = 'vpc-09bc1660'
        self.subnetid_1 = self.record['subnetid_1']
        # self.subnetid_1 = 'subnet-1af53661'
        self.sg_devopschain_application_id = self.record['sg_devopschain_application_id']
        self.igwid = self.record['igwid']
        # self.igwid = 'igw-69578f00'

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

    # def create_key_pair(self):
    #     self.ec2.ec2_key_pair_create(key_pair_uat)
    #     self.ec2.ec2_key_pair_create(key_pair_prod)

    def create_security_group(self):
        if self.sg_devopschain_application_id != "None":
            sg_devopschain_application_path = 'config/devops_chain/securitygroup_devopschain.txt'
            devopschain_application = self.read_file(sg_devopschain_application_path)
            devopschain_application['vpcid'] = self.vpcid
            if self.sg_devopschain_application_id == "None":
                self.sg_devopschain_application_id = self.ec2.ec2_security_group_create(devopschain_application)
            self.record['sg_devopschain_application_id'] = self.sg_devopschain_application_id

        sg_devopschain_application_inbound_path = 'config/devops_chain/sg_inbound_devopschain.txt'
        sg_devopschain_application_inbound = self.read_file(sg_devopschain_application_inbound_path)
        sg_devopschain_application_inbound['securitygroupid'] = self.sg_devopschain_application_id
        try:
            self.ec2.ec2_security_group_inbound_policies_add(sg_devopschain_application_inbound)
        except Exception as e:
            print(e.__str__())

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
        try:
            self.create_security_group()
            if 'instance_1_id' not in self.record.keys():
                instance_1_id = self.create_ec2('config/devops_chain/instance_1.txt')
                self.assign_eip(instance_1_id)
            if 'instance_2_id' not in self.record.keys():
                instance_2_id = self.create_ec2('config/devops_chain/instance_2.txt')
                self.record['instance_2_id'] = instance_2_id
                self.assign_eip(instance_2_id)
            if 'instance_3_id' not in self.record.keys():
                instance_3_id = self.create_ec2('config/devops_chain/instance_3.txt')
                self.record['instance_3_id'] = instance_3_id
                self.assign_eip(instance_3_id)
            # self.assign_eip('i-03786cc629160283b')
        except Exception as e:
            print(e.__str__())
            self.write_file()
        finally:
            self.write_file()


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
