import boto3
import json
from datetime import datetime


def lambda_handler(event, context):
    app = MetricS3()
    app.main()


class MetricS3(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.s3_client = boto3.client('s3')
        self.metric_data_template = 'metric/metric_template.txt'
        self.s3_bucketcount = 'metric/metric_put_count.txt'
        self.s3_objectssize = 'metric/metric_put_size.txt'
        self.metric_data = []

    def set_metric_data(self, file_path, metricname, dimension_value, value_value):
        metric_data = self.read_file(file_path)
        metric_data['MetricName'] = metricname
        metric_data['Dimensions'][0]['Value'] = dimension_value
        metric_data['Value'] = value_value
        self.metric_data.append(metric_data)

    def cloudwatch_metric_data_put(self, metric_data_info):
        self.cloudwatch_client.put_metric_data(
            Namespace=metric_data_info['Namespace'],
            MetricData=metric_data_info['MetricData']
        )

    def s3_buckets_list(self):
        response = self.s3_client.list_buckets()
        return response['Buckets']

    # def s3_objects_items(self, bucket_name):
    #     objects_count = 0
    #     objects_size = 0
    #     resp = self.s3_client.list_objects_v2(Bucket=bucket_name)
    #     if 'Contents' in resp.keys():
    #         bucket_objects = resp['Contents']
    #         objects_count += len(bucket_objects)
    #         for bucket_object in bucket_objects:
    #             object_size = bucket_object['Size']
    #             objects_size += object_size
    #         while 'NextContinuationToken' in resp:
    #             resp = self.s3_client.list_objects_v2(Bucket=bucket_name, ContinuationToken=resp['NextContinuationToken'])
    #             bucket_objects = resp['Contents']
    #             objects_count += len(bucket_objects)
    #             for bucket_object in bucket_objects:
    #                 object_size = bucket_object['Size']
    #                 objects_size += object_size
    #     return objects_count, objects_size

    @staticmethod
    def get_bucket_info(bucketname, s3_info):
        object_count = s3_info[bucketname]['count']
        object_size = s3_info[bucketname]['size']
        # print(object_count,object_size)
        return object_count, object_size

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def main(self):
        print(datetime.now())
        metric_data_put = self.read_file(self.metric_data_template)
        metric_data_put['Namespace'] = 'S3'
        s3_buckets_info = self.s3_buckets_list()
        s3_buckets_count = len(s3_buckets_info)
        s3_object_total_count = 0
        s3_object_total_size = 0
        s3_file = 's3_info.txt'
        # local_file = 's3_info.txt'
        local_file = '/tmp/s3_info.txt'
        s3_info_backet = 'cloudwatchlog'
        s3 = boto3.resource('s3')
        s3.meta.client.download_file(s3_info_backet, s3_file, local_file)
        s3_info = self.read_file(local_file)
        for s3_bucket_info in s3_buckets_info[:]:
            s3_bucket_name = s3_bucket_info['Name']
            s3_bucket_object_count, s3_bucket_object_size = self.get_bucket_info(s3_bucket_name, s3_info)
            # print(count)
            s3_object_total_count += s3_bucket_object_count
            s3_object_total_size += s3_bucket_object_size
            # print(s3_bucket_name,s3_object_total_count,s3_object_total_size)
            self.set_metric_data(self.s3_bucketcount, 'ObjectCount', s3_bucket_name, s3_bucket_object_count)
            self.set_metric_data(self.s3_objectssize, 'BucketSize', s3_bucket_name, s3_bucket_object_size)
        # print(s3_object_total_count,s3_object_total_size)
        self.set_metric_data(self.s3_bucketcount, 'BucketCount', 'Bucket', s3_buckets_count)
        self.set_metric_data(self.s3_bucketcount, 'TotalObjectCount', 'TotalObject', s3_object_total_count)
        self.set_metric_data(self.s3_objectssize, 'AllBucketSize', 'AllBucket', s3_object_total_size)
        for metric_data in self.metric_data:
            metric_data_put['MetricData'] = [metric_data]
            self.cloudwatch_metric_data_put(metric_data_put)
        print(datetime.now())


# lambda_handler(1, 1)
if __name__ == '__main__':
    app = MetricS3()
    app.main()
