import boto3


class AWSElastiCache(object):
    def __init__(self):
        self.elasticache_client = boto3.client('elasticache')

    def elasticache_subnet_group_create(self, subnet_group_info):
        # subnet_group_info={
        #     'CacheSubnetGroupName':'brandgoods-prod-subnet-group',
        #     'CacheSubnetGroupDescription':'brandgoods-prod-subnet-group',
        #     'SubnetIds':['subnet-id'],
        # }
        response = self.elasticache_client.create_cache_subnet_group(
            CacheSubnetGroupName=subnet_group_info['CacheSubnetGroupName'],
            CacheSubnetGroupDescription=subnet_group_info['CacheSubnetGroupDescription'],
            SubnetIds=subnet_group_info['SubnetIds']
        )
        print(response)
        return response['CacheSubnetGroup']['CacheSubnetGroupName']

    def elasticache_subnet_group_delete(self, subnet_group_name):
        response = self.elasticache_client.delete_cache_subnet_group(
            CacheSubnetGroupName=subnet_group_name
        )
        print(response)

    def elasticache_cache_cluster_create(self,cache_cluster_info):
        # cache_cluster_info={
        #     'CacheClusterId':'brandgoods-prod-cg',
        #     'AZMode':'single-az',
        #     'PreferredAvailabilityZones':['cn-north-1b'],
        #     'NumCacheNodes':1,
        #     'CacheNodeType':'cache.r4.large',
        #     'Engine':'redis',
        #     'EngineVersion':'5.0.3',
        #     'CacheParameterGroupName':'',
        #     'CacheSubnetGroupName':'',
        #     'SecurityGroupIds':['sg-aaaa',],
        #     'Port':6379,
        # }
        response = self.elasticache_client.create_cache_cluster(
            CacheClusterId=cache_cluster_info['CacheClusterId'],
            # ReplicationGroupId='string',
            # AZMode='single-az' | 'cross-az',
            AZMode=cache_cluster_info['AZMode'],
            # PreferredAvailabilityZone='string',
            PreferredAvailabilityZones=cache_cluster_info['PreferredAvailabilityZones'],
            NumCacheNodes=cache_cluster_info['NumCacheNodes'],
            CacheNodeType=cache_cluster_info['CacheNodeType'],
            Engine=cache_cluster_info['Engine'],
            EngineVersion=cache_cluster_info['EngineVersion'],
            CacheParameterGroupName=cache_cluster_info['CacheParameterGroupName'],
            CacheSubnetGroupName=cache_cluster_info['CacheSubnetGroupName'],
            # CacheSecurityGroupNames=[
            #     'string',
            # ],
            SecurityGroupIds=cache_cluster_info['SecurityGroupIds'],
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ],
            # SnapshotArns=[
            #     'string',
            # ],
            # SnapshotName='string',
            # PreferredMaintenanceWindow='string',
            Port=cache_cluster_info['Port'],
            # NotificationTopicArn='string',
            # AutoMinorVersionUpgrade=True | False,
            # SnapshotRetentionLimit=123,
            # SnapshotWindow='string',
            # AuthToken='string'
        )
        print(response)
        return response['CacheCluster']['CacheClusterId']

    def elasticache_cache_cluster_describe(self,cluster_id):
        response = self.elasticache_client.describe_cache_clusters(
            CacheClusterId=cluster_id,
            # MaxRecords=123,
            # Marker='string',
            # ShowCacheNodeInfo=True | False,
            # ShowCacheClustersNotInReplicationGroups=True | False
        )
        print(response)
        return response

    def elasticache_cache_clusters_describe(self):
        response = self.elasticache_client.describe_cache_clusters(
            # CacheClusterId=cluster_id,
            # MaxRecords=123,
            # Marker='string',
            # ShowCacheNodeInfo=True | False,
            # ShowCacheClustersNotInReplicationGroups=True | False
        )
        # print(response)
        return response['CacheClusters']


if __name__ == '__main__':
    app = AWSElastiCache()
    app.elasticache_cache_clusters_describe()
