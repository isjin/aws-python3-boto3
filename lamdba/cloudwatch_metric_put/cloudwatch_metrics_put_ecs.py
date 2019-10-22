import boto3
import json


def lambda_handler(event, context):
    app = MetricECS()
    app.main()


class MetricECS(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.ecs_client = boto3.client('ecs')
        self.metric_data_template = 'metric/metric_template.txt'
        self.metric_count_template = 'metric/metric_put_count.txt'
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

    def ecs_clusters_list(self):
        response = self.ecs_client.list_clusters(
        )
        return response['clusterArns']

    def ecs_services_list(self, cluser_name):
        response = self.ecs_client.list_services(
            cluster=cluser_name,
        )
        return response['serviceArns']

    def ecs_service_describe(self, cluster_name, service_name):
        response = self.ecs_client.describe_services(
            cluster=cluster_name,
            services=[
                service_name,
            ]
        )
        # print(response)
        return response['services'][0]

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def ecs_tasks_list(self, clustername):
        response = self.ecs_client.list_tasks(
            cluster=clustername,
        )
        # print(response)
        return response['taskArns']

    def main(self):
        metric_data_put = self.read_file(self.metric_data_template)
        metric_data_put['Namespace'] = 'ECS'
        ecs_cluster_arns = self.ecs_clusters_list()
        ecs_cluster_count = len(ecs_cluster_arns)
        ecs_service_count = 0
        ecs_service_active_count = 0
        ecs_service_inactive_count = 0
        ecs_tasks_total_count = 0
        for ecs_cluster_arn in ecs_cluster_arns:
            ecs_cluster_name = str(ecs_cluster_arn).split('/')[-1]
            ecs_services_info = self.ecs_services_list(ecs_cluster_name)
            ecs_service_count += len(ecs_services_info)
            tasks_info = self.ecs_tasks_list(ecs_cluster_name)
            ecs_tasks_count = len(tasks_info)
            ecs_tasks_total_count += ecs_tasks_count
            # self.set_metric_data(self.metric_count_template, 'ECSTaskCount', 'ECSTask', ecs_tasks_count)
            for i in range(len(ecs_services_info)):
                ecs_service_name = str(ecs_services_info[i]).split('/')[1]
                ecs_service_info = self.ecs_service_describe(ecs_cluster_name, ecs_service_name)
                ecs_service_status = ecs_service_info['status']
                if ecs_service_status == 'ACTIVE':
                    running_count = ecs_service_info['runningCount']
                    desired_count = ecs_service_info['desiredCount']
                    if running_count == 0 and desired_count !=0:
                        ecs_service_inactive_count += 1
                    else:
                        ecs_service_active_count += 1
                else:
                    ecs_service_inactive_count += 1
        self.set_metric_data(self.metric_count_template, 'ECSTaskCount', 'ECSTask', ecs_tasks_total_count)
        self.set_metric_data(self.metric_count_template, 'ECSClusterCount', 'ECSCluster', ecs_cluster_count)
        self.set_metric_data(self.metric_count_template, 'ECSServiceCount', 'ECSService', ecs_service_count)
        self.set_metric_data(self.metric_count_template, 'ECSServiceActiveCount', 'ECSServiceActive', ecs_service_active_count)
        self.set_metric_data(self.metric_count_template, 'ECSServiceInactiveCount', 'ECSServiceInactive', ecs_service_inactive_count)
        for metric_data in self.metric_data:
            metric_data_put['MetricData'] = [metric_data]
            self.cloudwatch_metric_data_put(metric_data_put)

# if __name__ == '__main__':
#     app = MetricECS()
#     app.main()