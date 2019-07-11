from configparser import ConfigParser
import json

cf = ConfigParser()
cf.read('config1.ini')
services_dict = {}
record_path = cf.get('file', 'path')


def write_file():
    while True:
        try:
            f = open(record_path, 'w')
            f.write(json.dumps(services_dict))
            f.close()
            break
        except Exception as e:
            print(e.__str__())


for service in cf.sections():
    if service != 'file':
        services_dict[service] = {}
        for item in cf.options(service):
            service_string = cf.get(service, item)
            service_list = str(service_string).split(',')
            key = service_list[0]
            value = service_list[1]
            if value != "none":
                services_dict[service][key] = value

write_file()
