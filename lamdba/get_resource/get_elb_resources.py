import boto3
import json


# from datetime import datetime


def lambda_handler(event, context):
    app = GetResources()
    app.main()


class GetResources(object):
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.elbv2 = boto3.client('elbv2')
        self.s3 = boto3.resource('s3')
        # self.file_path = '/tmp/elb_information.txt'
        self.file_path = 'elb_information.txt'
        self.s3_bucket = 'services.information'
        self.s3_file_path = 'elb_information.txt'
        self.filter = [
            # {
            #     'Name': 'tag:System',
            #     'Values': [
            #         'OP',
            #     ]
            # },
        ]

    @staticmethod
    def write_file(path, data):
        data = json.dumps(data, sort_keys=False, indent=4)
        f = open(path, 'w', encoding='utf-8')
        f.write(data)
        f.close()
        return

    def ec2_instance_describe(self, instanceid):
        response = self.ec2.describe_instances(
            InstanceIds=[
                instanceid,
            ],
        )
        return response['Reservations'][0]

    def elbv2_load_balancers_describe(self):
        response = self.elbv2.describe_load_balancers(
        )
        # print(response)
        return response['LoadBalancers']

    def elbv2_listeners_describe(self, lb_arn):
        response = self.elbv2.describe_listeners(
            LoadBalancerArn=lb_arn,
        )
        return response['Listeners']

    def ec2_security_group_describe(self, sgid):
        response = self.ec2.describe_security_groups(
            GroupIds=[
                sgid,
            ],
        )
        return response['SecurityGroups'][0]

    @staticmethod
    def format_sg_data(data):
        new_data = []
        for each_data in data:
            # print(each_data)
            protocol = each_data['IpProtocol']
            if protocol == "-1":
                protocol = "All"
            if "FromPort" in each_data.keys():
                from_port = each_data['FromPort']
                to_port = each_data['ToPort']
                if from_port == to_port:
                    port_range = str(from_port)
                else:
                    port_range = "%s-%s" % (from_port, to_port)
            else:
                port_range = "All"
            source = []
            ip_ranges = each_data['IpRanges']
            if len(ip_ranges) > 0:
                for ip_range in ip_ranges:
                    source.append(ip_range['CidrIp'])
            user_id_group_pairs = each_data['UserIdGroupPairs']
            if len(user_id_group_pairs) > 0:
                for user_id_group_pair in user_id_group_pairs:
                    source.append(user_id_group_pair['GroupId'])
            new_data.append(
                {
                    'Protocol': protocol,
                    'PortRange': port_range,
                    'Source': source,
                }
            )
        return new_data

    def elbv2_rules_describe(self, listener_arn):
        response = self.elbv2.describe_rules(
            ListenerArn=listener_arn,
        )
        return response['Rules']

    def elbv2_target_group_describe(self, target_group_arn):
        response = self.elbv2.describe_target_groups(
            TargetGroupArns=[
                target_group_arn,
            ]
        )
        return response['TargetGroups'][0]

    def elbv2_target_healthy_describe(self, target_group_arn):
        response = self.elbv2.describe_target_health(
            TargetGroupArn=target_group_arn,
        )
        return response['TargetHealthDescriptions']

    def main(self):
        total_infos = []
        elbsv2_info = self.elbv2_load_balancers_describe()
        for elbv2_info in elbsv2_info:
            # print(elbv2_info)
            elbv2_load_balancer_arn = elbv2_info['LoadBalancerArn']
            elbv2_load_balancer_name = elbv2_info['LoadBalancerName']
            elbv2_dns_name = elbv2_info['DNSName']
            elbv2_state = elbv2_info['State']['Code']
            elbv2_vpc_id = elbv2_info['VpcId']
            elbv2_type = elbv2_info['Type']
            elbv2_subnets_ids = []
            elbv2_availability_zones = []
            elbv2_availability_zones_infos = elbv2_info['AvailabilityZones']
            for elbv2_az_info in elbv2_availability_zones_infos:
                elbv2_subnets_ids.append(elbv2_az_info['SubnetId'])
                elbv2_availability_zones.append(elbv2_az_info['ZoneName'])
            elbv2_security_groups_policies = []
            for sg_id in elbv2_info['SecurityGroups']:
                ec2_sg_id_info = self.ec2_security_group_describe(sg_id)
                # print(ec2_sg_id_info)
                ec2_sg_name = ec2_sg_id_info['GroupName']
                ec2_sg_id_inbound_infos = ec2_sg_id_info['IpPermissions']
                ec2_sg_id_inbound_infos = self.format_sg_data(ec2_sg_id_inbound_infos)
                ec2_sg_id_outbound_infos = ec2_sg_id_info['IpPermissionsEgress']
                ec2_sg_id_outbound_infos = self.format_sg_data(ec2_sg_id_outbound_infos)
                elbv2_security_groups_policies.append(
                    {'SecurityGroupID': sg_id, 'SecurityGroupName': ec2_sg_name, 'InboundRules': ec2_sg_id_inbound_infos,
                     'OutboundRules': ec2_sg_id_outbound_infos})
            elbv2_listeners = []
            elbv2_listeners_info = self.elbv2_listeners_describe(elbv2_load_balancer_arn)
            for elbv2_listener_info in elbv2_listeners_info:
                # print(elbv2_listener_info)
                elbsv2_listener_arn = elbv2_listener_info['ListenerArn']
                elbsv2_listener_protocol = elbv2_listener_info['Protocol']
                elbsv2_listener_port = elbv2_listener_info['Port']
                elbsv2_certificates = None
                if 'Certificates' in elbv2_listener_info.keys():
                    elbsv2_certificates = []
                    for certificate_info in elbv2_listener_info['Certificates']:
                        certificate_arn = certificate_info['CertificateArn']
                        certificate_name = str(certificate_arn).split('/')[1]
                        elbsv2_certificates.append(certificate_name)
                elbv2_listener_rules = []
                elbv2_listener_rules_info = self.elbv2_rules_describe(elbsv2_listener_arn)
                for elbsv2_listener_rule_info in elbv2_listener_rules_info:
                    # print(elbsv2_listener_rule_info)
                    rule_priority = elbsv2_listener_rule_info['Priority']
                    conditions = None
                    conditions_info = elbsv2_listener_rule_info['Conditions']
                    if len(conditions_info) > 0:
                        conditions = conditions_info
                    elbv2_listener_target_groups_info = elbsv2_listener_rule_info['Actions'][0]['ForwardConfig']['TargetGroups']
                    elbv2_target_groups = []
                    for elbv2_listener_target_group_info in elbv2_listener_target_groups_info:
                        elbv2_listener_target_group_arn = elbv2_listener_target_group_info['TargetGroupArn']
                        elbv2_target_group_info = self.elbv2_target_group_describe(elbv2_listener_target_group_arn)
                        # print(elbv2_target_group_info)
                        elbv2_target_group_name = elbv2_target_group_info['TargetGroupName']
                        elbv2_target_group_protocol = elbv2_target_group_info['Protocol']
                        elbv2_target_group_port = elbv2_target_group_info['Port']
                        elbv2_target_group_type = elbv2_target_group_info['TargetType']
                        elbv2_targets_health_info = self.elbv2_target_healthy_describe(elbv2_listener_target_group_arn)
                        # print(elbv2_targets_health_info)
                        ec2_instances = []
                        for elbv2_target_health_info in elbv2_targets_health_info:
                            ec2_instance_id = elbv2_target_health_info['Target']['Id']
                            ec2_instance_info = self.ec2_instance_describe(ec2_instance_id)['Instances'][0]
                            # print(ec2_instance_info)
                            ec2_instance_name = None
                            for tag in ec2_instance_info['Tags']:
                                if tag['Key'] == 'Name':
                                    ec2_instance_name = tag['Value']
                            ec2_instances.append(
                                {
                                    'InstanceId': ec2_instance_id,
                                    'InstanceName': ec2_instance_name,
                                }
                            )
                        elbv2_target_groups.append(
                            {
                                'TargetGroupName': elbv2_target_group_name,
                                'TargetGroupProtocol': elbv2_target_group_protocol,
                                'TargetGroupPort': elbv2_target_group_port,
                                'TargetGroupType': elbv2_target_group_type,
                                'Targets': ec2_instances,
                            }
                        )
                    elbv2_listener_rules.append(
                        {
                            'Priority': rule_priority,
                            'Conditions': conditions,
                            'TargetGroups': elbv2_target_groups,
                        }
                    )

                elbv2_listeners.append(
                    {
                        'ListenerArn': elbsv2_listener_arn,
                        'ListenerProtocol': elbsv2_listener_protocol,
                        'ListenerPort': elbsv2_listener_port,
                        'SSLCertificates': elbsv2_certificates,
                        'Rules': elbv2_listener_rules,
                    }
                )
            total_infos.append(
                {
                    'LoadBalancerName': elbv2_load_balancer_name,
                    'DNSName': elbv2_dns_name,
                    'State': elbv2_state,
                    'VpcId': elbv2_vpc_id,
                    'SubnetsId': elbv2_subnets_ids,
                    'AvailabilityZones': elbv2_availability_zones,
                    'Type': elbv2_type,
                    'SecurityGroupsPolicies': elbv2_security_groups_policies,
                    'Listeners': elbv2_listeners,
                }
            )
        self.write_file(self.file_path, total_infos)
        # self.s3.meta.client.upload_file(self.file_path, self.s3_bucket, self.s3_file_path)


if __name__ == '__main__':
    app = GetResources()
    app.main()
