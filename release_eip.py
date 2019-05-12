from function.aws_ec2 import AWSEC2

instanceids = ['i-aaaaaa']
# instanceids = ['i-0526e82c2a702a757', 'i-014c4cef19cef30a6', 'i-0e1f7de89f1532b6b', 'i-00ac456d6b2508dfb']
# instanceids = ['i-09421013b67e02b6f','i-0769a4d0a1e22b23f','i-0f8b3df82161baf5f']

class ReleaseEIP(object):
    def __init__(self):
        self.client = AWSEC2()

    def get_instance_public_ip(self, instanceid):
        instance_info = self.client.ec2_instance_describe(instanceid)
        public_ip = instance_info['Instances'][0]['PublicIpAddress']
        return public_ip

    def get_public_ip_id(self, public_ip):
        eip_info = self.client.ec2_eip_describe(public_ip)
        eipid = eip_info['Addresses'][0]['AllocationId']
        return eipid

    def release_eip(self, instanceid):
        public_ip = self.get_instance_public_ip(instanceid)
        eipid = self.get_public_ip_id(public_ip)
        self.client.ec2_eip_disassociate_address(eipid)
        self.client.ec2_eip_release(eipid)

    def main(self):
        for instanceid in instanceids:
            self.release_eip(instanceid)


if __name__ == '__main__':
    app = ReleaseEIP()
    app.main()
