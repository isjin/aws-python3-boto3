import boto3


def lambda_handler(event, context):
    app = CleanCloudWatchLogGroups()
    app.main()


class CleanCloudWatchLogGroups(object):
    def __init__(self):
        self.logs = boto3.client('logs')

    def logs_groups_describe(self):
        response = self.logs.describe_log_groups(
            logGroupNamePrefix='/aws/lambda/',
        )
        return response['logGroups']

    def logs_groups_delete(self, group_name):
        response = self.logs.delete_log_group(
            logGroupName=group_name
        )
        print(response)

    def main(self):
        log_groups_info = self.logs_groups_describe()
        for log_group_info in log_groups_info:
            log_group_name = log_group_info['logGroupName']
            self.logs_groups_delete(log_group_name)


# if __name__ == '__main__':
#     app = CleanCloudWatchLogGroups()
#     app.main()
