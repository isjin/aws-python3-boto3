from function.aws_ec2 import AWSEC2


class SecurityGroup(object):
    def __init__(self):
        self.client = AWSEC2()
        self.sg_id = None

    def create_sg(self):
        sg_info = {
            'groupname': 'hrm-waf-bastion-sg',
            'description': 'hrm-waf-bastion-sg',
            'vpcid': 'vpc-03f41ad765358c055',
            'tags': [
                {
                    'Key': 'Name',
                    'Value': 'hrm-waf-bastion-sg'
                },
                {
                    'Key': 'System',
                    'Value': 'HRM'
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
