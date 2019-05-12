from function.aws_ec2 import AWSEC2

# import sys

# instanceid=sys.argv[1]
# instanceids = ['i-0a162b830a0a09307', 'i-0b9a4107702590309', 'i-09421013b67e02b6f', 'i-0769a4d0a1e22b23f','i-0f8b3df82161baf5f']
# instanceids = ['i-0526e82c2a702a757', 'i-014c4cef19cef30a6', 'i-0e1f7de89f1532b6b', 'i-00ac456d6b2508dfb']
instanceids = ['i-09421013b67e02b6f','i-0769a4d0a1e22b23f','i-0f8b3df82161baf5f']


class ASSIGNEIP(object):
    def __init__(self):
        self.client = AWSEC2()

    def get_instance_name(self, instanceid):
        instance_info = self.client.ec2_instance_describe(instanceid)
        tags = instance_info['Instances'][0]['Tags']
        instance_name = ''
        for tag in tags:
            if tag['Key'] == "Name":
                instance_name = tag['Value']
                break
        return instance_name

    def create_eip(self, instance_name):
        tags = [
            {
                'Key': 'Name',
                'Value': instance_name
            },
            {
                'Key': 'System',
                'Value': 'BPM'
            },
        ]
        eipid = self.client.ec2_eip_allocate(tags)
        return eipid

    def assign_eip(self, instanceid):
        instance_name = self.get_instance_name(instanceid)
        eipid = self.create_eip(instance_name)
        associate_info = {
            'AllocationId': eipid,
            # 'AllocationId': 'eipalloc-0e0be917bbb463d1c',
            'InstanceId': instanceid,
        }
        self.client.ec2_eip_associate_address(associate_info)

    def main(self):
        for instanceid in instanceids:
            self.assign_eip(instanceid)


if __name__ == '__main__':
    app = ASSIGNEIP()
    app.main()
