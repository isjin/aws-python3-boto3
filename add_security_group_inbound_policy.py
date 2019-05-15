from function.aws_ec2 import AWSEC2

app = AWSEC2()

# data = app.ec2_security_group_describe('sg-0a97d9150f2dfb4a8')
# print(data)
sg_application_id = 'sg-08ce92b068895a67b'
sg_application_inbound = {
  "securitygroupid":sg_application_id,
  "policy":[
    {
      "IpProtocol":"-1",
      "IpRanges":[
        {
          "CidrIp":"120.31.137.144/29",
          "Description":"New Bund guest wifi"
        },
        {
          "CidrIp":"192.168.1.0/24",
          "Description":"New Bund guest wifi"
        }
      ]
    }
  ]
}
app.ec2_security_group_inbound_policies_add(sg_application_inbound)
