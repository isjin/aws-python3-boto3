from configparser import RawConfigParser, ConfigParser
import os
import json

# resource_path = 'config/devops_chain/resouces.txt'
resource_path = 'resouces_list.txt'
resource_config_path = 'resouces_config.ini'
resource_log_path = 'resources.log'


class GenerateConfig(object):
    def __init__(self):
        # self.cf = ConfigParser()
        self.cfw = RawConfigParser()
        self.cfr = ConfigParser()
        self.resources = {}
        self.log = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)

    def write_file(self):
        f = open(resource_log_path, 'w')
        f.write(json.dumps(self.log))
        f.close()

    def set_cf(self, service, option, keyname):
        item = self.resources[service][option][keyname]
        self.cfw.set(service, option, item)

    def generate_resources_config_file(self):
        for service in self.resources.keys():
            if service != 'resource':
                self.cfw.add_section(service)
                for option in self.resources[service]:
                    if service == 'vpcs':
                        self.set_cf(service, option, 'VpcId')
                    elif service == 'subnets':
                        self.set_cf(service, option, 'SubnetId')
                    elif service == 'ecs_clusters':
                        self.set_cf(service, option, 'clusterArn')
                    elif service == 'ecs_task_definitions':
                        self.set_cf(service, option, 'taskDefinitionArns')
                    elif service == 'ecr_repositories':
                        self.set_cf(service, option, 'repositoryName')
                    elif service == 'eips':
                        self.set_cf(service, option, 'PublicIp')
                    elif service == 'volumes':
                        self.set_cf(service, option, 'VolumeId')
                    elif service == 'sns_subscriptions':
                        self.set_cf(service, option, 'SubscriptionArn')
                    else:
                        for key in self.resources[service][option].keys():
                            self.set_cf(service, option, key)
        f = open(resource_config_path, 'w')
        self.cfw.write(f)

    def generate_resources_log(self):
        self.cfr.read(resource_config_path)
        for section in self.cfr.sections():
            self.log[section] = {}
            for option in self.cfr.options(section):
                self.log[section][option] = self.cfr.get(section, option)
        self.write_file()

    def main(self):
        self.generate_resources_config_file()
        self.generate_resources_log()


if __name__ == '__main__':
    app = GenerateConfig()
    app.main()
