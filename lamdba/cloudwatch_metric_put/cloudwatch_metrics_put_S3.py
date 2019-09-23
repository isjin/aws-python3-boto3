import boto3
import json
from datetime import datetime

cloudwatch_client = boto3.client('cloudwatch')
s3_client = boto3.client('s3')
metric_data_template = 'metric/metric_template.txt'
s3_bucketcount = 'metric/metric_put_count.txt'
metric_data_put = None
metric_data = []


def lambda_handler(event, context):
    print(datetime.now())
    metric_data_put = read_file(metric_data_template)
    metric_data_put['Namespace'] = 'Custom/S3'
    s3_buckets_info = s3_buckets_list()
    s3_buckets_count = len(s3_buckets_info)
    s3_object_total_count = 0
    for s3_bucket_info in s3_buckets_info[:]:
        s3_bucket_name = s3_bucket_info['Name']
        count = s3_objects_count(s3_bucket_name)
        print(count)
        s3_object_total_count += count
        set_metric_data(s3_bucketcount, 'ObjectCount', s3_bucket_name, count)
    set_metric_data(s3_bucketcount, 'BucketCount', 'Bucket', s3_buckets_count)
    set_metric_data(s3_bucketcount, 'TotalObjectCount', 'TotalObject', s3_object_total_count)
    metric_data_put['MetricData'] = metric_data
    cloudwatch_metric_data_put(metric_data_put)
    print(datetime.now())


def set_metric_data(file_path, metricname, dimension_value, value_value):
    metric_data1 = read_file(file_path)
    metric_data1['MetricName'] = metricname
    metric_data1['Dimensions'][0]['Value'] = dimension_value
    metric_data1['Value'] = value_value
    metric_data.append(metric_data1)


def cloudwatch_metric_data_put(metric_data_info):
    cloudwatch_client.put_metric_data(
        Namespace=metric_data_info['Namespace'],
        MetricData=metric_data_info['MetricData']
    )


def s3_buckets_list():
    response = s3_client.list_buckets()
    return response['Buckets']


def s3_objects_count(bucket_name):
    count = 0
    resp = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in resp.keys():
        count += len(resp['Contents'])
        while 'NextContinuationToken' in resp:
            resp = s3_client.list_objects_v2(Bucket=bucket_name, ContinuationToken=resp['NextContinuationToken'])
            count += len(resp['Contents'])
    return count


def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)
    return data


# lambda_handler(1, 1)
