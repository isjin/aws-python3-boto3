from function.aws_ec2 import AWSEC2
from function.aws_elb import AWSELB

tags = [
    {
        'Key': 'System',
        'Value': 'WAF'
    }
]


class ALB(object):
    def __init__(self):
        self.elb = AWSELB()
        self.ec2 = AWSEC2()
        self.alb_arn = 'arn:aws-cn:elasticloadbalancing:cn-north-1:168677335524:loadbalancer/app/waf-app-internet-gw-alb/a00f07d65d31be5b'
        self.target_group_arn = None
        # self.target_group_arn = 'arn:aws-cn:elasticloadbalancing:cn-north-1:168677335524:targetgroup/waf-app-internet-9009/25ce751a0b2b58c5'
        # self.listener_arn = None
        self.listener_arn = 'arn:aws-cn:elasticloadbalancing:cn-north-1:168677335524:listener/app/waf-app-internet-gw-alb/a00f07d65d31be5b/a7b044c8ab34f53a'
        self.sg_waf_gateway = 'sg-0c0107d24a5c2c6ef'
        self.sg_alb = 'sg-0f2cee09386bcea89'
        self.source_port = 9009
        self.dest_port = 9009

    def create_target_group(self):
        target_group_info = {
            'Name': 'waf-app-internet-brandedgoods',
            'Protocol': 'HTTP',
            'Port': self.dest_port,
            'VpcId': 'vpc-06e5e4b230542de7b',
            'TargetType': 'instance',
        }
        self.target_group_arn = self.elb.elbv2_target_group_create(target_group_info)
        self.elb.elbv2_tags_create(self.target_group_arn, tags)

    def register_target(self):
        target_instance = {
            'TargetGroupArn': self.target_group_arn,
            'Targets': [
                {
                    'Id': 'i-02d6870334c830e3e',
                    'Port': self.dest_port,
                },
                {
                    'Id': 'i-080fbec0b131b8425',
                    'Port': self.dest_port,
                },
            ],
        }
        self.elb.elbv2_target_register(target_instance)

    def create_listener(self):
        listeners_info = {
            'LoadBalancerArn': self.alb_arn,
            'Protocol': 'HTTPS',
            'Port': self.source_port,
            'Certificates': [
                {
                    'CertificateArn': 'arn:aws-cn:iam::168677335524:server-certificate/jlrinfo_cn',
                    # 'IsDefault': True | False
                },
                # {
                #     'CertificateArn': 'arn:aws-cn:iam::168677335524:server-certificate/jaguarlandrover_cn',
                #     # 'IsDefault': True | False
                # },
            ],
            'Type': 'forward',
            'TargetGroupArn': self.target_group_arn,
        }
        self.listener_arn = self.elb.elbv2_listener_create(listeners_info)

    def sg_waf_gateway_add(self):
        inbound_info = {
            'securitygroupid': self.sg_waf_gateway,
            'policy': [
                {
                    'FromPort': self.dest_port,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                        },
                    ],
                    'ToPort': self.dest_port,
                },
            ],
        }
        self.ec2.ec2_security_group_inbound_policies_add(inbound_info)

    def sg_alb_add(self):
        inbound_info = {
            'securitygroupid': self.sg_alb,
            'policy': [
                {
                    'FromPort': self.source_port,
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': '10.20.2.0/24',
                            'Description': 'WAF',
                        },
                    ],
                    'ToPort': self.source_port,
                },
            ],
        }
        self.ec2.ec2_security_group_inbound_policies_add(inbound_info)

    def create_rule(self):
        listener_arn = self.listener_arn
        rule_info = {
            'ListenerArn': listener_arn,
            'Conditions': [
                {
                    "Field": "host-header",
                    "Values": [
                        "baidu.com"
                    ]
                }
            ],
            'Priority': 1,
            'Actions': [
                {
                    'Type': 'forward',
                    'TargetGroupArn': self.target_group_arn,
                    'Order': 2,
                }
            ],
        }
        self.elb.elbv2_rule_create(rule_info)

    def main(self):
        self.create_target_group()
        self.register_target()
        # self.create_listener()
        self.create_rule()
        # self.sg_waf_rule_add()
        # self.sg_alb_add()


if __name__ == '__main__':
    app = ALB()
    app.main()

