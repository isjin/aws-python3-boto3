import boto3
from datetime import datetime, timedelta

##早上2点，7天

ec2_client = boto3.client('ec2')

# today = datetime.now()+timedelta(days=8)
today = datetime.now()


def lambda_handler(event, context):
    for instanceid in get_instances():
        create_snapshot(instanceid)


def get_instances():
    instanceids = []
    for instance_info in ec2_instances_describe():
        instanceids.append(instance_info['Instances'][0]['InstanceId'])
    return instanceids


def ec2_instances_describe():
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:System type',
                'Values': [
                    'PROD',
                ]
            },
            {
                'Name': 'tag:System',
                'Values': [
                    'AMP',
                ]
            },

        ],
    )
    return response['Reservations']


def create_snapshot(instanceid):
    instance_info = ec2_instance_describe(instanceid)['Instances'][0]
    description = ''
    tags = instance_info['Tags']
    for tag in tags:
        if tag['Key'] == 'Name':
            description = tag['Value']
            tag['Value'] = tag['Value'] + '_' + today.strftime('%Y%m%d')
    volumes_info = instance_info['BlockDeviceMappings']
    for volume_info in volumes_info:
        volumeid = volume_info['Ebs']['VolumeId']
        device = volume_info['DeviceName']
        volume_description = description + '_' + device
        print(volumeid, volume_description, tags)
        delete_snapshot(volumeid)
        ec2_snapshot_create(volumeid, volume_description, tags)


def ec2_instance_describe(instanceid):
    response = ec2_client.describe_instances(
        InstanceIds=[instanceid, ],
    )
    return response['Reservations'][0]


def ec2_snapshot_create(volumeid, description, tags):
    response = ec2_client.create_snapshot(
        Description=description,
        VolumeId=volumeid,
    )
    print(response)
    snapshotid = response['SnapshotId']
    ec2_tags_create(snapshotid, tags)


def ec2_tags_create(resource_id, tags):
    response = ec2_client.create_tags(
        Resources=[
            resource_id,
        ],
        Tags=tags
    )
    print(response)


def delete_snapshot(volume_id):
    snapshot_infos = ec2_snapshot_describe(volume_id)
    for snapshot_info in snapshot_infos:
        # print(snapshot_info)
        snapshotid = snapshot_info['SnapshotId']
        snapshot_date = snapshot_info['StartTime']
        snapshot_date = datetime.strftime(snapshot_date, '%Y%m%d')
        snapshot_date = datetime.strptime(snapshot_date, '%Y%m%d')
        delta = (today - snapshot_date).days
        if delta > 6:
            ec2_snapshot_delete(snapshotid)
    return


def ec2_snapshot_describe(volume_id):
    response = ec2_client.describe_snapshots(
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [volume_id, ]
            },
        ],
        OwnerIds=[
            '168677335524',
        ],
    )
    return response['Snapshots']


def ec2_snapshot_delete(snapshotid):
    response = ec2_client.delete_snapshot(
        SnapshotId=snapshotid,
    )
    print(response)
