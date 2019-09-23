import boto3

sns_client = boto3.client('sns')

topic_arn = 'arn:aws-cn:sns:cn-northwest-1:646976741397:cloudwatch-email-alarm'


def lambda_handler(event, context):
    for subscription in sns_subscriptions_by_topic_list(topic_arn):
        subscription_status = subscription['SubscriptionArn']
        if subscription_status == 'PendingConfirmation':
            sns_subscription_create(subscription['TopicArn'], subscription['Protocol'], subscription['Endpoint'])


def sns_subscriptions_by_topic_list(topic_arn):
    response = sns_client.list_subscriptions_by_topic(
        TopicArn=topic_arn
    )
    return response['Subscriptions']


def sns_subscription_create(topic_arn, protocol, endpoint):
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol=protocol,
        Endpoint=endpoint,
    )
    return response['SubscriptionArn']


# lambda_handler(1, 1)
