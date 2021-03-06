from function import aws_ec2, aws_iam, aws_cloudformation, aws_ecs, aws_ecr, aws_cloudwatch, aws_sns, aws_elb, aws_lambda
from function import aws_autoscaling
from function import aws_cloudwatchlogs
from function import aws_cloudwatchevents
from function import aws_s3
import json
import os
import re
import time
import base64
from datetime import datetime
from configparser import ConfigParser

cf = ConfigParser()
cf.read('build_resources_config.ini')
resource_path = cf.get('resource', 'path')


class DevopsChain(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.iam = aws_iam.AWSIAM()
        self.ecs = aws_ecs.AWSECS()
        self.ecr = aws_ecr.AWSECR()
        self.sns = aws_sns.AWSSNS()
        self.elb = aws_elb.AWSELB()
        self.s3 = aws_s3.AWSS3()
        self.logs = aws_cloudwatchlogs.AWSCloudWatchLogs()
        self.event = aws_cloudwatchevents.AWSEvent()
        self.autoscaling = aws_autoscaling.AWSAutoScaling()
        self.lambda_function = aws_lambda.AWSLambda()
        self.cloudwatch = aws_cloudwatch.AWSCloudWatch()
        self.cloudformation = aws_cloudformation.AWSCloudFormation()
        self.resources = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)
        else:
            self.resources['cloudformations'] = {}
            self.resources['cloudwatch_metric_filters'] = {}
            self.resources['cloudwatch_dashboards'] = {}
            self.resources['cloudwatch_alarms'] = {}
            self.resources['cloudwatchevents_rules'] = {}
            self.resources['cloudwatchevents_rule_targets'] = {}
            self.resources['sns_subscriptions'] = {}
            self.resources['sns_topics'] = {}
            self.resources['ecs_clusters'] = {}
            self.resources['ecs_services'] = {}
            self.resources['ecs_task_definitions'] = {}
            self.resources['ecr_repositories'] = {}
            self.resources['lambda_functions'] = {}
            self.resources['lambda_triggers'] = {}
            self.resources['rds'] = {}
            self.resources['elasticaches'] = {}
            self.resources['igws'] = {}
            self.resources['ngws'] = {}
            self.resources['rtbs'] = {}
            self.resources['roles'] = {}
            self.resources['nacls'] = {}
            self.resources['keypairs'] = {}
            self.resources['ec2_instances'] = {}
            self.resources['autoscaling_launch_configurations'] = {}
            self.resources['autoscaling_groups'] = {}
            self.resources['eips'] = {}
            self.resources['volumes'] = {}
            self.resources['snapshots'] = {}
            self.resources['images'] = {}
            self.resources['elbs'] = {}
            self.resources['elb_target_groups'] = {}
            self.resources['security_groups'] = {}
            self.resources['subnets'] = {}
            self.resources['vpcs'] = {}
            self.resources['s3_buckets'] = {}
            self.write_file()

    @staticmethod
    def read_file(path):
        f = open(path, 'r', encoding='utf-8')
        data = f.read()
        f.close()
        data = json.loads(data.encode(encoding='utf-8'))
        return data

    def write_file(self):
        while True:
            try:
                f = open(resource_path, 'w')
                f.write(json.dumps(self.resources))
                f.close()
                break
            except Exception as e:
                print(e.__str__())

    @staticmethod
    def base64_encrypt(data):
        base64_data = base64.b64encode(str(data).encode('utf-8'))
        # print(base64_data)
        return base64_data.decode()

    def create_vpc(self, vpc_info_path, vpc_key_name):
        vpc_info = self.read_file(vpc_info_path)
        vpc_id = self.ec2.ec2_vpc_create(vpc_info)
        self.resources['vpcs'][vpc_key_name] = vpc_id
        self.write_file()

    def create_subnet(self, subnet_info_path, subnet_key_name, vpc_key_name):
        subnet_info = self.read_file(subnet_info_path)
        if vpc_key_name != 'none':
            subnet_info['vpc'] = self.resources['vpcs'][vpc_key_name]
        subnet_id = self.ec2.ec2_subnet_create(subnet_info)
        self.resources['subnets'][subnet_key_name] = subnet_id
        self.write_file()

    def create_igw(self, igw_info_path, igw_key_name, vpc_key_name):
        igw_info = self.read_file(igw_info_path)
        igw_id = self.ec2.ec2_internet_gateway_create(igw_info)
        self.ec2.ec2_internet_gateway_attach(igw_id, self.resources['vpcs'][vpc_key_name])
        self.resources['igws'][igw_key_name] = igw_id
        self.write_file()

    def create_default_route(self, vpc_key_name, igw_key_name, route_table_name):
        filters = [
            {
                'Name': 'vpc-id',
                'Values': [
                    self.resources['vpcs'][vpc_key_name]
                ]
            }
        ]
        routetable_id = self.ec2.ec2_route_tables_describe(filters)[0]['RouteTableId']
        route_table_tag = {
            'tag': 'Name',
            'tag_description': route_table_name
        }
        self.ec2.ec2_tag_create(routetable_id, route_table_tag)
        route_info = {
            'DestinationCidrBlock': '0.0.0.0/0',
            'GatewayId': self.resources['igws'][igw_key_name]
        }
        self.ec2.ec2_route_add_igw(routetable_id, route_info)

    def create_route(self):
        pass

    def create_keypair(self, keypair_name, keypair_key_name):
        self.ec2.ec2_key_pair_create(keypair_name)
        self.resources['keypairs'][keypair_key_name] = keypair_name
        self.write_file()

    def create_security_group(self, sg_info_path, sg_rule_info_path, sg_key_name, vpc_key_name):
        security_group_info = self.read_file(sg_info_path)
        security_group_info['vpcid'] = self.resources['vpcs'][vpc_key_name]
        security_group_id = self.ec2.ec2_security_group_create(security_group_info)
        self.resources['security_groups'][sg_key_name] = security_group_id
        self.write_file()
        security_group_rule_info = self.read_file(sg_rule_info_path)
        security_group_rule_info['securitygroupid'] = security_group_id
        self.ec2.ec2_security_group_inbound_policies_add(security_group_rule_info)

    def create_role(self, role_info_path, role_key_name):
        role_info = self.read_file(role_info_path)
        role_arn = self.iam.iam_role_create(role_info)['Arn']
        self.resources['roles'][role_key_name] = {}
        self.resources['roles'][role_key_name]['name'] = role_info['RoleName']
        self.resources['roles'][role_key_name]['arn'] = role_arn
        self.write_file()
        if role_info['InstanceProfile']:
            instance_profile_arn = self.iam.iam_instance_profile_create(role_info['RoleName'])
            self.resources['instance_profiles'][role_key_name] = {}
            self.resources['instance_profiles'][role_key_name]['name'] = role_info['RoleName']
            self.resources['instance_profiles'][role_key_name]['arn'] = instance_profile_arn
            self.write_file()
            self.iam.iam_role_to_instance_profile_add(role_info['RoleName'], role_info['RoleName'])
        for policy_arn in role_info['PolicyArns']:
            self.iam.iam_role_policy_attach(role_info['RoleName'], policy_arn)
        self.resources['policies'][role_key_name] = role_info['PolicyArns']
        self.write_file()

    def create_ecr_repository(self, repository_name, repository_keyname):
        self.ecr.repository_create(repository_name)
        self.resources['ecr_repositories'][repository_keyname] = repository_name
        self.write_file()

    def create_ecs_cluster(self, cluster_name, ecs_keyname):
        self.ecs.ecs_cluster_create(cluster_name)
        self.resources['ecs_clusters'][ecs_keyname] = cluster_name
        self.write_file()

    def create_cloudformation(self, cf_template_path, cf_stack_info, cf_stack_keyname):
        # stack_info = self.read_file(cloudformation_stack_path)
        f = open(cf_template_path, 'r')
        template_data = f.read()
        f.close()
        cf_stack_info['TemplateBody'] = template_data
        # print(stack_info)
        self.cloudformation.cloudformation_stack_create(cf_stack_info)
        self.resources['cloudformations'][cf_stack_keyname] = cf_stack_info['StackName']
        self.write_file()
        time.sleep(60)

    def create_ec2_instance(self, ec2_instance_path, sg_keyname, subnet_keyname, ec2_instance_keyname, eip_value):
        instance_info = self.read_file(ec2_instance_path)
        if sg_keyname != 'none':
            instance_info['SecurityGroupIds'] = [self.resources['security_groups'][sg_keyname]]
        if subnet_keyname != 'none':
            instance_info['SubnetId'] = self.resources['subnets'][subnet_keyname]
        instance_id = self.ec2.ec2_instance_create(instance_info)[0]
        self.resources['ec2_instances'][ec2_instance_keyname] = instance_id
        self.write_file()
        while True:
            # status = self.ec2.ec2_instance_describe('i-0064841176315c612')['Instances'][0]['State']['Name']
            status = self.ec2.ec2_instance_describe(instance_id)['Instances'][0]['State']['Name']
            if status == "pending":
                time.sleep(5)
            else:
                break
        if eip_value == 'true':
            self.assign_eip(instance_id, ec2_instance_keyname)
        return

    def get_instance_name(self, instanceid):
        instance_info = self.ec2.ec2_instance_describe(instanceid)
        tags = instance_info['Instances'][0]['Tags']
        instance_name = ''
        for tag in tags:
            if tag['Key'] == "Name":
                instance_name = tag['Value']
                break
        return instance_name

    def create_eip(self, instance_name):
        tags = [
            {
                'Key': 'Name',
                'Value': instance_name
            }
        ]
        eipid, eip_ip = self.ec2.ec2_eip_allocate(tags)
        return eipid, eip_ip

    def assign_eip(self, instanceid, ec2_instance_keyname):
        instance_name = self.get_instance_name(instanceid)
        eipid, eip_ip = self.create_eip(instance_name)
        associate_info = {
            'AllocationId': eipid,
            # 'AllocationId': 'eipalloc-0e0be917bbb463d1c',
            'InstanceId': instanceid,
        }
        self.ec2.ec2_eip_associate_address(associate_info)
        self.resources['eips'][ec2_instance_keyname] = eip_ip
        self.write_file()

    def register_task_definition(self, ecs_task_definition_path, ecs_task_definition_keyname):
        print(ecs_task_definition_path, ecs_task_definition_keyname)
        task_definition_info = self.read_file(ecs_task_definition_path)
        task_definition_arn = self.ecs.ecs_task_definition_register(task_definition_info)
        self.resources['ecs_task_definitions'][ecs_task_definition_keyname] = task_definition_arn
        self.write_file()

    def create_cloudwatch_metric_filter(self, metric_filter_file, keyname):
        metric_filter_info = self.read_file(metric_filter_file)
        # print(metric_filter_info)
        metric_filter_file_name = metric_filter_file.split('/')[-1]
        self.logs.logs_metric_filter_put(metric_filter_info)
        self.resources['cloudwatch_metric_filters'][keyname] = metric_filter_file_name
        self.write_file()

    def create_cloudwatch_dashboard(self, dashboard_path, keyname):
        # os.system('python generate_cloudwatch_metrics.py')
        dashboard_info = self.read_file(dashboard_path)
        self.cloudwatch.cloudwatch_dashboard_create(dashboard_info)
        self.resources['cloudwatch_dashboards'][keyname] = dashboard_info['DashboardName']
        self.write_file()

    def create_cloudwatch_alarm(self, alarm_path, sns_keyname, service_type, instance_type, type_value, keyname):
        if service_type == 'ecs_service':
            ecs_cluster = self.resources['ecs_clusters'][type_value]
            ecs_service_arns = self.ecs.ecs_services_list(ecs_cluster)
            ecs_services = []
            for ecs_service_arn in ecs_service_arns:
                ecs_service = str(ecs_service_arn).split('/')[1]
                ecs_services.append(ecs_service)
            for i in range(len(ecs_services)):
                ecs_service = ecs_services[i]
                alarm_info = self.read_file(alarm_path)
                if sns_keyname != 'none':
                    alarm_info['OKActions'] = [self.resources['sns_topics'][sns_keyname]]
                    alarm_info['AlarmActions'] = [self.resources['sns_topics'][sns_keyname]]
                    alarm_info['InsufficientDataActions'] = [self.resources['sns_topics'][sns_keyname]]
                alarm_path_split = re.split(r'[_.]', str(alarm_path))
                metric = alarm_path_split[-2]
                alarm_name = service_type + '_' + ecs_cluster + '_' + ecs_service + '_' + metric
                alarm_info['AlarmName'] = alarm_name
                alarm_info['Dimensions'][0]['Value'] = ecs_service
                alarm_info['Dimensions'][1]['Value'] = ecs_cluster
                self.cloudwatch.cloudwatch_alarm_create(alarm_info)
                key_number = re.search(r'\d+', str(keyname)).group()
                key_name = 'alarm' + str(int(key_number) + i)
                self.resources['cloudwatch_alarms'][key_name] = alarm_name
                self.write_file()
        else:
            alarm_info = self.read_file(alarm_path)
            alarm_name = None
            alarm_dimension = None
            alarm_path_split = re.split(r'[_.]', str(alarm_path))
            metric = alarm_path_split[-2]
            if sns_keyname != 'none':
                alarm_info['AlarmActions'] = [self.resources['sns_topics'][sns_keyname]]
                # if metric in ['HTTPCode-ELB-4XX-Count', 'HTTPCode-Target-4XX-Count', 'ProcessedBytes', 'TargetResponseTime', 'ActiveConnectionCount']:
                if service_type in ['elb', 'elb_tg']:
                    pass
                else:
                    alarm_info['OKActions'] = [self.resources['sns_topics'][sns_keyname]]
                    alarm_info['InsufficientDataActions'] = [self.resources['sns_topics'][sns_keyname]]
            if instance_type == 'instance':
                alarm_name = service_type + '_' + type_value + '_' + metric
                alarm_dimension = type_value
            else:
                if service_type == 'ec2':
                    alarm_name = service_type + '_' + self.resources['ec2_instances'][type_value] + '_' + metric
                    alarm_dimension = self.resources['ec2_instances'][type_value]
                elif service_type == 'ecs':
                    alarm_name = service_type + '_' + self.resources['ecs_clusters'][type_value] + '_' + metric
                    alarm_dimension = self.resources['ecs_clusters'][type_value]
                elif service_type == 'rds':
                    alarm_name = service_type + '_' + self.resources['rds'][type_value] + '_' + metric
                    alarm_dimension = self.resources['rds'][type_value]
                elif service_type == 'elb':
                    alarm_name = service_type + '_' + str(self.resources['elbs'][type_value]).split('/')[-2] + '_' + metric
                    alarm_dimension = str(self.resources['elbs'][type_value]).split('loadbalancer/')[1]
                elif service_type == 'elb_tg':
                    tg_arn = self.resources['elb_target_groups'][type_value]
                    alarm_dimension_tg = str(tg_arn).split(':')[-1]
                    tg_info = self.elb.elbv2_target_group_describe(tg_arn)
                    tg_name = tg_info['TargetGroupName']
                    elb_arn = tg_info['LoadBalancerArns'][0]
                    elb_name = str(elb_arn).split('/')[-2]
                    alarm_name = service_type + '_' + elb_name + '_' + tg_name + '_' + metric
                    alarm_dimension_elb = str(elb_arn).split('loadbalancer/')[1]
                    alarm_info['Dimensions'][0]['Value'] = alarm_dimension_tg
                    alarm_info['Dimensions'][1]['Value'] = alarm_dimension_elb
                elif service_type == 'elasticache':
                    # if service_type == 'elasticache':
                    #     service_type = 'redis'
                    alarm_name = service_type + '_' + self.resources['elasticaches'][type_value] + '_' + metric
                    alarm_dimension = self.resources['elasticaches'][type_value]
                elif service_type == "cloudwatchlog":
                    alarm_name = alarm_path_split[2] + '_' + alarm_path_split[3]
                    alarm_info['InsufficientDataActions'] = []
                    # alarm_info['OKActions'] = []
            alarm_info['AlarmName'] = alarm_name
            if type_value == 'all':
                alarm_info['Dimensions'] = []
            else:
                if service_type == 'elb_tg':
                    pass
                elif service_type == 'cloudwatchlog':
                    alarm_info['Dimensions'] = []
                else:
                    if metric == 'DiskSpaceUtilization':
                        alarm_info['Dimensions'][1]['Value'] = alarm_dimension
                    else:
                        alarm_info['Dimensions'][0]['Value'] = alarm_dimension
            # print(alarm_info)
            self.cloudwatch.cloudwatch_alarm_create(alarm_info)
            self.resources['cloudwatch_alarms'][keyname] = alarm_name
            self.write_file()

    def create_sns_topic(self, topic_name, keyname):
        topic_arn = self.sns.sns_topic_create(topic_name)
        self.resources['sns_topics'][keyname] = topic_arn
        self.write_file()

    def create_sns_subscription(self, topic_keyname, protocol, endpoint, keyname):
        topic_arn = self.resources['sns_topics'][topic_keyname]
        subscription_arn = self.sns.sns_subscription_create(topic_arn, protocol, endpoint)
        self.resources['sns_subscriptions'][keyname] = subscription_arn
        self.write_file()

    def get_ecs_instance_ids(self):
        if "ecs_clusters" in cf.sections():
            ecs_cluster_options = cf.options('ecs_clusters')
            for i in range(len(ecs_cluster_options)):
                ecs_cluster_name = str(cf.get('ecs_clusters', ecs_cluster_options[i])).split(',')[1]
                while True:
                    container_instances_info = self.ecs.ecs_container_instance_list(ecs_cluster_name)
                    if len(container_instances_info) > 1:
                        break
                for j in range(len(container_instances_info)):
                    ecs_instances_info = self.ecs.ecs_container_instance_describe(ecs_cluster_name, container_instances_info[j])
                    for k in range(len(ecs_instances_info)):
                        ecs_instance_id = ecs_instances_info[k]['ec2InstanceId']
                        ecs_instance_key = 'instance_ecs_' + '%d%d' % (i, j + 1)
                        self.resources['ec2_instances'][ecs_instance_key] = ecs_instance_id
            self.write_file()

    def create_lambda_function(self, zip_file_path, function_name, role, keyname):
        with open(zip_file_path, 'rb') as f:
            zipped_code = f.read()
        function_info = {
            'FunctionName': function_name,
            'Runtime': 'python3.6',
            'Role': role,
            'Handler': '%s.lambda_handler' % function_name,
            'ZipFile': {'ZipFile': zipped_code},
        }
        lambda_info = self.lambda_function.lambda_function_create(function_info)
        function_arn = lambda_info['FunctionArn']
        self.resources['lambda_functions'][keyname] = function_arn
        self.write_file()

    def create_auto_scaling_launch_configuration(self, autoscaling_launch_configuration_file, userdata_file, sg_keyname, keyname):
        autoscaling_launch_configuration_info = self.read_file(autoscaling_launch_configuration_file)
        if userdata_file != 'none':
            f = open(userdata_file, 'r')
            data = f.read()
            f.close()
            # userdata = self.base64_encrypt(data)
            userdata = data
            autoscaling_launch_configuration_info['UserData'] = userdata
        if sg_keyname != 'none':
            sg_name = self.resources['security_groups'][sg_keyname]
            autoscaling_launch_configuration_info['SecurityGroups'] = [sg_name]
        # print(autoscaling_launch_configuration_info)
        launcah_configuration_name = autoscaling_launch_configuration_info['LaunchConfigurationName']
        self.autoscaling.autoscaling_launch_configuration_create(autoscaling_launch_configuration_info)
        self.resources['autoscaling_launch_configurations'][keyname] = launcah_configuration_name
        self.write_file()

    def create_cloudwatchevent_rule(self, rule_name, schedule_rule, keyname):
        rule_arn = self.event.event_rule_put(rule_name, schedule_rule)
        self.resources['cloudwatchevents_rules'][keyname] = rule_arn
        self.write_file()

    def put_cloudwatchevent_rule_target(self, rule_target_file, rule_name, target_id, service_type, target_keyname, keyname):
        target_info = self.read_file(rule_target_file)
        target_info['Rule'] = rule_name
        target_info['Targets'][0]['Id'] = target_id
        if target_keyname != 'none':
            target_arn = self.resources[service_type][target_keyname]
            target_info['Targets'][0]['Arn'] = target_arn
        self.event.event_target_put(target_info)
        self.resources['cloudwatchevents_rule_targets'][keyname] = target_id
        self.write_file()

    def add_lambda_trigger(self, trigger_file, trigger_type, source_arn_keyname, keyname):
        trigger_info = self.read_file(trigger_file)
        if source_arn_keyname != 'none':
            source_arn = self.resources[trigger_type][source_arn_keyname]
            trigger_info['SourceArn'] = source_arn
        self.lambda_function.lambda_permission_add(trigger_info)
        self.resources['lambda_triggers'][keyname] = trigger_info['StatementId']
        self.write_file()

    def create_s3_bucket(self, bucket_file, keyname):
        bucket_info = self.read_file(bucket_file)
        bucket_name = bucket_info['Bucket']
        self.s3.s3_bucket_create(bucket_info)
        self.resources['s3_buckets'][keyname] = bucket_name
        self.write_file()

    def main(self):
        for service in cf.sections():
            service = str(service)
            if service not in ['resource', 'ecs_tasks']:
                print("%s Start to create %s." % (datetime.now(), service))
                for item in cf.options(service):
                    info = str(cf.get(service, item))
                    info = info.split(',')
                    if service == 'default_routes':
                        if info[3] == "true":
                            self.create_default_route(info[0], info[1], info[2])
                    elif info[0] not in self.resources[service].keys():
                        if service == 'vpcs':
                            self.create_vpc(info[1], info[0])
                        if service == "s3_buckets":
                            self.create_s3_bucket(info[1], info[0])
                        elif service == 'subnets':
                            self.create_subnet(info[1], info[0], info[2])
                        elif service == 'igws':
                            self.create_igw(info[1], info[0], info[2])
                        elif service == 'keypairs':
                            self.create_keypair(info[1], info[0])
                        elif service == 'security_groups':
                            self.create_security_group(info[1], info[2], info[0], info[3])
                        elif service == 'roles':
                            self.create_role(info[1], info[0])
                        elif service == 'ecr_repositories':
                            self.create_ecr_repository(info[1], info[0])
                        elif service == 'ecs_clusters':
                            self.create_ecs_cluster(info[1], info[0])
                        elif service == 'lambda_functions':
                            self.create_lambda_function(info[1], info[2], info[3], info[0])
                        elif service == 'lambda_triggers':
                            self.add_lambda_trigger(info[1], info[2], info[3], info[0])
                        elif service == 'cloudformations':
                            cf_stack_info = self.read_file(info[1])
                            cf_parameters = str(info[3]).split(';')
                            subnetids_keyname = cf_parameters[0].split('=')[1].split('|')
                            subnetids_keyname_length = len(subnetids_keyname)
                            subnetids = ''
                            for i in range(subnetids_keyname_length):
                                subnet_id = self.resources['subnets'][subnetids_keyname[i]]
                                if i == subnetids_keyname_length - 1:
                                    subnetids = subnetids + subnet_id
                                else:
                                    subnetids = subnetids + subnet_id + ','
                            sg_keyname = cf_parameters[1].split('=')[1]
                            vpc_keyname = cf_parameters[2].split('=')[1]
                            parameters = []
                            for parameter in cf_stack_info['Parameters']:
                                if parameter['ParameterKey'] == 'VpcId':
                                    parameter['ParameterValue'] = self.resources['vpcs'][vpc_keyname]
                                    parameters.append(parameter)
                                elif parameter['ParameterKey'] == 'SubnetIds':
                                    parameter['ParameterValue'] = subnetids
                                    parameters.append(parameter)
                                elif parameter['ParameterKey'] == 'SecurityGroupId':
                                    parameter['ParameterValue'] = self.resources['security_groups'][sg_keyname]
                                    parameters.append(parameter)
                                else:
                                    parameters.append(parameter)
                            cf_stack_info['Parameters'] = parameters
                            self.create_cloudformation(info[2], cf_stack_info, info[0])
                        elif service == 'ecs_task_definitions':
                            self.register_task_definition(info[1], info[0])
                        elif service == 'ec2_instances':
                            self.create_ec2_instance(info[1], info[2], info[3], info[0], info[4])
                        elif service == 'autoscaling_launch_configurations':
                            self.create_auto_scaling_launch_configuration(info[1], info[2], info[3], info[0])
                        elif service == 'autoscaling_groups':
                            pass
                        elif service == 'sns_topics':
                            self.create_sns_topic(info[1], info[0])
                        elif service == 'sns_subscriptions':
                            self.create_sns_subscription(info[1], info[2], info[3], info[0])
                        elif service == 'cloudwatch_metric_filters':
                            print(info)
                            self.create_cloudwatch_metric_filter(info[1], info[0])
                        elif service == 'cloudwatch_dashboards':
                            # self.get_ecs_instance_ids()
                            self.create_cloudwatch_dashboard(info[1], info[0])
                        elif service == 'cloudwatch_alarms':
                            # self.get_ecs_instance_ids()
                            # print(info)
                            self.create_cloudwatch_alarm(info[1], info[2], info[3], info[4], info[5], info[0])
                        elif service == 'cloudwatchevents_rules':
                            self.create_cloudwatchevent_rule(info[1], info[2], info[0])
                        elif service == 'cloudwatchevents_rule_targets':
                            self.put_cloudwatchevent_rule_target(info[1], info[2], info[3], info[4], info[5], info[0])
                        else:
                            print("%s Service %s %s does not create because it is not in scope!" % (datetime.now(), service, item))
                print("%s Service %s creation is done." % (datetime.now(), service))
        print("%s Infrastructure deployment is done." % (datetime.now()))


if __name__ == '__main__':
    app = DevopsChain()
    app.main()
