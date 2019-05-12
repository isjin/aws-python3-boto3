import json


def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)
    return data
