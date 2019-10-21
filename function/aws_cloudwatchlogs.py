import boto3


class AWSCloudWatchLogs(object):
    def __init__(self):
        self.logs_client = boto3.client('logs')

    def logs_log_group_create(self, log_group_name):
        response = self.logs_client.create_log_group(
            logGroupName=log_group_name,
            # kmsKeyId='string',
            # tags={
            #     'string': 'string'
            # }
        )
        print(response)

    def logs_log_group_delete(self, log_group_name):
        response = self.logs_client.delete_log_group(
            logGroupName=log_group_name
        )
        print(response)

    def logs_log_groups_describe(self):
        response = self.logs_client.describe_log_groups(
            # logGroupNamePrefix='string',
            # nextToken='string',
            # limit=123
        )
        print(response)
        return response['logGroups']

    def logs_log_group_describe(self, log_group_name_prefix):
        response = self.logs_client.describe_log_groups(
            logGroupNamePrefix=log_group_name_prefix,
            # nextToken='string',
            # limit=123
        )
        print(response)
        return response['logGroups']

    def logs_tags_log_group_list(self, log_group_name):
        response = self.logs_client.list_tags_log_group(
            logGroupName=log_group_name
        )
        print(response)

    def logs_log_stream_create(self, log_group_name, log_stream_name):
        response = self.logs_client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )
        print(response)

    def logs_log_stream_delete(self, log_group_name, log_stream_name):
        response = self.logs_client.delete_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )
        print(response)

    def logs_log_stream_describe(self, log_group_name, log_stream_name):
        response = self.logs_client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name,
            # orderBy='LogStreamName' | 'LastEventTime',
            # descending=True | False,
            # nextToken='string',
            # limit=123
        )
        print(response)

    def logs_log_streams_describe(self, log_group_name):
        response = self.logs_client.describe_log_streams(
            logGroupName=log_group_name,
            # logStreamNamePrefix=log_stream_name,
            orderBy='LastEventTime',
            # orderBy='LogStreamName' | 'LastEventTime',
            # descending=True | False,
            descending=True,
            # nextToken='string',
            # limit=123
        )
        # print(response['logStreams'])
        return response['logStreams']

    def logs_metric_filters_describe(self):
        response = self.logs_client.describe_metric_filters(
            # logGroupName='string',
            # filterNamePrefix='string',
            # nextToken='string',
            # limit=123,
            # metricName='string',
            # metricNamespace='string'
        )
        print(response)

    def logs_metric_filter_describe(self, log_group_name):
        response = self.logs_client.describe_metric_filters(
            logGroupName=log_group_name,
            # filterNamePrefix='string',
            # nextToken='string',
            # limit=123,
            # metricName=mertic_name,
            # metricNamespace='string'
        )
        print(response)

    def logs_metric_filter_delete(self, log_group_name, filter_name):
        response = self.logs_client.delete_metric_filter(
            logGroupName=log_group_name,
            filterName=filter_name
        )
        print(response)

    def logs_metric_filter_put(self, metric_filter_info):
        # metric_filter_info={
        #     'logGroupName':'test',
        #     'filterName':'test',
        #     'filterPattern':'test',
        #     'metricTransformations':[
        #         {
        #             'metricName': 'test',
        #             'metricNamespace': 'test',
        #             'metricValue': 'test',
        #             'defaultValue': 123.0
        #         },
        #     ]
        # }
        response = self.logs_client.put_metric_filter(
            logGroupName=metric_filter_info['logGroupName'],
            filterName=metric_filter_info['filterName'],
            filterPattern=metric_filter_info['filterPattern'],
            metricTransformations=metric_filter_info['metricTransformations'],
        )
        print(response)
        return response

    def logs_metric_filter_test(self,filter_pattern):
        response = self.logs_client.test_metric_filter(
            filterPattern=filter_pattern,
            logEventMessages=[
                'string',
            ]
        )
        print(response)
        return response

    def logs_log_events_filter(self):
        log_event_filter_info={
            'logGroupName':'/ecs/op-prd-wxapi-task',
            'logStreamNames':['ecs/op-prd-wxapi-container/880c6ed2-229c-41ba-95bc-c0a1a4f4f781',],
            # 'startTime':123,
            # 'endTime':123,
            'filterPattern':'GET',
        }
        response = self.logs_client.filter_log_events(
            logGroupName=log_event_filter_info['logGroupName'],
            # logStreamNames=log_event_filter_info['logStreamNames'],
            # logStreamNamePrefix='string',
            startTime=1570452000000,
            endTime=1570452010000,
            filterPattern=log_event_filter_info['filterPattern'],
            # nextToken='string',
            # limit=123,
            # interleaved=True | False
        )
        print(response['events'])
        print(len(response['events']))
        return response['events']

    def logs_log_events_put(self):
        event_info={
            'logGroupName':'opwxapi-test',
            'logStreamName':'opwxapi',
            'logEvents':['opxinapi',]
        }
        response = self.logs_client.put_log_events(
            logGroupName=event_info['logGroupName'],
            logStreamName=event_info['logGroupName'],
            logEvents=event_info['logEvents'],
            # logEvents=[
            #     {
            #         'timestamp': 123,
            #         'message': 'string'
            #     },
            # ],
            # sequenceToken='string'
        )
        print(response)



if __name__ == '__main__':
    app = AWSCloudWatchLogs()
    # app.logs_metric_filters_describe()
    # app.logs_log_stream_delete('test', 'nginx')
    app.logs_metric_filters_describe()
    # app.logs_log_events_filter()
    # app.logs_log_events_put()
    # app.logs_metric_filter_delete('/ecs/dudu-api','test-INF')
