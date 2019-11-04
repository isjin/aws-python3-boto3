import boto3


class AWSS3(object):
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def s3_bucket_create(self,bucket_info):
        # bucket_info = {
        #     'ACL': 'private',
        #     'Bucket': 'jlrtest',
        #     'LocationConstraint': 'cn-north-1',
        # }
        response = self.s3_client.create_bucket(
            # ACL='private' | 'public-read' | 'public-read-write' | 'authenticated-read',
            ACL=bucket_info['ACL'],
            Bucket=bucket_info['Bucket'],
            CreateBucketConfiguration={
                'LocationConstraint': bucket_info['LocationConstraint']
            },
            # GrantFullControl='string',
            # GrantRead='string',
            # GrantReadACP='string',
            # GrantWrite='string',
            # GrantWriteACP='string',
            # ObjectLockEnabledForBucket=True | False
        )
        print(response)

    def s3_bucket_delete(self, bucket_name):
        response = self.s3_client.delete_bucket(
            Bucket=bucket_name
        )
        print(response)

    def s3_buckets_list(self):
        response = self.s3_client.list_buckets()
        # print(response)
        return response['Buckets']

    def s3_objects_list(self, bucket_name):
        response = self.s3_client.list_objects(
            Bucket=bucket_name,
            # Delimiter='string',
            # EncodingType='url',
            # Marker='string',
            # MaxKeys=123,
            # Prefix='string',
            # RequestPayer='requester'
        )
        # print(response)
        return response['Contents']

    def s3_bucket_acl_get(self, bucket_name):
        response = self.s3_client.get_bucket_acl(
            Bucket=bucket_name
        )
        print(response)

    def s3_bucket_policy_get(self, bucket_name):
        response = self.s3_client.get_bucket_policy(
            Bucket=bucket_name
        )
        print(response)

    def s3_bucket_lifecycle_get(self, bucket_name):
        response = self.s3_client.get_bucket_lifecycle(
            Bucket=bucket_name
        )
        print(response)


if __name__ == '__main__':
    app = AWSS3()
    # app.s3_bucket_create()
    # app.s3_bucket_acl_get('jlr-backup')
    app.s3_objects_list('dudumaildebug')
