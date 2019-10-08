import boto3
import json
import time


class CheckS3(object):
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.s3_dict = {}
        self.s3_client2 = boto3.resource('s3')

    def get_s3_bucket_list(self):
        buckets = []
        buckets_info = self.s3_buckets_list()
        for bucket in buckets_info:
            buckets.append(bucket['Name'])
        return buckets

    def s3_buckets_list(self):
        response = self.s3_client.list_buckets()
        return response['Buckets']

    def s3_objects_items(self, bucket_name):
        objects_count = 0
        objects_size = 0
        resp = self.s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in resp.keys():
            bucket_objects = resp['Contents']
            objects_count += len(bucket_objects)
            for bucket_object in bucket_objects:
                object_size = bucket_object['Size']
                objects_size += object_size
            while 'NextContinuationToken' in resp:
                resp = self.s3_client.list_objects_v2(Bucket=bucket_name, ContinuationToken=resp['NextContinuationToken'])
                bucket_objects = resp['Contents']
                objects_count += len(bucket_objects)
                for bucket_object in bucket_objects:
                    object_size = bucket_object['Size']
                    objects_size += object_size
        return objects_count, objects_size

    def main(self):
        filename = 's3_info.txt'
        upload_bucket = 'cloudwatchlog'
        f = open(filename, 'w')
        for bucket in self.get_s3_bucket_list()[:]:
            self.s3_dict[bucket] = {}
            objects_count, objects_size = self.s3_objects_items(bucket)
            self.s3_dict[bucket]['count'] = objects_count
            self.s3_dict[bucket]['size'] = objects_size
        f.write(json.dumps(self.s3_dict))
        f.close()
        self.s3_client2.meta.client.upload_file(filename, upload_bucket, filename)


if __name__ == '__main__':
    app = CheckS3()
    while True:
        app.main()
        time.sleep(3600)
