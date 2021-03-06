import boto3


class AWSECS(object):
    def __init__(self):
        self.ecs_client = boto3.client('ecs')

    def ecs_cluster_create(self, cluster_name):
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
            clusterName=cluster_name,
            # tags=cluster_info['tags'],
        )
        print(response)
        return response['cluster']

    def ecs_cluster_delete(self, clustername):
        response = self.ecs_client.delete_cluster(
            cluster=clustername
        )
        print(response)

    def ecs_cluster_describe(self, clustername):
        response = self.ecs_client.describe_clusters(
            clusters=[
                clustername,
            ]
        )
        print(response)
        return response

    def ecs_clusters_list(self):
        response = self.ecs_client.list_clusters(
            # nextToken='string',
            # maxResults=123
        )
        return response['clusterArns']

    def ecs_task_definition_register(self, task_definition_info):
        # task_definition_info={
        #     'family':'hello world',
        #     'taskRoleArn':'arn:aws-cn:iam::952375741452:role/ECSTaskRole',
        #     'executionRoleArn':'arn:aws-cn:iam::952375741452:role/ECSTaskRole',
        #     'networkMode':'bridge',
        #     'containerDefinitions':[],
        #     'volumes':[],
        #     'cpu':'null',
        #     'memory':'null',
        #     'proxyConfiguration':'null',
        # }
        response = self.ecs_client.register_task_definition(
            family=task_definition_info['family'],
            taskRoleArn=task_definition_info['taskRoleArn'],
            executionRoleArn=task_definition_info['executionRoleArn'],
            networkMode=task_definition_info['networkMode'],
            containerDefinitions=task_definition_info['containerDefinitions'],
            volumes=task_definition_info['volumes'],
            # placementConstraints=[
            #     {
            #         'type': 'memberOf',
            #         'expression': 'string'
            #     },
            # ],
            # requiresCompatibilities=[
            #     'EC2' | 'FARGATE',
            # ],
            # cpu=task_definition_info['cpu'],
            # memory=task_definition_info['memory'],
            # tags=[
            #     {
            #         'key': 'string',
            #         'value': 'string'
            #     },
            # ],
            # pidMode='host' | 'task',
            # ipcMode='host' | 'task' | 'none',
            # proxyConfiguration=task_definition_info['proxyConfiguration'],
            # proxyConfiguration={
            #     'type': 'APPMESH',
            #     'containerName': 'string',
            #     'properties': [
            #         {
            #             'name': 'string',
            #             'value': 'string'
            #         },
            #     ]
            # }
        )
        print(response)
        return response['taskDefinition']['taskDefinitionArn']

    def ecs_task_definition_describe(self, task_definition):
        response = self.ecs_client.describe_task_definition(
            taskDefinition=task_definition,
            # include=[
            #     'TAGS',
            # ]
        )
        print(response)

    def ecs_task_definitions_list(self):
        response = self.ecs_client.list_task_definitions(
            # familyPrefix='string',
            # status='ACTIVE' | 'INACTIVE',
            # sort='ASC' | 'DESC',
            # nextToken='string',
            # maxResults=123
        )
        return response['taskDefinitionArns']

    def ecs_task_definition_list(self, task_definition_name):
        response = self.ecs_client.list_task_definitions(
            familyPrefix=task_definition_name,
            # status='ACTIVE' | 'INACTIVE',
            # sort='ASC' | 'DESC',
            # nextToken='string',
            # maxResults=123
        )
        return response['taskDefinitionArns']

    def ecs_task_definition_deregister(self, task_definition):
        # task_definition and version number
        response = self.ecs_client.deregister_task_definition(
            taskDefinition=task_definition
        )
        print(response)

    def ecs_task_run(self, cluster_name, task_definition_name):
        response = self.ecs_client.run_task(
            cluster=cluster_name,
            taskDefinition=task_definition_name,
            # overrides={
            #     'containerOverrides': [
            #         {
            #             'name': 'string',
            #             'command': [
            #                 'string',
            #             ],
            #             'environment': [
            #                 {
            #                     'name': 'string',
            #                     'value': 'string'
            #                 },
            #             ],
            #             'cpu': 123,
            #             'memory': 123,
            #             'memoryReservation': 123,
            #             'resourceRequirements': [
            #                 {
            #                     'value': 'string',
            #                     'type': 'GPU'
            #                 },
            #             ]
            #         },
            #     ],
            #     'taskRoleArn': 'string',
            #     'executionRoleArn': 'string'
            # },
            # count=123,
            # startedBy='string',
            # group='string',
            # placementConstraints=[
            #     {
            #         'type': 'distinctInstance' | 'memberOf',
            #         'expression': 'string'
            #     },
            # ],
            # placementStrategy=[
            #     {
            #         'type': 'random' | 'spread' | 'binpack',
            #         'field': 'string'
            #     },
            # ],
            # launchType='EC2' | 'FARGATE',
            # platformVersion='string',
            # networkConfiguration={
            #     'awsvpcConfiguration': {
            #         'subnets': [
            #             'string',
            #         ],
            #         'securityGroups': [
            #             'string',
            #         ],
            #         'assignPublicIp': 'ENABLED' | 'DISABLED'
            #     }
            # },
            # tags=[
            #     {
            #         'key': 'string',
            #         'value': 'string'
            #     },
            # ],
            # enableECSManagedTags=True | False,
            # propagateTags='TASK_DEFINITION' | 'SERVICE'
        )
        print(response)

    def ecs_task_stop(self, clustername, task_name):
        response = self.ecs_client.stop_task(
            cluster=clustername,
            task=task_name,
            # reason='string'
        )
        print(response)

    def ecs_container_instance_describe(self, cluster, container_instance):
        response = self.ecs_client.describe_container_instances(
            cluster=cluster,
            containerInstances=[
                container_instance,
            ],
            # include=[
            #     'TAGS',
            # ]
        )
        # print(response)
        return response['containerInstances']

    def ecs_container_instance_list(self, cluster_name):
        response = self.ecs_client.list_container_instances(
            cluster=cluster_name,
            # filter='string',
            # nextToken='string',
            # maxResults=123,
            # status='ACTIVE' | 'DRAINING' | 'REGISTERING' | 'DEREGISTERING' | 'REGISTRATION_FAILED'
        )
        return response['containerInstanceArns']

    def ecs_services_list(self, cluser_name):
        response = self.ecs_client.list_services(
            cluster=cluser_name,
            # nextToken='string',
            # maxResults=123,
            # launchType='EC2' | 'FARGATE',
            # schedulingStrategy='REPLICA' | 'DAEMON'
        )
        # print(response)
        return response['serviceArns']

    def ecs_service_describe(self, cluster_name, service_name):
        response = self.ecs_client.describe_services(
            cluster=cluster_name,
            services=[
                service_name,
            ],
            # include=[
            #     'TAGS',
            # ]
        )
        print(response)
        return response

    def ecs_task_describe(self, clustername, task_name):
        response = self.ecs_client.describe_tasks(
            cluster=clustername,
            tasks=[
                task_name,
            ],
            # include=[
            #     'TAGS',
            # ]
        )
        print(response)
        return response['tasks']

    def ecs_tasks_list(self, clustername):
        response = self.ecs_client.list_tasks(
            cluster=clustername,
            # containerInstance='string',
            # family='string',
            # nextToken='string',
            # maxResults=123,
            # startedBy='string',
            # serviceName='string',
            # desiredStatus='RUNNING' | 'PENDING' | 'STOPPED',
            # launchType='EC2' | 'FARGATE'
        )
        print(response)
        return response['taskArns']


if __name__ == '__main__':
    app = AWSECS()
    # app.ecs_container_instance_list('devops-chain-ecs')
    # app.ecs_service_describe('dudu-ecs-prod','dudu-website')
    app.ecs_tasks_list('op-ecs-prod')
    app.ecs_task_describe('op-ecs-prod', 'arn:aws-cn:ecs:cn-northwest-1:646976741397:task/0b552903-2c37-448b-bc13-0c2f0f4a2002')
