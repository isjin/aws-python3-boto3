from function import aws_ec2


class DeleteEC2(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()

    def main(self, instance_id):
        instance_info = self.ec2.ec2_instance_describe(instance_id)['Instances'][0]
        volumes_info = instance_info['BlockDeviceMappings']
        # release public IP
        if 'PublicIpAddress' in instance_info.keys():
            public_ip = instance_info['PublicIpAddress']
            eip_info = self.ec2.ec2_eip_public_ip_describe(public_ip)
            association_id = eip_info['Addresses'][0]['AssociationId']
            allocation_id = eip_info['Addresses'][0]['AllocationId']
            self.ec2.ec2_eip_disassociate_address(association_id)
            self.ec2.ec2_eip_release(allocation_id)
        # delete ec2 instance
        self.ec2.ec2_instance_delete(instance_id)

        # delete volumes
        for volume_info in volumes_info:
            device_name = volume_info['DeviceName']
            if device_name not in ['/dev/sda1', '/dev/xvda']:
                volume_id = volume_info['Ebs']['VolumeId']
                self.ec2.ec2_volume_delete(volume_id)


if __name__ == '__main__':
    app = DeleteEC2()
    app.main('i-020147c43898aa481')
