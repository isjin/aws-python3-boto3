from function.aws_ec2 import AWSEC2


class SecurityGroup(object):
    def __init__(self):
        self.client = AWSEC2()
        self.sg_id = None

    def create_sg(self):
        groupname='amp-waf-bastion-sg'
        sg_info = {
            'groupname': groupname,
            'description': groupname,
            'vpcid': 'vpc-07c4e7ecc9ef08e1e',
            'tags': [
                {
                    'Key': 'Name',
                    'Value': groupname
                },
                {
                    'Key': 'System',
                    'Value': 'BPM'
                },
            ]
        }
        self.sg_id = self.client.ec2_security_group_create(sg_info)

    def add_inboud_policy(self):
        inbound_info = {
            'securitygroupid': self.sg_id,
            'policy': [
                {
                    'IpProtocol': '-1',
                    'IpRanges': [
                        {
                            'CidrIp': '10.20.2.6/32',
                            'Description': 'waf bastion'
                        },
                    ]
                },
            ],
        }
        self.client.ec2_security_group_inbound_policies_add(inbound_info)

    def main(self):
        self.create_sg()
        self.add_inboud_policy()


if __name__ == '__main__':
    app = SecurityGroup()
    app.main()
