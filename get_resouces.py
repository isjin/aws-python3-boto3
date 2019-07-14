from function import aws_ec2, aws_ecs, aws_ecr, aws_cloudformation
import json
import os

resource_path = 'resouces_list.txt'
filters = []
owner_id = '952375741452'


class GetResources(object):
    def __init__(self):
        self.ec2 = aws_ec2.AWSEC2()
        self.ecs = aws_ecs.AWSECS()
        self.ecr = aws_ecr.AWSECR()
        self.cf = aws_cloudformation.AWSCloudFormation()
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
            self.resources['vpcs'] = {}
            self.resources['subnets'] = {}
            self.resources['igws'] = {}
            self.resources['ngws'] = {}
            self.resources['rtbs'] = {}
            self.resources['nacls'] = {}
            self.resources['keypairs'] = {}
            self.resources['security_groups'] = {}
            self.resources['ec2_instances'] = {}
            self.resources['eips'] = {}
            self.resources['volumes'] = {}
            self.resources['snapshots'] = {}
            self.resources['images'] = {}
            self.resources['elbs'] = {}
            self.resources['auto_scaling'] = {}
            self.resources['ecs_clusters'] = {}
            self.resources['ecs_task_definitions'] = {}
            self.resources['ecr_repositories'] = {}
            self.resources['cloudformations'] = {}
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
        Filters = [
            {
                'Name': 'owner-alias',
                'Values': [
                    'self ',
                ]
            },
        ]
        snapshots_info = self.ec2.ec2_snapshots_describe(Filters)
        for i in range(len(snapshots_info)):
            snapshot_keyname = 'snapshot' + str(i + 1)
            snapshot_id = snapshots_info[i]['SnapshotId']
            self.resources['snapshots'][snapshot_keyname] = {}
            self.resources['snapshots'][snapshot_keyname]['SnapshotId'] = snapshot_id
        self.write_file()

    def get_images(self):
        Filters = [
            {
                'Name': 'owner-id',
                'Values': [
                    owner_id,
                ]
            }
        ]
        images_info = self.ec2.ec2_images_describe(Filters)
        for i in range(len(images_info)):
            image_keyname = 'image' + str(i + 1)
            image_id = images_info[i]['ImageId']
            self.resources['images'][image_keyname] = {}
            self.resources['images'][image_keyname]['imageId'] = image_id
        self.write_file()

    def get_elbs(self):
        pass

    def get_auto_scaling(self):
        pass

    def get_ecs_clusters(self):
        ecs_clusters_info = self.ecs.ecs_clusters_list()
        for i in range(len(ecs_clusters_info)):
            ecs_cluster_keyname = 'cluster_arn' + str(i + 1)
            ecs_cluster_arn = ecs_clusters_info[i]
            self.resources['ecs_clusters'][ecs_cluster_keyname] = {}
            self.resources['ecs_clusters'][ecs_cluster_keyname]['ClusterArn'] = ecs_cluster_arn
        self.write_file()

    def get_ecs_task_definitions(self):
        ecs_task_definitions_info = self.ecs.ecs_task_definition_list()
        for i in range(len(ecs_task_definitions_info)):
            ecs_task_definition_keyname = 'task_definition_arn' + str(i + 1)
            ecs_task_definition_arn = ecs_task_definitions_info[i]
            self.resources['ecs_task_definitions'][ecs_task_definition_keyname] = {}
            self.resources['ecs_task_definitions'][ecs_task_definition_keyname]['taskDefinitionArns'] = ecs_task_definition_arn
        self.write_file()

    def get_ecr_repositories(self):
        repositories_info = self.ecr.repositories_describe()
        for i in range(len(repositories_info)):
            repository_keyname = 'repository_arn' + str(i + 1)
            repository_arn = repositories_info[i]['repositoryArn']
            repository_uri = repositories_info[i]['repositoryUri']
            self.resources['ecr_repositories'][repository_keyname] = {}
            self.resources['ecr_repositories'][repository_keyname]['repositoryArn'] = repository_arn
            self.resources['ecr_repositories'][repository_keyname]['repositoryUri'] = repository_uri
        self.write_file()

    def get_cloudformations(self):
        cfs_info = self.cf.cloudformation_stacks_describe()
        for i in range(len(cfs_info)):
            stack_keyname = 'stack' + str(i + 1)
            stack_id = cfs_info[i]['StackId']
            stack_name = cfs_info[i]['StackName']
            self.resources['cfs'][stack_keyname] = {}
            self.resources['cfs'][stack_keyname]['StackId'] = stack_id
            self.resources['cfs'][stack_keyname]['StackName'] = stack_name
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
        self.get_auto_scaling()
        self.get_ecs_clusters()
        self.get_ecs_task_definitions()
        self.get_ecr_repositories()
        self.get_cloudformations()


if __name__ == '__main__':
    app = GetResources()
    app.main()
