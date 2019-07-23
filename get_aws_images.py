import boto3
from datetime import datetime
import re
from operator import itemgetter

date = datetime.now().strftime('%Y%m%d%H%M%S')
# owner_ids = ['141808717104', ]
owner_ids = ['837727238323', '841869936221', '841258680906', '141808717104', '016951021795', '124890673580']


class GetImages(object):
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def descript_images(self, filters):
        response = self.ec2.describe_images(
            Filters=filters,
            # ImageIds=[
            #     'ami-0caeb068a98b44d18',
            # ],
        )
        # print(response)
        return response['Images']

    def get_image_info(self, filters):
        images_list = []
        images = self.descript_images(filters)
        for i in range(len(images)):
            create_time = images[i]['CreationDate']
            create_time = re.split(r'[T.]', str(create_time))
            create_time = create_time[0] + ' ' + create_time[1]
            create_time = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
            create_time = str(create_time)
            image_id = images[i]['ImageId']
            owner_id = images[i]['OwnerId']
            hypervisor = images[i]['Hypervisor']
            virtualization_type = images[i]['VirtualizationType']
            architecture = images[i]['Architecture']
            root_device_type = images[i]['RootDeviceType']
            try:
                ena_support = images[i]['EnaSupport']
                ena_support = str(ena_support)
            except Exception:
                ena_support = "None"
            try:
                sriov_net_support = images[i]['SriovNetSupport']
                sriov_net_support = str(sriov_net_support)
            except Exception:
                sriov_net_support = "None"
            name = images[i]['Name']
            description = images[i]['Description']
            if owner_id == '837727238323':
                name = re.split(r'/', str(name))[-1]
                name = re.sub(r'-\d{8}\.\d|-\d{8}', '', str(name))
            elif owner_id == '841869936221':
                name = re.sub(r'v\d{8}-', '', str(name))
            elif owner_id == '841258680906':
                name = re.sub(r'\d{8}-', '', str(name))
            elif owner_id == '141808717104':
                name = re.sub(r'\.\d{8}|\d{4}\.\d{2}\.\d+', '', str(name))
                name = re.sub(r'--|-\.', '-', str(name))
            elif owner_id == '016951021795':
                name = re.sub(r'-\d{4}\.\d{2}\.\d{2}', '', str(name))
            images_list.append(
                [image_id, owner_id, hypervisor, virtualization_type, architecture, root_device_type, ena_support,
                 sriov_net_support, name, description, create_time])
        images_list = sorted(images_list, key=itemgetter(8, 10), reverse=True)
        new_images_list = []
        for image in images_list:
            if len(new_images_list) == 0:
                new_images_list.append(image)
            else:
                name = new_images_list[-1][8]
                if image[8] != name:
                    new_images_list.append(image)
        f = open('aws_amis_list_%s.csv' % date, 'a+')
        line = ''
        for image_info in new_images_list:
            for j in range(len(image_info)):
                line = line + '"%s"' % image_info[j] + ','
            f.write(line + '\n')
            line = ''
        f.close()

    def main(self):
        f = open('aws_amis_list_%s.csv' % date, 'w')
        f.write(
            'ImageId,OwnerId,Hypervisor,VirtualizationType,Architecture,RootDeviceType,EnaSupport,SriovNetSupport,Name,Description,CreateTime' + '\n')
        f.close()
        for owner_id in owner_ids:
            filters = [
                {
                    'Name': 'owner-id',
                    'Values': [
                        owner_id
                    ]
                },
            ]
            self.get_image_info(filters)


if __name__ == '__main__':
    app = GetImages()
    app.main()
