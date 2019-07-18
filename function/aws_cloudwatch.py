import boto3
import json

class AWSCloudWatch(object):
    def __init__(self):
        self.cloudwatch_client=boto3.client('cloudwatch')

    def cloudwatch_dashboard_create(self,dashboard_info):
        # dashboard_info={
        #     'DashboardName':'test2',
        #     'DashboardBody':{
        #         "widgets": [
        #
        #         ]
        #     }
        # }
        response = self.cloudwatch_client.put_dashboard(
            DashboardName=dashboard_info['DashboardName'],
            DashboardBody=json.dumps(dashboard_info['DashboardBody'])
        )
        print(response)

    def cloudwatch_dashboard_get(self,dashboard_name):
        response = self.cloudwatch_client.get_dashboard(
            DashboardName=dashboard_name
        )
        print(response)

    def cloudwatch_dashboard_delete(self,dashboard_name):
        response = self.cloudwatch_client.delete_dashboards(
            DashboardNames=[
                dashboard_name,
            ]
        )
        print(response)

if __name__ == '__main__':
    app =AWSCloudWatch()
    app.cloudwatch_dashboard_delete('test2')