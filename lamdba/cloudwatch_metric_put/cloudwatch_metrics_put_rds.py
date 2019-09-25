import boto3
import json


def lambda_handler(event, context):
    app = MetricRDS()
    app.main()


class MetricRDS(object):
    def __init__(self):
        self.cloudwatch_client = boto3.client('cloudwatch')
        self.rds_client = boto3.client('rds')
        self.metric_data_template = 'metric/metric_template.txt'
        self.metric_count_template = 'metric/metric_put_count.txt'
        self.metric_data = []

    def set_metric_data(self, file_path, MetricName, dimension_value, value_value):
        metric_data = self.read_file(file_path)
        metric_data['MetricName'] = MetricName
        metric_data['Dimensions'][0]['Value'] = dimension_value
        metric_data['Value'] = value_value
        self.metric_data.append(metric_data)

    def cloudwatch_metric_data_put(self, metric_data_info):
        self.cloudwatch_client.put_metric_data(
            Namespace=metric_data_info['Namespace'],
            MetricData=metric_data_info['MetricData']
        )

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def rds_instances_describe(self):
        response = self.rds_client.describe_db_instances(
        )
        return response['DBInstances']

    def main(self):
        metric_data_put = self.read_file(self.metric_data_template)
        metric_data_put['Namespace'] = 'RDS'
        rds_instances_info = self.rds_instances_describe()
        rds_total_count = len(rds_instances_info)
        self.set_metric_data(self.metric_count_template, 'RDSTotalCount', 'RDSTotalTotal', rds_total_count)
        for metric_data in self.metric_data:
            metric_data_put['MetricData'] = [metric_data]
            self.cloudwatch_metric_data_put(metric_data_put)

# lambda_handler(1, 1)
