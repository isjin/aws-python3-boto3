from function.aws_elb import AWSELB

tags = [
    {
        'Key': 'System',
        'Value': 'BPM'
    },
    {
        'Key': 'System type',
        'Value': 'PROD'
    },
]


class ALB(object):
    def __init__(self):
        self.client = AWSELB()
        self.alb_arn = None
        self.target_group_arn = None

    def create_alb(self):
        elb_info = {
            'Name': 'bpm-prod-app-external-alb',
            'Subnets': ['subnet-0c2085fe6974c518c', 'subnet-05c6866bcc1315c27'],
            'SecurityGroups': ['sg-0845a9efb32232a8b', ],
            'Scheme': 'internet-facing',
            'Tags': [
                {
                    'Key': 'System',
                    'Value': 'BPM'
                },
                {
                    'Key': 'System type',
                    'Value': 'PROD'
                },
            ],
            'Type': 'application',

        }
        self.alb_arn = self.client.elbv2_load_balancer_create(elb_info)
        self.client.elbv2_tags_create(self.alb_arn, tags)

    def create_target_group(self):
        # target_group_info = {
        #     'Name': 'bpm-prod-app-external',
        #     'Protocol': 'HTTP',
        #     'Port': 80,
        #     'VpcId': 'vpc-0a01461d0036a5c13',
        #     'TargetType': 'instance',
        # }
        target_group_info = {
            'Name': 'bpm-prod-app-external-443',
            'Protocol': 'HTTP',
            'Port': 443,
            'VpcId': 'vpc-0a01461d0036a5c13',
            'TargetType': 'instance',
        }
        self.target_group_arn = self.client.elbv2_target_group_create(target_group_info)
        self.client.elbv2_tags_create(self.target_group_arn, tags)

    def register_target(self):
        # target_info = {
        #     'TargetGroupArn': self.target_group_arn,
        #     'Targets': [
        #         {
        #             'Id': 'i-0b9a4107702590309',
        #             'Port': 80,
        #         },
        #         {
        #             'Id': 'i-0a162b830a0a09307',
        #             'Port': 80,
        #         },
        #     ],
        # }
        target_info = {
            'TargetGroupArn': self.target_group_arn,
            'Targets': [
                {
                    'Id': 'i-0b9a4107702590309',
                    'Port': 443,
                },
                {
                    'Id': 'i-0a162b830a0a09307',
                    'Port': 443,
                },
            ],
        }
        self.client.elbv2_target_register(target_info)

    def create_listener(self):
        # listeners_info = {
        #     'LoadBalancerArn': self.alb_arn,
        #     'Protocol': 'HTTP',
        #     'Port': 80,
        #     'Certificates': [
        #         # {
        #         #     'CertificateArn': 'string',
        #         #     'IsDefault': True | False
        #         # },
        #     ],
        #     'Type': 'forward',
        #     'TargetGroupArn': self.target_group_arn,
        # }
        listeners_info = {
            'LoadBalancerArn': self.alb_arn,
            'Protocol': 'HTTP',
            'Port': 443,
            'Certificates': [
                # {
                #     'CertificateArn': 'string',
                #     'IsDefault': True | False
                # },
            ],
            'Type': 'forward',
            'TargetGroupArn': self.target_group_arn,
        }
        self.client.elbv2_listeners_create(listeners_info)

    def main(self):
        # self.create_alb()
        self.create_target_group()
        self.register_target()
        self.create_listener()


if __name__ == '__main__':
    app = ALB()
    app.main()
