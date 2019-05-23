from function.aws_ec2 import AWSEC2
import json

sg_info = {
    "securitygroupid": "sg-0a97d9150f2dfb4a8",
    "policy": ''
}


class Network(object):
    def __init__(self):
        self.client = AWSEC2()
        self.sg_id = 'sg-0a97d9150f2dfb4a8'
        self.route_table_id = 'rtb-026894dd715d4c5c5'
        self.inbound_policy_path = 'config/waf/sg_inbound_access.txt'
        self.gw_id = 'igw-07c7878cae15f2ac8'
        # self.destinations =['114.55.164.102/32','58.247.155.150/32','220.248.34.166/32']
        # self.destinations =['0.0.0.0/0',]
        self.destinations =['0.0.0.0/0',] #AWS yum resource
        self.new_inbound_policy = self.read_file(self.inbound_policy_path)

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
        return data

    def get_sg_inbond_policy(self):
        inbound_policy = self.client.ec2_security_group_describe(self.sg_id)['IpPermissions']
        return inbound_policy

    def update_sg_inbound(self):
        sg_info['policy'] = self.get_sg_inbond_policy()
        self.client.ec2_security_group_inbound_policies_revoke(sg_info)
        self.client.ec2_security_group_inbound_policies_add(self.new_inbound_policy)

    def get_route(self):
        route = self.client.ec2_route_table_describe(self.route_table_id)
        print(route)

    def add_route(self):
        for destination in self.destinations:
            route_table_info = {
                'DestinationCidrBlock': destination,
                'GatewayId': self.gw_id,
            }
            self.client.ec2_route_add_gw(self.route_table_id, route_table_info)

    def delete_route(self):
        for destination in self.destinations:
            self.client.ec2_route_delete(destination, self.route_table_id)

    def main(self):
        # self.update_sg_inbound()
        self.add_route()
        # self.delete_route()


if __name__ == '__main__':
    app = Network()
    app.main()
