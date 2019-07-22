from configparser import RawConfigParser
import json
import os

resource_path = 'config/devops_chain/resource.txt'
config_file_path = 'resource_j2c.ini'


class JsonToConfig(object):
    def __init__(self):
        self.cfw = RawConfigParser()
        self.resources = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)

    def set_cf(self, service, option):
        item = self.resources[service][option]
        self.cfw.set(service, option, item)

    def main(self):
        print(self.resources)
        for service in self.resources:
            self.cfw.add_section(service)
            keys=self.resources[service].keys()
            if len(keys) !=0:
                for option in keys:
                    self.set_cf(service, option)
        f = open(config_file_path, 'w')
        self.cfw.write(f)


if __name__ == '__main__':
    app = JsonToConfig()
    app.main()
