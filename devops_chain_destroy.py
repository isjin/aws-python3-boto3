from function import aws_ec2,aws_iam
import json
import os
import time

# brandedgoods


key_pair = 'devopschaindemo'
record_path = 'config/devops_chain/devops_chain2.log'


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.iam=aws_iam.AWSIAM()
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
        for key in list(self.record['vpcs'].keys()):
            try:
                self.ec2.ec2_vpc_delete(self.record['vpcs'][key])
            except Exception as e:
                print(e.__str__())
            del self.record['vpcs'][key]
            self.write_file()

    def delete_subnets(self):
        for key in list(self.record['subnets'].keys()):
            try:
                self.ec2.ec2_subnet_delete(self.record['subnets'][key])
            except Exception as e:
                print(e.__str__())
            del self.record['subnets'][key]
            self.write_file()

    def delete_igws(self):
        for key in list(self.record['igws'].keys()):
            try:
                vpcid = \
                self.ec2.ec2_internet_gateway_describe(self.record['igws'][key])['InternetGateways'][0]['Attachments'][
                    0]['VpcId']
                self.ec2.ec2_internet_gateway_detach(self.record['igws'][key], vpcid)
                self.ec2.ec2_internet_gateway_delete(self.record['igws'][key])
            except Exception as e:
                print(e.__str__())
            del self.record['igws'][key]
            self.write_file()

    def delete_keypair(self):
        for key in list(self.record['keypairs'].keys()):
            try:
                self.ec2.ec2_key_pair_delete(self.record['keypairs'][key])
            except Exception as e:
                print(e.__str__())
            del self.record['keypairs'][key]
            self.write_file()

    def delete_security_groups(self):
        for key in list(self.record['security_groups'].keys()):
            try:
                self.ec2.ec2_security_group_delete(self.record['security_groups'][key])
            except Exception as e:
                print(e.__str__())
            del self.record['security_groups'][key]
            self.write_file()

    def delete_role(self):
        for key in list(self.record['roles'].keys()):
            try:
                if key in self.record['instance_profiles'].keys():
                    self.iam.iam_role_to_instance_profile_remove(self.record['instance_profiles'][key],self.record['roles'][key])
                    self.iam.iam_instance_profile_delete(self.record['instance_profiles'][key])
                    del self.record['instance_profiles'][key]
                    self.write_file()
                for policy_arn in self.record['policies'][key]:
                    self.iam.iam_role_policy_detach(self.record['roles'][key],policy_arn)
                self.iam.iam_role_delete(self.record['roles'][key])
                del self.record['policies'][key]
                self.write_file()
            except Exception as e:
                print(e.__str__())
            del self.record['roles'][key]
            self.write_file()


    def main(self):
        self.delete_role()
        # self.delete_security_groups()
        # self.delete_keypair()
        # self.delete_igws()
        # self.delete_subnets()
        # self.delete_vpcs()


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
