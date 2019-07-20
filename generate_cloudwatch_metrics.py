from function.aws_cloudwatch import AWSCloudWatch
import json

ecs_clusters = ['ecs_test', 'test-ecs']
instance_ids = ['i-004a96c77deedf4da', 'i-0281ab6b8c52e8fd9']


class GenerateMetrics(object):
    def __init__(self):
        self.cloudwatch = AWSCloudWatch()
        self.cloudwatch_path = 'config/test/cloudwatch/cloudwatch.txt'
        self.cloudwatch_data = self.read_file(self.cloudwatch_path)
        self.widgets = []

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    @staticmethod
    def write_file(path, data):
        f = open(path, 'w')
        f.write(json.dumps(data))
        f.close()

    def create_metrics(self, metric_file, service_metrics, service, metric_list, instances):
        for service_metric in service_metrics:
            title = service_metric + '_%s' % service
            data = self.read_file(metric_file)
            metrics = []
            for instance in instances:
                metric = metric_list.copy()
                metric.append(instance)
                metric.append(service_metric)
                metrics.append(metric)
            # print(metrics)
            data['properties']['metrics'] = metrics
            data['properties']['title'] = title
            self.widgets.append(data)

    def create_ecs_metric(self):
        metric_file = 'config/test/cloudwatch/metric_ecs.txt'
        ecs_metrics = ['CPUReservation', 'CPUUtilization', 'MemoryReservation', 'MemoryUtilization']
        service_name = 'ECS'
        metric = ['AWS/ECS', 'ClusterName']
        self.create_metrics(metric_file, ecs_metrics, service_name, metric, ecs_clusters)

    def create_ec2_instance_metric(self):
        metric_file = 'config/test/cloudwatch/metric_ec2_instance.txt'
        ec2_metrics = ['CPUUtilization', 'DiskReadBytes', 'DiskReadOps', 'DiskWriteBytes', 'DiskWriteOps', 'NetworkIn', 'NetworkOut', 'StatusCheckFailed_Instance']
        service_name = 'EC2'
        metric = ['AWS/EC2', 'InstanceId']
        self.create_metrics(metric_file, ec2_metrics, service_name, metric, instance_ids)

    def main(self):
        self.create_ecs_metric()
        self.create_ec2_instance_metric()
        self.cloudwatch_data['DashboardBody']['widgets'] = self.widgets
        self.write_file('config/test/cloudwatch.txt', self.cloudwatch_data)


if __name__ == '__main__':
    app = GenerateMetrics()
    app.main()
