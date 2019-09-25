import boto3


def lambda_handler(event, context):
    app = ConfirmSubscriptions()
    app.main()


class ConfirmSubscriptions(object):
    def __init__(self):
        self.sns_client = boto3.client('sns')
        self.topic_arn = 'arn:aws-cn:sns:cn-northwest-1:646976741397:cloudwatch-email-alarm'

    def sns_subscriptions_by_topic_list(self, topic_arn):
        response = self.sns_client.list_subscriptions_by_topic(
            TopicArn=topic_arn
        )
        return response['Subscriptions']

    def sns_subscription_create(self, topic_arn, protocol, endpoint):
        response = self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
        )
        return response['SubscriptionArn']

    def main(self):
        for subscription in self.sns_subscriptions_by_topic_list(self.topic_arn):
            subscription_status = subscription['SubscriptionArn']
            if subscription_status == 'PendingConfirmation':
                self.sns_subscription_create(subscription['TopicArn'], subscription['Protocol'], subscription['Endpoint'])
