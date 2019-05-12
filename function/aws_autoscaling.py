import boto3


class AWSAutoScaling(object):
    def __init__(self):
        self.autoscaling_client = boto3.client('autoscaling')

    def autoscaling_auto_scaling_group_describe(self,autoscaling_group_name):
        response = self.autoscaling_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                autoscaling_group_name,
            ],
            # NextToken='string',
            # MaxRecords=123
        )
        print(response)
        return response

    def autoscaling_auto_scaling_groups_describe(self):
        response = self.autoscaling_client.describe_auto_scaling_groups(
            # AutoScalingGroupNames=[
            #     'string',
            # ],
            # NextToken='string',
            # MaxRecords=123
        )
        print(response)

if __name__ == '__main__':
    app=AWSAutoScaling()
    app.autoscaling_auto_scaling_groups_describe()