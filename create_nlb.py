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


class NLB(object):
    def __init__(self):
        self.client = AWSELB()
        self.nlb_arn = None
        self.target_group_arn = None

    def create_nlb(self):
        elb_info = {
            'Name': 'bpm-prod-test',
            'Subnets': ['subnet-0c2085fe6974c518c', 'subnet-05c6866bcc1315c27'],
            'SecurityGroups': [],
            'Scheme': 'internal',
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
            'Type': 'network',

        }
        self.nlb_arn = self.client.elbv2_load_balancer_create(elb_info)
        self.client.elbv2_tags_create(self.nlb_arn, tags)

    def create_target_group(self):
        target_group_info = {
            'Name': 'bpm-prod-app-test',
            'Protocol': 'TCP',
            'Port': 22,
            'VpcId': 'vpc-0a01461d0036a5c13',
            'TargetType': 'instance',
        }
        self.target_group_arn = self.client.elbv2_target_group_create(target_group_info)
        self.client.elbv2_tags_create(self.target_group_arn, tags)

    def register_target(self):
        target_info = {
            'TargetGroupArn': self.target_group_arn,
            'Targets': [
                {
                    'Id': 'i-03a1c9ed8eb9b637e',
                    'Port': 22,
                },
                {
                    'Id': 'i-0a162b830a0a09307',
                    'Port': 22,
                },
            ],
        }
        self.client.elbv2_target_register(target_info)

    def create_listener(self):
        listeners_info = {
            'LoadBalancerArn': self.nlb_arn,
            'Protocol': 'TCP',
            'Port': 22,
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
        self.create_nlb()
        self.create_target_group()
        self.register_target()
        self.create_listener()


if __name__ == '__main__':
    app = NLB()
    app.main()
