import boto3


class AWSS3(object):
    def __init__(self):
        self.emr_client = boto3.client('emr')

    def emr_cluster_describe(self,clusterid):
        response = self.emr_client.describe_cluster(
            ClusterId=clusterid
        )
        print(response)
        return response



if __name__ == '__main__':
    app = AWSS3()
    app.emr_cluster_describe('j-1D42XBDMWY41Y')
