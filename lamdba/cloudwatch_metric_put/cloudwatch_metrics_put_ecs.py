import boto3
import json

cloudwatch_client = boto3.client('cloudwatch')
ecs_client = boto3.client('ecs')
metric_data_template = 'metric/metric_template.txt'
metric_count_template = 'metric/metric_put_count.txt'
metric_data = []


def lambda_handler(event, context):
    metric_data_put = read_file(metric_data_template)
    metric_data_put['Namespace'] = 'Custom/ECS'
    ecs_cluster_arns = ecs_clusters_list()
    ecs_cluster_count = len(ecs_cluster_arns)
    ecs_service_count = 0
    ecs_service_active_count = 0
    ecs_service_inactive_count = 0
    for ecs_cluster_arn in ecs_cluster_arns:
        ecs_cluster_name = str(ecs_cluster_arn).split('/')[-1]
        ecs_services_info = ecs_services_list(ecs_cluster_name)
        ecs_service_count += len(ecs_services_info)
        for i in range(len(ecs_services_info)):
            ecs_service_name = str(ecs_services_info[i]).split('/')[1]
            ecs_service_info = ecs_service_describe(ecs_cluster_name, ecs_service_name)
            ecs_service_status = ecs_service_info['status']
            if ecs_service_status == 'ACTIVE':
                ecs_service_active_count += 1
            else:
                ecs_service_inactive_count += 1
    set_metric_data(metric_count_template, 'ECSClusterCount', 'ECSCluster', ecs_cluster_count)
    set_metric_data(metric_count_template, 'ECSServiceCount', 'ECSService', ecs_service_count)
    set_metric_data(metric_count_template, 'ECSServiceActiveCount', 'ECSServiceActive', ecs_service_active_count)
    set_metric_data(metric_count_template, 'ECSServiceInactiveCount', 'ECSServiceInactive', ecs_service_inactive_count)
    metric_data_put['MetricData'] = metric_data
    cloudwatch_metric_data_put(metric_data_put)


def set_metric_data(file_path, MetricName, dimension_value, value_value):
    metric_data1 = read_file(file_path)
    metric_data1['MetricName'] = MetricName
    metric_data1['Dimensions'][0]['Value'] = dimension_value
    metric_data1['Value'] = value_value
    metric_data.append(metric_data1)


def cloudwatch_metric_data_put(metric_data_info):
    response = cloudwatch_client.put_metric_data(
        Namespace=metric_data_info['Namespace'],
        MetricData=metric_data_info['MetricData']
    )


def ecs_clusters_list():
    response = ecs_client.list_clusters(
    )
    return response['clusterArns']


def ecs_services_list(cluser_name):
    response = ecs_client.list_services(
        cluster=cluser_name,
    )
    return response['serviceArns']


def ecs_service_describe(cluster_name, service_name):
    response = ecs_client.describe_services(
        cluster=cluster_name,
        services=[
            service_name,
        ],
        # include=[
        #     'TAGS',
        # ]
    )
    return response['services'][0]


def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)
    return data


lambda_handler(1, 1)
