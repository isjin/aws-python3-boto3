import boto3


def lambda_handler(event, context):
    client = boto3.client('ec2')
    # instanceids = ['i-00e50946ad570a835', 'i-04ef0a9fb5855667f', 'i-0a1ae25bef22107da', 'i-09ed5e8e88a70e1ba','i-0e518f779edad179d', 'i-0d4b90a92aa5e5591']
    instanceids = ['i-0c9ba1c2244a32141']
    client.start_instances(
        InstanceIds=instanceids
    )
