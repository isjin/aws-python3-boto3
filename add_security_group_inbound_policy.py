from function.aws_ec2 import AWSEC2

app = AWSEC2()

# data = app.ec2_security_group_describe('sg-0a97d9150f2dfb4a8')
# print(data)
sg_application_id = 'sg-0a97d9150f2dfb4a8'
sg_application_inbound = {
    'securitygroupid': '{sgid}',
    'policy': [
        {
            'FromPort': 22,
            'IpProtocol': 'tcp',
            # 'IpRanges': [
            #     {
            #         'CidrIp': '120.31.137.144/29',
            #         'Description': 'New Bund guest wifi'
            #     },
            # ],
            'ToPort': 22,
            'UserIdGroupPairs': [
                {
                    'Description': 'python',
                    'GroupId': sg_application_id,
                },
            ]
        },
        {
            'FromPort': 3389,
            'IpProtocol': 'tcp',
            # 'IpRanges': [
            #     {
            #         'CidrIp': '10.1.1.0/29',
            #         'Description': 'New Bund guest wifi'
            #     },
            # ],
            'ToPort': 3389,
            'UserIdGroupPairs': [
                {
                    'Description': 'python',
                    'GroupId': sg_application_id,
                },
            ]
        },
        {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            # 'IpRanges': [
            #     {
            #         'CidrIp': '10.1.1.0/29',
            #         'Description': 'New Bund guest wifi'
            #     },
            # ],
            'ToPort': 80,
            'UserIdGroupPairs': [
                {
                    'Description': 'python',
                    'GroupId': sg_application_id,
                },
            ]
        },
    ]
}
app.ec2_security_group_inbound_policies_add(sg_application_inbound)
