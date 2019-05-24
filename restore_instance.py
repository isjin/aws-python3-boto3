from function.aws_ec2 import AWSEC2

snapshotid = 'snap-07a95ed40f6a4e28a'
volume_snapshotid='snap-04277b0124adf3fb5'

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
        self.instance_az=None
        self.instance_sgs = []
        self.instance_virtualization_type=None

    def get_snapshot_info(self):
        snapshot_info = self.client.ec2_snapshot_describe(snapshotid)
        self.volumeid = snapshot_info['VolumeId']
        self.volumesize = snapshot_info['VolumeSize']


    def get_volume_info(self):
        volume_info = self.client.ec2_volume_describe(self.volumeid)
        self.devicename = volume_info['Attachments'][0]['Device']
        self.instanceid = volume_info['Attachments'][0]['InstanceId']
        self.volumetype = volume_info['VolumeType']

    def get_instance_info(self):
        instance_info = self.client.ec2_instance_describe(self.instanceid)
        self.instance_type = instance_info['Instances'][0]['InstanceType']
        self.instance_subnetid = instance_info['Instances'][0]['SubnetId']
        self.instance_keyname = instance_info['Instances'][0]['KeyName']
        self.instance_tags = instance_info['Instances'][0]['Tags']
        self.instance_virtualization_type = instance_info['Instances'][0]['VirtualizationType']
        self.instance_az=instance_info['Instances'][0]['Placement']['AvailabilityZone']
        for sg in instance_info['Instances'][0]['SecurityGroups']:
            self.instance_sgs.append(sg['GroupId'])

    def register_image(self):
        snapshot_info = {
            'DeviceName': self.devicename,
            'Description': snapshotid,
            'Name': snapshotid,
            'SnapshotId': snapshotid,
            'RootDeviceName': self.devicename,
            'VirtualizationType': self.instance_virtualization_type,
            'VolumeType': self.volumetype,
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

    def attach_volume(self):
        volume_info={
            'AvailabilityZone':self.instance_az,
            'Size':self.volumesize,
            'SnapshotId':volume_snapshotid,
            'VolumeType':self.volumetype,
            'Tags':self.instance_tags,
        }
        volume_id=self.client.ec2_volume_create(volume_info)
        attach_info={
            'Device':'xvdb',
            'InstanceId':self.instanceid,
            'VolumeId':volume_id,
        }
        self.client.ec2_volume_attach(attach_info)


    def main(self):
        self.get_snapshot_info()
        self.get_volume_info()
        self.get_instance_info()
        self.launch_instance()
        if volume_snapshotid !='':
            self.attach_volume()



if __name__ == '__main__':
    app = RestoreInstance()
    app.main()
    # app.get_snapshot_info()
    # app.get_volume_info()
    # app.get_instance_info()
