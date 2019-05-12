from function.aws_ec2 import AWSEC2

snapshotid = 'snap-01c0184d0168d6253'


class RestoreInstance(object):
    def __init__(self):
        self.client = AWSEC2()
        self.volumetype = None
        self.volumesize = None
        self.volumeid = None
        self.instance_type = None
        self.devicename = None
        self.instanceid = None
        self.instance_subnetid = None
        self.instance_keyname = None
        self.instance_tags = None
        self.instance_sgs = []

    def get_snapshot_info(self):
        snapshot_info = self.client.ec2_snapshot_describe(snapshotid)
        self.volumeid = snapshot_info['VolumeId']
        self.volumesize = snapshot_info['VolumeSize']
        self.volumetype = snapshot_info['VolumeType']

    def get_volume_info(self):
        volume_info = self.client.ec2_volume_describe(self.volumeid)
        self.devicename = volume_info['Attachments'][0]['Device']
        self.instanceid = volume_info['Attachments'][0]['InstanceId']

    def get_instance_info(self):
        instance_info = self.client.ec2_instance_describe(self.instanceid)
        self.instance_type = instance_info['Instances'][0]['InstanceType']
        self.instance_subnetid = instance_info['Instances'][0]['SubnetId']
        self.instance_keyname = instance_info['Instances'][0]['KeyName']
        self.instance_tags = instance_info['Instances'][0]['Tags']
        for sg in instance_info['Instances'][0]['SecurityGroups']:
            self.instance_sgs.append(sg['GroupId'])

    def register_image(self):
        snapshot_info = {
            'DeviceName': self.devicename,
            'Description': snapshotid,
            'Name': snapshotid,
            'SnapshotId': snapshotid,
            'RootDeviceName': self.devicename,
        }
        imageid = self.client.ec2_register_image(snapshot_info)
        return imageid

    def launch_instance(self):
        instance_info = {
            'BlockDeviceMappings': [
                {
                    'DeviceName': self.devicename,
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': self.volumesize,
                        'VolumeType': self.volumetype,
                    },
                },
            ],
            'ImageId': self.register_image(),
            'InstanceType': self.instance_type,
            'maxcount': 1,
            'mincount': 1,
            'KeyName': self.instance_keyname,
            'SecurityGroupIds': self.instance_sgs,
            'SubnetId': self.instance_subnetid,
            'TagSpecifications': [
                {
                    'ResourceType': 'instance',
                    'Tags': self.instance_tags
                },
                {
                    'ResourceType': 'volume',
                    'Tags': self.instance_tags
                },
            ],
        }
        self.client.ec2_instance_create(instance_info)

    def main(self):
        self.get_snapshot_info()
        self.get_volume_info()
        self.get_instance_info()
        self.register_image()
        self.launch_instance()


if __name__ == '__main__':
    app = RestoreInstance()
    app.main()
    # app.get_snapshot_info()
    # app.get_volume_info()
    # app.get_instance_info()
