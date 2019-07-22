import boto3


class AWSSNS(object):
    def __init__(self):
        self.sns_client = boto3.client('sns')

    def sns_topics_list(self):
        response = self.sns_client.list_topics(
            # NextToken='string'
        )
        # print(response)
        return response['Topics']

    def sns_topic_create(self, topic_name):
        response = self.sns_client.create_topic(
            Name=topic_name,
            # Attributes={
            #     'string': 'string'
            # },
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ]
        )
        print(response)
        return response['TopicArn']

    def sns_topic_delete(self, topic_arn):
        response = self.sns_client.delete_topic(
            TopicArn=topic_arn
        )
        print(response)

    def sns_subscriptions_by_topic_list(self, topic_arn):
        response = self.sns_client.list_subscriptions_by_topic(
            TopicArn=topic_arn,
            # NextToken='string'
        )
        # print(response)
        return response['Subscriptions']

    def sns_subscription_create(self, topic_arn, protocol, endpoint):
        # http,https,email,email-json,sms,sqs,application,lambda
        response = self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
            # Attributes={
            #     'string': 'string'
            # },
            # ReturnSubscriptionArn=True | False
        )
        print(response)
        return response['SubscriptionArn']

    def sns_subscription_delete(self, subscription_arn):
        # http,https,email,email-json,sms,sqs,application,lambda
        response = self.sns_client.unsubscribe(
            SubscriptionArn=subscription_arn
        )
        print(response)

    def sns_subscription_comfirm(self, topic_arn, token):
        response = self.sns_client.confirm_subscription(
            TopicArn=topic_arn,
            Token=token,
            # AuthenticateOnUnsubscribe='string'
        )
        print(response)


if __name__ == '__main__':
    app = AWSSNS()
    # topic_arn = app.sns_topic_create('test')
    topic_arn = app.sns_subscription_create('arn:aws-cn:sns:cn-northwest-1:952375741452:email-alarm', 'email', 'isjin1@163.com')
    # app.sns_subscription_delete('arn:aws-cn:sns:cn-northwest-1:952375741452:test:c368a503-2d9f-419d-8ceb-d4d3a1bae436')
