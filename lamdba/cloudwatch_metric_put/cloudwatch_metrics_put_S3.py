import boto3
import json

cloudwatch_client = boto3.client('cloudwatch')
s3_client = boto3.client('s3')
s3_bucket_count_metric_template = 'metric/metric_put_s3_bucketcount.txt'


def lambda_handler(event, context):
    s3_buckets = s3_buckets_list()
    s3_buckets_count = len(s3_buckets)
    metric_data_s3bucketcount = read_file(s3_bucket_count_metric_template)
    metric_data_s3bucketcount['MetricData'][0]['Value'] = s3_buckets_count
    cloudwatch_metric_data_put(metric_data_s3bucketcount)


def cloudwatch_metric_data_put(metric_data_info):
    response = cloudwatch_client.put_metric_data(
        Namespace=metric_data_info['Namespace'],
        MetricData=metric_data_info['MetricData']
    )


def s3_buckets_list():
    response = s3_client.list_buckets()
    return response['Buckets']


def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)
    return data


lambda_handler('1', '1')
