import boto3


class AWSECS(object):
    def __init__(self):
        self.ecs_client = boto3.client('ecs')

    def ecs_cluster_create(self,cluster_info):
        # cluster_info={
        #     'clusterName':'demo01',
        #     'tags':[
        #         {
        #             'key': 'string',
        #             'value': 'string'
        #         }
        #     ]
        # }
        response = self.ecs_client.create_cluster(
            clusterName=cluster_info['clusterName'],
            tags=cluster_info['tags'],
        )
        print(response)
        return response

if __name__ == '__main__':
    app=AWSECS()
