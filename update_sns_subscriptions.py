from function.aws_sns import AWSSNS
from configparser import ConfigParser
import os
import json

cf = ConfigParser()
cf.read('build_resources_config.ini')
resource_path = cf.get('resource', 'path')


class UpdateSubscription(object):
    def __init__(self):
        self.sns = AWSSNS()
        self.resources = {}
        self.init_resources()
        self.sns_topics = self.get_sns_topics()

    def init_resources(self):
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)

    def write_file(self):
        while True:
            try:
                f = open(resource_path, 'w')
                f.write(json.dumps(self.resources))
                f.close()
                break
            except Exception as e:
                print(e.__str__())

    def get_sns_topics(self):
        sns_topics = []
        for key in self.resources['sns_topics'].keys():
            sns_topics.append(self.resources['sns_topics'][key])
        return sns_topics

    def main(self):
        for key in list(self.resources['sns_subscriptions'].keys()):
            del self.resources['sns_subscriptions'][key]
        for i in range(len(self.sns_topics)):
            sns_subscriptions_info = self.sns.sns_subscriptions_by_topic_list(self.sns_topics[i])
            for j in range(len(sns_subscriptions_info)):
                key_name = 'subscription' + str(i) + str(j + 1)
                self.resources['sns_subscriptions'][key_name] = sns_subscriptions_info[j]['SubscriptionArn']
        self.write_file()


if __name__ == '__main__':
    app = UpdateSubscription()
    app.main()
