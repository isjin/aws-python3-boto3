from function.aws_ec2 import AWSEC2
import json

class CreateEC2(object):
    def __init__(self):
        self.client = AWSEC2()
        self.ec2_config_path='config/instance.txt'

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def create_ec2(self):
        ec2_info =self.read_file(self.ec2_config_path)
        self.client.ec2_instance_create(ec2_info)


if __name__ == '__main__':
    app = CreateEC2()
    app.create_ec2()
