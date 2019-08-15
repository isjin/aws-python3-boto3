from function.aws_ec2 import AWSEC2
import json


def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)
    return data

app = AWSEC2()


# data = app.ec2_security_group_describe('sg-0a97d9150f2dfb4a8')
# print(data)
sg_application_id = 'sg-0e5a63e0254abc056'
sg_info = app.ec2_security_group_describe(sg_application_id)
inboud_info = {}
inboud_info['policy'] = sg_info['IpPermissions']
inboud_info["securitygroupid"] = sg_application_id
app.ec2_security_group_inbound_policies_revoke(inboud_info)

sg_inbound_path = 'config/JLR/waf/sg_inbound-waf-cil-alb.txt'
sg_inbound = read_file(sg_inbound_path)
sg_inbound['securitygroupid'] = sg_application_id
try:
    app.ec2_security_group_inbound_policies_add(sg_inbound)
except Exception as e:
    print(e.__str__())
