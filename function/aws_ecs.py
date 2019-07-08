import boto3

#ami id is ami-0cdb0bf27047e574c or ami-0e81f5d171d41f252


class AWSECS(object):
    def __init__(self):
        self.ecs_client = boto3.client('ecs')

    def ecs_cluster_create(self, cluster_info):
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

    def ecs_cluster_delete(self, clustername):
        response = self.ecs_client.delete_cluster(
            cluster=clustername
        )
        print(response)

    def ecs_clusters_descirpt(self, clustername):
        response = self.ecs_client.describe_clusters(
            clusters=[
                clustername,
            ]
        )
        print(response)


if __name__ == '__main__':
    app = AWSECS()
    cluster_info = {
        'clusterName': 'demo01',
        'tags': [
            {
                'key': 'Name',
                'value': 'demo01'
            }
        ]
    }
    app.ecs_cluster_delete('demo01')
