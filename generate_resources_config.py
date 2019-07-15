from configparser import RawConfigParser, ConfigParser
import os
import json

resource_path = 'resouces_list.txt'
resource_config_path = 'resouce_config.ini'


class GenerateConfig(object):
    def __init__(self):
        # self.cf = ConfigParser()
        self.cf = RawConfigParser()
        self.resources = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)

    def set_cf(self, service, option, keyname):
        item = self.resources[service][option][keyname]
        self.cf.set(service, option, item)

    def main(self):
        for service in self.resources.keys():
            if service != 'resource':
                self.cf.add_section(service)
                for option in self.resources[service]:
                    if service == 'vpcs':
                        self.set_cf(service, option, 'VpcId')
                    elif service == 'subnets':
                        self.set_cf(service, option, 'SubnetId')
                    elif service == 'ecs_clusters':
                        self.set_cf(service, option, 'ClusterArn')
                    elif service == 'ecs_task_definitions':
                        self.set_cf(service, option, 'taskDefinitionArns')
                    elif service == 'ecr_repositories':
                        self.set_cf(service, option, 'repositoryArn')
                    elif service == 'eips':
                        self.set_cf(service, option, 'PublicIp')
                    elif service == 'volumes':
                        self.set_cf(service, option, 'VolumeId')
                    else:
                        for key in self.resources[service][option].keys():
                            self.set_cf(service, option, key)
        f = open(resource_config_path, 'w')
        self.cf.write(f)


if __name__ == '__main__':
    app = GenerateConfig()
    app.main()
