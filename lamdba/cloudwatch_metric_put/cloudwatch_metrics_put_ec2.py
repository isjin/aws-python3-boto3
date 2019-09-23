import boto3
import json

cloudwatch_client = boto3.client('cloudwatch')
ec2_client = boto3.client('ec2')
metric_data_template = 'metric/metric_template.txt'
metric_count_template = 'metric/metric_put_count.txt'

metric_data = []


def lambda_handler(event, context):
    metric_data_put = read_file(metric_data_template)
    metric_data_put['Namespace'] = 'Custom/EC2'
    ec2_instances_info = ec2_instances_describe()
    ec2_instance_count = len(ec2_instances_info)
    ec2_instance_running_count = 0
    ec2_instance_stopped_count = 0
    for ec2_instance_info in ec2_instances_info:
        status = ec2_instance_info['Instances'][0]['State']['Name']
        if status == "running":
            ec2_instance_running_count += 1
        elif status == "stopped":
            ec2_instance_stopped_count += 1
    set_metric_data(metric_count_template, 'EC2InstanceCount', 'EC2Instance', ec2_instance_count)
    set_metric_data(metric_count_template, 'EC2InstanceRunningCount', 'EC2InstanceRunning', ec2_instance_running_count)
    set_metric_data(metric_count_template, 'EC2InstanceStoppedCount', 'EC2InstanceStopped', ec2_instance_stopped_count)
    metric_data_put['MetricData'] = metric_data
    cloudwatch_metric_data_put(metric_data_put)


def set_metric_data(file_path, MetricName, dimension_value, value_value):
    metric_data1 = read_file(file_path)
    metric_data1['MetricName'] = MetricName
    metric_data1['Dimensions'][0]['Value'] = dimension_value
    metric_data1['Value'] = value_value
    metric_data.append(metric_data1)


def cloudwatch_metric_data_put(metric_data_info):
    response = cloudwatch_client.put_metric_data(
        Namespace=metric_data_info['Namespace'],
        MetricData=metric_data_info['MetricData']
    )


def ec2_instances_describe():
    response = ec2_client.describe_instances(
    )
    return response['Reservations']


def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)
    return data


lambda_handler(1, 1)
