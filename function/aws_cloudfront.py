import boto3


class AWSCloudFront(object):
    def __init__(self):
        self.cloudfront_client = boto3.client('cloudfront')
