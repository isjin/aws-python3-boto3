from function import aws_ec2, aws_ecs, aws_ecr, aws_cloudformation, aws_sns, aws_cloudwatch, aws_rds, aws_elb, aws_elasticache, aws_lambda
from function import aws_autoscaling
import json
import os

resource_path = 'resouces_list.txt'
filters = []
owner_id = '952375741452'


class GetResources(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.rds = aws_rds.AWSRDS()
        self.ecs = aws_ecs.AWSECS()
        self.ecr = aws_ecr.AWSECR()
        self.elb = aws_elb.AWSELB()
        self.autoscaling = aws_autoscaling.AWSAutoScaling()
        self.lambda_function = aws_lambda.AWSLambda()
        self.elasticache = aws_elasticache.AWSElastiCache()
        self.cf = aws_cloudformation.AWSCloudFormation()
        self.sns = aws_sns.AWSSNS()
        self.cloudwatch = aws_cloudwatch.AWSCloudWatch()
        self.resources = {}
        self.init_resources()

    def init_resources(self):
        if os.path.exists(resource_path):
            os.remove(resource_path)
        if os.path.exists(resource_path):
            f = open(resource_path, 'r')
            data = f.read()
            f.close()
            if len(data) > 0:
                self.resources = json.loads(data)
        else:
            self.resources['resource'] = {}
            self.resources['resource']['path'] = resource_path
            self.resources['cloudformations'] = {}
            self.resources['cloudwatch_dashboards'] = {}
            self.resources['cloudwatch_alarms'] = {}
            self.resources['sns_subscriptions'] = {}
            self.resources['sns_topics'] = {}
            self.resources['ec2_instances'] = {}
            self.resources['ecs_clusters'] = {}
            self.resources['ecs_services'] = {}
            self.resources['ecs_task_definitions'] = {}
            self.resources['ecr_repositories'] = {}
            self.resources['lambda_functions'] = {}
            self.resources['rds'] = {}
            self.resources['elasticaches'] = {}
            self.resources['igws'] = {}
            self.resources['ngws'] = {}
            self.resources['rtbs'] = {}
            self.resources['nacls'] = {}
            self.resources['roles'] = {}
            self.resources['keypairs'] = {}
            self.resources['autoscaling_groups'] = {}
            self.resources['autoscaling_launch_configurations'] = {}
            self.resources['eips'] = {}
            self.resources['volumes'] = {}
            self.resources['snapshots'] = {}
            self.resources['images'] = {}
            self.resources['elbs'] = {}
            self.resources['elb_target_groups'] = {}
            self.resources['security_groups'] = {}
            self.resources['subnets'] = {}
            self.resources['vpcs'] = {}
            self.write_file()

    @staticmethod
    def read_file(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)
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

    def get_vpcs(self):
        vpcs_info = self.ec2.ec2_vpcs_describe(filters)
        for i in range(len(vpcs_info)):
            vpc_keyname = 'vpc' + str(i + 1)
            vpc_id = vpcs_info[i]['VpcId']
            vpc_cidr = vpcs_info[i]['CidrBlock']
            self.resources['vpcs'][vpc_keyname] = {}
            self.resources['vpcs'][vpc_keyname]['VpcId'] = vpc_id
            self.resources['vpcs'][vpc_keyname]['CidrBlock'] = vpc_cidr
        self.write_file()

    def get_subnets(self):
        subnets_info = self.ec2.ec2_subnets_describe(filters)
        for i in range(len(subnets_info)):
            subnet_keyname = 'subnet' + str(i + 1)
            subnet_id = subnets_info[i]['SubnetId']
            subnet_cidr = subnets_info[i]['CidrBlock']
            subnet_az = subnets_info[i]['AvailabilityZone']
            subnet_arn = subnets_info[i]['SubnetArn']
            self.resources['subnets'][subnet_keyname] = {}
            self.resources['subnets'][subnet_keyname]['SubnetId'] = subnet_id
            self.resources['subnets'][subnet_keyname]['CidrBlock'] = subnet_cidr
            self.resources['subnets'][subnet_keyname]['AvailabilityZone'] = subnet_az
            self.resources['subnets'][subnet_keyname]['SubnetArn'] = subnet_arn
        self.write_file()

    def get_igws(self):
        igws_info = self.ec2.ec2_internet_gateways_describe(filters)
        for i in range(len(igws_info)):
            igw_keyname = 'igw' + str(i + 1)
            igw_id = igws_info[i]['InternetGatewayId']
            self.resources['igws'][igw_keyname] = {}
            self.resources['igws'][igw_keyname]['InternetGatewayId'] = igw_id
        self.write_file()

    def get_ngw(self):
        pass

    def get_route_tables(self):
        rtbs_info = self.ec2.ec2_route_tables_describe(filters)
        for i in range(len(rtbs_info)):
            rtb_keyname = 'rtb' + str(i + 1)
            rtb_id = rtbs_info[i]['RouteTableId']
            self.resources['rtbs'][rtb_keyname] = {}
            self.resources['rtbs'][rtb_keyname]['RouteTableId'] = rtb_id
        self.write_file()

    def get_network_acls(self):
        nacls_info = self.ec2.ec2_network_acls_describe(filters)
        for i in range(len(nacls_info)):
            nacl_keyname = 'nacl' + str(i + 1)
            nacl_id = nacls_info[i]['NetworkAclId']
            self.resources['nacls'][nacl_keyname] = {}
            self.resources['nacls'][nacl_keyname]['NetworkAclId'] = nacl_id
        self.write_file()

    def get_keypairs(self):
        keypairs_info = self.ec2.ec2_key_pairs_describe(filters)
        for i in range(len(keypairs_info)):
            keypair_keyname = 'keypair' + str(i + 1)
            keypair_name = keypairs_info[i]['KeyName']
            self.resources['keypairs'][keypair_keyname] = {}
            self.resources['keypairs'][keypair_keyname]['KeyName'] = keypair_name
        self.write_file()

    def get_security_groups(self):
        sgs_info = self.ec2.ec2_security_groups_describe(filters)
        for i in range(len(sgs_info)):
            sg_keyname = 'sg' + str(i + 1)
            sg_id = sgs_info[i]['GroupId']
            self.resources['security_groups'][sg_keyname] = {}
            self.resources['security_groups'][sg_keyname]['GroupId'] = sg_id
        self.write_file()

    def get_ec2_instances(self):
        ec2_instances_info = self.ec2.ec2_instances_describe(filters)
        for i in range(len(ec2_instances_info)):
            ec2_instance_keyname = 'ec2_instance' + str(i + 1)
            ec2_instance_id = ec2_instances_info[i]['Instances'][0]['InstanceId']
            self.resources['ec2_instances'][ec2_instance_keyname] = {}
            self.resources['ec2_instances'][ec2_instance_keyname]['InstanceId'] = ec2_instance_id
        self.write_file()

    def get_eips(self):
        eips_info = self.ec2.ec2_eips_describe(filters)
        for i in range(len(eips_info)):
            eip_keyname = 'eip' + str(i + 1)
            self.resources['eips'][eip_keyname] = {}
            eip_allocation_id = eips_info[i]['AllocationId']
            eip_ip = eips_info[i]['PublicIp']
            self.resources['eips'][eip_keyname]['AllocationId'] = eip_allocation_id
            self.resources['eips'][eip_keyname]['PublicIp'] = eip_ip
            if 'AssociationId' in eips_info[i].keys():
                eip_association_id = eips_info[i]['AssociationId']
                self.resources['eips'][eip_keyname]['AssociationId'] = eip_association_id
        self.write_file()

    def get_volumes(self):
        volumes_info = self.ec2.ec2_volumes_describe(filters)
        for i in range(len(volumes_info)):
            volume_keyname = 'volume' + str(i + 1)
            volume_id = volumes_info[i]['VolumeId']
            volume_type = volumes_info[i]['VolumeType']
            volume_status = volumes_info[i]['State']
            self.resources['volumes'][volume_keyname] = {}
            self.resources['volumes'][volume_keyname]['VolumeId'] = volume_id
            self.resources['volumes'][volume_keyname]['VolumeType'] = volume_type
            self.resources['volumes'][volume_keyname]['State'] = volume_status
        self.write_file()

    def get_snapshots(self):
        filter2 = [
            {
                'Name': 'owner-alias',
                'Values': [
                    'self',
                ]
            },
        ]
        snapshots_info = self.ec2.ec2_snapshots_describe(filter2)
        for i in range(len(snapshots_info)):
            snapshot_keyname = 'snapshot' + str(i + 1)
            snapshot_id = snapshots_info[i]['SnapshotId']
            self.resources['snapshots'][snapshot_keyname] = {}
            self.resources['snapshots'][snapshot_keyname]['SnapshotId'] = snapshot_id
        self.write_file()

    def get_images(self):
        filter2 = [
            {
                'Name': 'owner-id',
                'Values': [
                    owner_id,
                ]
            }
        ]
        images_info = self.ec2.ec2_images_describe(filter2)
        for i in range(len(images_info)):
            image_keyname = 'image' + str(i + 1)
            image_id = images_info[i]['ImageId']
            self.resources['images'][image_keyname] = {}
            self.resources['images'][image_keyname]['imageId'] = image_id
        self.write_file()

    def get_elbs(self):
        elbs_info = self.elb.elbv2_load_balancers_describe()
        for i in range(len(elbs_info)):
            elb_info = elbs_info[i]
            elb_keyname = 'elb' + str(i + 1)
            elb_arn = elb_info['LoadBalancerArn']
            elb_dns_name = elb_info['DNSName']
            elb_name = elb_info['LoadBalancerName']
            self.resources['elbs'][elb_keyname] = {}
            self.resources['elbs'][elb_keyname]['LoadBalancerArn'] = elb_arn
            self.resources['elbs'][elb_keyname]['DNSName'] = elb_dns_name
            self.resources['elbs'][elb_keyname]['LoadBalancerName'] = elb_name
        self.write_file()

    def get_elb_target_groups(self):
        target_groups_info = self.elb.elbv2_target_groups_describe()
        for i in range(len(target_groups_info)):
            target_group_info = target_groups_info[i]
            # print(target_group_info)
            tg_keyname = 'elb_tg' + str(i + 1)
            tg_arn = target_group_info['TargetGroupArn']
            tg_name = target_group_info['TargetGroupName']
            self.resources['elb_target_groups'][tg_keyname] = {}
            self.resources['elb_target_groups'][tg_keyname]['TargetGroupArn'] = tg_arn
            self.resources['elb_target_groups'][tg_keyname]['TargetGroupName'] = tg_name
            if len(target_group_info['LoadBalancerArns']) != 0:
                tg_elb = target_group_info['LoadBalancerArns'][0]
                self.resources['elb_target_groups'][tg_keyname]['LoadBalancerArns'] = tg_elb
        self.write_file()

    def get_auto_scaling_group(self):
        autoscaling_groups_info=self.autoscaling.autoscaling_auto_scaling_groups_describe()
        for i in range(len(autoscaling_groups_info)):
            autoscaling_group_keyname = 'autoscaling_group'+str(i+1)
            autoscaling_group_info = autoscaling_groups_info[i]
            # print(autoscaling_group_info)
            autoscaling_group_name = autoscaling_group_info['AutoScalingGroupName']
            autoscaling_group_arn = autoscaling_group_info['AutoScalingGroupARN']
            launch_configuration_name = autoscaling_group_info['LaunchConfigurationName']
            self.resources['autoscaling_groups'][autoscaling_group_keyname] = {}
            self.resources['autoscaling_groups'][autoscaling_group_keyname]['AutoScalingGroupName'] = autoscaling_group_name
            self.resources['autoscaling_groups'][autoscaling_group_keyname]['AutoScalingGroupARN'] = autoscaling_group_arn
            self.resources['autoscaling_groups'][autoscaling_group_keyname]['LaunchConfigurationName'] = launch_configuration_name
        self.write_file()

    def get_auto_scaling_launch_configurations(self):
        autoscaling_launch_configurations_info=self.autoscaling.autoscaling_launch_configurations_describe()
        for i in range(len(autoscaling_launch_configurations_info)):
            autoscaling_launch_configuration_keyname = 'autoscaling_launch_configuration'+str(i+1)
            autoscaling_launch_configuration_info = autoscaling_launch_configurations_info[i]
            # print(autoscaling_launch_configuration_info)
            autoscaling_launch_configuration_name = autoscaling_launch_configuration_info['LaunchConfigurationName']
            autoscaling_launch_configuration_arn = autoscaling_launch_configuration_info['LaunchConfigurationARN']
            self.resources['autoscaling_launch_configurations'][autoscaling_launch_configuration_keyname] = {}
            self.resources['autoscaling_launch_configurations'][autoscaling_launch_configuration_keyname]['LaunchConfigurationARN'] = autoscaling_launch_configuration_arn
            self.resources['autoscaling_launch_configurations'][autoscaling_launch_configuration_keyname]['LaunchConfigurationName'] = autoscaling_launch_configuration_name
        self.write_file()

    def get_ecs_clusters(self):
        ecs_clusters_info = self.ecs.ecs_clusters_list()
        for i in range(len(ecs_clusters_info)):
            ecs_cluster_keyname = 'ecs_cluster' + str(i + 1)
            ecs_cluster_arn = ecs_clusters_info[i]
            ecs_cluster_name = str(ecs_cluster_arn).split('/')[1]
            self.resources['ecs_clusters'][ecs_cluster_keyname] = {}
            self.resources['ecs_clusters'][ecs_cluster_keyname]['clusterArn'] = ecs_cluster_arn
            self.resources['ecs_clusters'][ecs_cluster_keyname]['clusterName'] = ecs_cluster_name
            self.resources['ecs_clusters'][ecs_cluster_keyname]['ecs_services'] = {}
            self.get_ecs_services(ecs_cluster_keyname, ecs_cluster_name)
        self.write_file()

    def get_ecs_task_definitions(self):
        ecs_task_definitions_info = self.ecs.ecs_task_definitions_list()
        for i in range(len(ecs_task_definitions_info)):
            ecs_task_definition_keyname = 'task_definition_arn' + str(i + 1)
            ecs_task_definition_arn = ecs_task_definitions_info[i]
            self.resources['ecs_task_definitions'][ecs_task_definition_keyname] = {}
            self.resources['ecs_task_definitions'][ecs_task_definition_keyname]['taskDefinitionArns'] = ecs_task_definition_arn
        self.write_file()

    def get_ecs_services(self, ecs_cluster_keyname, cluster_name):
        ecs_services_info = self.ecs.ecs_services_list(cluster_name)
        for i in range(len(ecs_services_info)):
            ecs_service_keyname = 'ecs_service_arn' + str(i + 1)
            self.resources['ecs_clusters'][ecs_cluster_keyname]['ecs_services'][ecs_service_keyname] = ecs_services_info[i]
            self.resources['ecs_services'][ecs_service_keyname] = {}
            self.resources['ecs_services'][ecs_service_keyname]['serviceArn'] = ecs_services_info[i]

    def get_ecr_repositories(self):
        repositories_info = self.ecr.repositories_describe()
        for i in range(len(repositories_info)):
            repository_keyname = 'ecr' + str(i + 1)
            repository_arn = repositories_info[i]['repositoryArn']
            repository_uri = repositories_info[i]['repositoryUri']
            repository_name = repositories_info[i]['repositoryName']
            self.resources['ecr_repositories'][repository_keyname] = {}
            self.resources['ecr_repositories'][repository_keyname]['repositoryArn'] = repository_arn
            self.resources['ecr_repositories'][repository_keyname]['repositoryUri'] = repository_uri
            self.resources['ecr_repositories'][repository_keyname]['repositoryName'] = repository_name
        self.write_file()

    def get_cloudformations(self):
        cfs_info = self.cf.cloudformation_stacks_describe()
        for i in range(len(cfs_info)):
            stack_keyname = 'stack' + str(i + 1)
            stack_id = cfs_info[i]['StackId']
            stack_name = cfs_info[i]['StackName']
            self.resources['cloudformations'][stack_keyname] = {}
            self.resources['cloudformations'][stack_keyname]['StackId'] = stack_id
            self.resources['cloudformations'][stack_keyname]['StackName'] = stack_name
        self.write_file()

    def get_cloudwatch_dashboards(self):
        dashboards_info = self.cloudwatch.cloudwatch_dashboards_list()
        for i in range(len(dashboards_info)):
            dashboard_keyname = 'dashboard' + str(i + 1)
            dashboard_name = dashboards_info[i]['DashboardName']
            self.resources['cloudwatch_dashboards'][dashboard_keyname] = {}
            self.resources['cloudwatch_dashboards'][dashboard_keyname]['DashboardName'] = dashboard_name
        self.write_file()

    def get_cloudwatch_alarms(self):
        alarms_info = self.cloudwatch.cloudwatch_alarms_describe()
        for i in range(len(alarms_info)):
            alarm_keyname = 'alarm' + str(i + 1)
            alarm_name = alarms_info[i]['AlarmName']
            self.resources['cloudwatch_alarms'][alarm_keyname] = {}
            self.resources['cloudwatch_alarms'][alarm_keyname]['AlarmName'] = alarm_name
        self.write_file()

    def get_sns_topics(self):
        sns_topics_info = self.sns.sns_topics_list()
        for i in range(len(sns_topics_info)):
            sns_topic_keyname = 'topic' + str(i + 1)
            sns_topic_arn = sns_topics_info[i]['TopicArn']
            self.resources['sns_topics'][sns_topic_keyname] = {}
            self.resources['sns_topics'][sns_topic_keyname]['TopicArn'] = sns_topic_arn
        self.write_file()

    def get_sns_subscriptions(self):
        for topic_info in self.resources['sns_topics'].values():
            sns_subscriptions_info = self.sns.sns_subscriptions_by_topic_list(topic_info['TopicArn'])
            for i in range(len(sns_subscriptions_info)):
                sns_subscription_keyname = 'subscription' + str(i + 1)
                sns_subscription_arn = sns_subscriptions_info[i]['SubscriptionArn']
                sns_subscription_protocol = sns_subscriptions_info[i]['Protocol']
                sns_subscription_endpoint = sns_subscriptions_info[i]['Endpoint']
                self.resources['sns_subscriptions'][sns_subscription_keyname] = {}
                self.resources['sns_subscriptions'][sns_subscription_keyname]['SubscriptionArn'] = sns_subscription_arn
                self.resources['sns_subscriptions'][sns_subscription_keyname]['Protocol'] = sns_subscription_protocol
                self.resources['sns_subscriptions'][sns_subscription_keyname]['Endpoint'] = sns_subscription_endpoint
                self.resources['sns_subscriptions'][sns_subscription_keyname]['TopicArn'] = topic_info['TopicArn']
            self.write_file()

    def get_rds(self):
        rds_info = self.rds.rds_instances_describe()
        for i in range(len(rds_info)):
            db_info = rds_info[i]
            rds_keyname = 'rds' + str(i + 1)
            rds_name = db_info['DBInstanceIdentifier']
            self.resources['rds'][rds_keyname] = {}
            self.resources['rds'][rds_keyname]['DBInstanceIdentifier'] = rds_name
        self.write_file()

    def get_elasticaches(self):
        elasticaches_info = self.elasticache.elasticache_cache_clusters_describe()
        for i in range(len(elasticaches_info)):
            elasticache_info = elasticaches_info[i]
            elasticache_keyname = 'elasticache' + str(i + 1)
            elasticache_cache_cluster_id = elasticache_info['CacheClusterId']
            self.resources['elasticaches'][elasticache_keyname] = {}
            self.resources['elasticaches'][elasticache_keyname]['CacheClusterId'] = elasticache_cache_cluster_id
        self.write_file()

    def get_lambda_functions(self):
        lambda_functions_info = self.lambda_function.lambda_functions_list()
        for i in range(len(lambda_functions_info)):
            lambda_function_info = lambda_functions_info[i]
            lambda_function_keyname = 'function' + str(i + 1)
            lambda_function_name = lambda_function_info['FunctionName']
            lambda_function_arn = lambda_function_info['FunctionArn']
            self.resources['lambda_functions'][lambda_function_keyname] = {}
            self.resources['lambda_functions'][lambda_function_keyname]['FunctionName'] = lambda_function_name
            self.resources['lambda_functions'][lambda_function_keyname]['FunctionArn'] = lambda_function_arn
        self.write_file()

    def main(self):
        self.get_vpcs()
        self.get_subnets()
        self.get_igws()
        self.get_ngw()
        self.get_route_tables()
        self.get_network_acls()
        self.get_keypairs()
        self.get_security_groups()
        self.get_ec2_instances()
        self.get_eips()
        self.get_volumes()
        self.get_snapshots()
        self.get_images()
        self.get_elbs()
        self.get_elb_target_groups()
        self.get_auto_scaling_group()
        self.get_auto_scaling_launch_configurations()
        self.get_ecs_clusters()
        self.get_ecs_task_definitions()
        self.get_ecr_repositories()
        self.get_cloudformations()
        self.get_cloudwatch_dashboards()
        self.get_cloudwatch_alarms()
        self.get_sns_topics()
        self.get_sns_subscriptions()
        self.get_rds()
        self.get_elasticaches()
        self.get_lambda_functions()
        os.system('python generate_resources_config.py')


if __name__ == '__main__':
    app = GetResources()
    app.main()
    # app.get_cloudwatch_alarms()
