from function.aws_ec2 import AWSEC2

instanceids = ['i-0c26f53bf5fa21034', 'i-019aaaf91665fc6d2', 'i-088bb3ef6dc4e9230']


class SecurityGroup(object):
    def __init__(self):
        self.client = AWSEC2()
        self.instanceid = 'i-0b6e8a971b56e3475'
        self.new_sg_id = 'sg-0ea1b2546ff3fedb2'

    def get_sg_ids(self, instanceid):
        instance_info = self.client.ec2_instance_describe(instanceid)
        sgs_info = (instance_info['Instances'][0]['NetworkInterfaces'][0]['Groups'])
        sg_ids = []
        for sg_info in sgs_info:
            sg_ids.append(sg_info['GroupId'])
        return sg_ids

    def modify_instance_sg(self, instanceid):
        sg_ids = self.get_sg_ids(instanceid)
        if self.new_sg_id not in sg_ids:
            sg_ids.append(self.new_sg_id)
        info = {
            'Groups': sg_ids,
            'InstanceId': instanceid
        }
        self.client.ec2_security_group_modify(info)

    def main(self):
        for instanceid in instanceids:
            self.modify_instance_sg(instanceid)


if __name__ == '__main__':
    app = SecurityGroup()
    app.main()
