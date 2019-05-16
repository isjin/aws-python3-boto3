import boto3
import os


class AWSEC2(object):
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')

    # def ec2_vpc_create(self, cidr, tags):
    #     response = self.ec2_client.create_vpc(
    #         CidrBlock=cidr,
    #         InstanceTenancy='default'
    #     )
    #     print(response)
    #     vpcid = response['Vpc']['VpcId']
    #     self.ec2_tags_create(vpcid, tags)
    #     return vpcid

    def ec2_vpc_create(self, vpc_info):
        # vpc_info = {
        #     'CidrBlock': '192.168.0.0/24',
        #     'Tags': [
        #         {
        #             'Key': 'Name',
        #             'Value': 'test'
        #         },
        #     ],
        # }
        response = self.ec2_client.create_vpc(
            CidrBlock=vpc_info['CidrBlock'],
            InstanceTenancy='default'
        )
        print(response)
        vpcid = response['Vpc']['VpcId']
        self.ec2_tags_create(vpcid, vpc_info['Tags'])
        return vpcid

    def ec2_vpc_delete(self, vpcid):
        response = self.ec2_client.delete_vpc(
            VpcId=vpcid,
        )
        print(response)

    def ec2_vpc_describe(self, vpcid):
        response = self.ec2_client.describe_vpcs(
            VpcIds=[vpcid, ],
        )
        return response['Vpcs'][0]

    def ec2_vpcs_describe(self, filters):
        response = self.ec2_client.describe_vpcs(
            Filters=filters,
        )
        return response['Vpcs']

    def ec2_vpc_peering_connect_create(self, vpc_peering_info):
        # vpc_peering_info={
        #     'PeerOwnerId':'168677335524',
        #     'PeerVpcId':'vpc-id',
        #     'VpcId':'vpc-id',
        #     'PeerRegion':'cn-north-1',
        #      'tags': [{'Key': 'Name', 'Value': 'vpc-to-vpc'}],
        # }
        response = self.ec2_client.create_vpc_peering_connection(
            PeerOwnerId=vpc_peering_info['PeerOwnerId'],
            PeerVpcId=vpc_peering_info['PeerVpcId'],
            VpcId=vpc_peering_info['VpcId'],
            PeerRegion=vpc_peering_info['PeerRegion']
        )
        vpc_peering_connection_id = response['VpcPeeringConnection']['VpcPeeringConnectionId']
        self.ec2_tags_create(vpc_peering_connection_id, vpc_peering_info['tags'])
        return vpc_peering_connection_id

    def ec2_vpc_peering_connect_delete(self, vpc_peering_connectid):
        response = self.ec2_client.delete_vpc_peering_connection(
            VpcPeeringConnectionId=vpc_peering_connectid
        )
        print(response)

    def ec2_vpc_peering_connect_accept(self, vpc_peering_connection_id):
        response = self.ec2_client.accept_vpc_peering_connection(
            VpcPeeringConnectionId=vpc_peering_connection_id
        )
        print(response)

    def ec2_tag_create(self, resource_id, tag_info):
        # tag_info = {
        #     'tag': 'Name',
        #     'tag_description': 'test'
        # }
        response = self.ec2_client.create_tags(
            Resources=[
                resource_id,
            ],
            Tags=[
                {
                    'Key': tag_info['tag'],
                    'Value': tag_info['tag_description'],
                },
            ]
        )
        print(response)

    def ec2_tags_create(self, resource_id, tags):
        # tags=[
        #     {
        #         'Key':'Name',
        #         'Value':'test'
        #     },
        #     {
        #         'Key': 'Name',
        #         'Value': 'test'
        #     },
        # ]
        response = self.ec2_client.create_tags(
            Resources=[
                resource_id,
            ],
            Tags=tags
        )
        print(response)

    def ec2_subnet_create(self, subnet_info):
        # subnet2_info = {
        #     'zone': 'cn-north-1b',
        #     'cidr': '10.20.2.16/28',
        #     'vpc': self.vpcid,
        #     'tags': [
        #         {
        #             'Key': 'System',
        #             'Value': 'test'
        #         },
        #         {
        #             'Key': 'Name',
        #             'Value': 'test'
        #         }
        #     ],
        # }
        response = self.ec2_client.create_subnet(
            AvailabilityZone=subnet_info['zone'],
            CidrBlock=subnet_info['cidr'],
            VpcId=subnet_info['vpc'],
        )
        print(response)
        subnetid = response['Subnet']['SubnetId']
        self.ec2_tags_create(subnetid, subnet_info['tags'])
        return subnetid

    def ec2_subnet_delete(self, subnetid):
        response = self.ec2_client.delete_subnet(
            SubnetId=subnetid,
        )
        print(response)

    def ec2_subnet_describe(self, subnetid):
        response = self.ec2_client.describe_subnets(
            SubnetIds=[
                subnetid,
            ],
        )
        return response['Subnets'][0]

    def ec2_subnets_describe(self, filters):
        response = self.ec2_client.describe_subnets(
            Filters=filters,
        )
        return response['Subnets']

    def ec2_route_table_create(self, routetableinfo):
        # route_table_info = {
        #     'VpcId': 'vpc-id',
        #     'Tags': [
        #         {
        #             'Key': 'Name',
        #             'Value': 'test'
        #         },
        #         {
        #             'Key': 'System',
        #             'Value': 'test'
        #         },
        #     ]
        # }
        response = self.ec2_client.create_route_table(
            VpcId=routetableinfo['VpcId']
        )
        route_id = response['RouteTable']['RouteTableId']
        self.ec2_tags_create(route_id, routetableinfo['Tags'])
        print(response)
        return route_id

    def ec2_route_table_delete(self, route_table_id):
        response = self.ec2_client.delete_route_table(
            RouteTableId=route_table_id
        )
        print(response)

    def ec2_route_add_egress_only_internet_gw(self, route_table_id, route_table_info):
        # route_table_info={
        #     'DestinationCidrBlock':'0.0.0.0/0',
        #     'EgressOnlyInternetGatewayId':'igw',
        # }
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route = route_table.create_route(
            DestinationCidrBlock=route_table_info['DestinationCidrBlock'],
            EgressOnlyInternetGatewayId=route_table_info['EgressOnlyInternetGatewayId'],
        )
        print(route)

    def ec2_route_add_gw(self, route_table_id, route_table_info):
        # route_table_info={
        #     'DestinationCidrBlock':'0.0.0.0/0',
        #     'GatewayId':'nid',
        # }
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route = route_table.create_route(
            DestinationCidrBlock=route_table_info['DestinationCidrBlock'],
            GatewayId=route_table_info['GatewayId'],
        )
        print(route)

    def ec2_route_add_instance(self, route_table_id, route_table_info):
        # route_table_info={
        #     'DestinationCidrBlock':'0.0.0.0/0',
        #     'InstanceId':'0.0.0.0/0',
        # }
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route = route_table.create_route(
            DestinationCidrBlock=route_table_info['DestinationCidrBlock'],
            InstanceId=route_table_info['InstanceId'],
        )
        print(route)

    def ec2_route_add_nat_gw(self, route_table_id, route_table_info):
        # route_table_info={
        #     'DestinationCidrBlock':'0.0.0.0/0',
        #     'NatGatewayId':'0.0.0.0/0',
        # }
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route = route_table.create_route(
            DestinationCidrBlock=route_table_info['DestinationCidrBlock'],
            NatGatewayId=route_table_info['NatGatewayId'],
        )
        print(route)

    def ec2_route_add_transit_gw(self, route_table_id, route_table_info):
        # route_table_info={
        #     'DestinationCidrBlock':'0.0.0.0/0',
        #     'TransitGatewayId':'0.0.0.0/0',
        # }
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route = route_table.create_route(
            DestinationCidrBlock=route_table_info['DestinationCidrBlock'],
            TransitGatewayId=route_table_info['TransitGatewayId'],
        )
        print(route)

    def ec2_route_add_network_interface(self, route_table_id, route_table_info):
        # route_table_info={
        #     'DestinationCidrBlock':'0.0.0.0/0',
        #     'NetworkInterfaceId':'0.0.0.0/0',
        # }
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route = route_table.create_route(
            DestinationCidrBlock=route_table_info['DestinationCidrBlock'],
            NetworkInterfaceId=route_table_info['NetworkInterfaceId'],
        )
        print(route)

    def ec2_route_add_vpcpeering(self, route_table_id, route_table_info):
        # route_table_info={
        #     'DestinationCidrBlock':'0.0.0.0/0',
        #     'VpcPeeringConnectionId':'0.0.0.0/0',
        # }
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route = route_table.create_route(
            DestinationCidrBlock=route_table_info['DestinationCidrBlock'],
            VpcPeeringConnectionId=route_table_info['VpcPeeringConnectionId'],
        )
        print(route)

    def ec2_route_table_subnet_associate(self, route_table_id, subnetid):
        route_table = self.ec2_resource.RouteTable(route_table_id)
        route_table_association = route_table.associate_with_subnet(
            SubnetId=subnetid
        )
        print(route_table_association)

    def ec2_eip_allocate(self, tags):
        # tags=[
        #     {
        #         'Key':'Name',
        #         'Value':'btest'
        #     },
        # ]
        response = self.ec2_client.allocate_address(
            Domain='vpc',
        )
        print(response)
        eipip = response['PublicIp']
        eipid = response['AllocationId']
        self.ec2_tags_create(eipid, tags)
        print(eipip, eipid)
        return eipid

    def ec2_eip_release(self, eipid):
        response = self.ec2_client.release_address(
            AllocationId=eipid,
        )
        print(response)

    def ec2_eip_associate_address(self, associate_info):
        # associate_info={
        #     'AllocationId':'eipalloc-id',
        #     'InstanceId':'i-id',
        #     'NetworkInterfaceId': 'interfaceid',
        # }
        response = self.ec2_client.associate_address(
            AllocationId=associate_info['AllocationId'],
            InstanceId=associate_info['InstanceId'],
            # PublicIp='string',
            # AllowReassociation=True | False,
            # DryRun=True | False,
            # NetworkInterfaceId=associate_info['NetworkInterfaceId'],
            # PrivateIpAddress='string'
        )
        print(response)

    def ec2_eip_disassociate_address(self, eipid):
        response = self.ec2_client.disassociate_address(
            AssociationId=eipid,
            # PublicIp=IP,
            # DryRun=True | False
        )
        print(response)

    def ec2_eip_describe(self, public_ip):
        response = self.ec2_client.describe_addresses(
            # Filters=[
            #     {
            #         'Name': 'string',
            #         'Values': [
            #             'string',
            #         ]
            #     },
            # ],
            PublicIps=[
                public_ip,
            ],
            # AllocationIds=[
            #     'string',
            # ],
            # DryRun=True | False
        )
        print(response)
        return response

    def ec2_internet_gateway_create(self, igw_info):
        response = self.ec2_client.create_internet_gateway(
        )
        print(response)
        igwid = response['InternetGateway']['InternetGatewayId']
        self.ec2_tags_create(igwid, igw_info['tags'])
        return igwid

    def ec2_internet_gateway_attach(self, internet_gatewayid, vpcid):
        response = self.ec2_client.attach_internet_gateway(
            InternetGatewayId=internet_gatewayid,
            VpcId=vpcid
        )
        print(response)

    def ec2_internet_gateway_delete(self, internet_gatewayid):
        response = self.ec2_client.delete_internet_gateway(
            InternetGatewayId=internet_gatewayid
        )
        print(response)

    def ec2_internet_gateway_describe(self, igw_id):
        response = self.ec2_client.describe_internet_gateways(
            InternetGatewayIds=[
                igw_id,
            ],
        )
        return response

    def ec2_internet_gateways_describe(self, filters):
        # filters = [
        #     {
        #         'Name': 'tag:System',
        #         'Values': [
        #             'test',
        #         ]
        #     },
        # ]
        response = self.ec2_client.describe_internet_gateways(
            Filters=filters,
        )
        return response['InternetGateways']

    def ec2_nat_gateway_create(self, nat_gateway_info):
        # nat_gateway_b_info = {
        #     'eipid': self.create_eip(tags_agw_eip_b),
        #     'subnetid': self.subnetid_2,
        #     'tags': [
        #         {
        #             'Key': 'Name',
        #             'Value': 'test',
        #         },
        #         {
        #             'Key': 'System',
        #             'Value': 'test'
        #         },
        #     ],
        # }
        response = self.ec2_client.create_nat_gateway(
            AllocationId=nat_gateway_info['eipid'],
            SubnetId=nat_gateway_info['subnetid']
        )
        print(response)
        nat_gatewayid = response['NatGateway']['NatGatewayId']
        self.ec2_tags_create(nat_gatewayid, nat_gateway_info['tags'])
        return nat_gatewayid

    def ec2_nat_gateway_delete(self, nat_gatewayid):
        response = self.ec2_client.delete_nat_gateway(
            NatGatewayId=nat_gatewayid
        )
        print(response)

    def ec2_nat_gateway_describe(self, ngw_id):
        response = self.ec2_client.describe_nat_gateways(
            NatGatewayIds=[
                ngw_id,
            ],
        )
        return response

    def ec2_nat_gateways_describe(self, filters):
        response = self.ec2_client.describe_nat_gateways(
            Filters=filters
        )
        return response['NatGateways']

    def ec2_security_group_create(self, sg_info):
        # sg_info = {
        #     'groupname': 'test-sg',
        #     'description': 'test-sg',
        #     'vpcid': 'vpc-id',
        #     'tags': [
        #         {
        #             'Key': 'Name',
        #             'Value': 'test'
        #         },
        #         {
        #             'Key': 'Name',
        #             'Value': 'test'
        #         },
        #     ]
        # }
        response = self.ec2_client.create_security_group(
            Description=sg_info['description'],
            GroupName=sg_info['groupname'],
            VpcId=sg_info['vpcid'],
        )
        print(response)
        sgid = response['GroupId']
        self.ec2_tags_create(sgid, sg_info['tags'])
        print(sgid)
        return sgid

    def ec2_security_group_delete(self, sgid):
        response = self.ec2_client.delete_security_group(
            GroupId=sgid,
        )
        print(response)

    def ec2_security_group_modify(self, info):
        # info = {
        #     'Groups': [
        #         'string',
        #     ],
        #     'InstanceId':''
        # }
        response = self.ec2_client.modify_instance_attribute(
            Groups=info['Groups'],
            InstanceId=info['InstanceId']
        )
        print(response)

    def ec2_security_group_describe(self, sgid):
        response = self.ec2_client.describe_security_groups(
            GroupIds=[
                sgid,
            ],
        )
        return response['SecurityGroups'][0]

    def ec2_security_groups_describe(self, filters):
        # filters = [
        #               {
        #                   'Name': 'string',
        #                   'Values': [
        #                       'string',
        #                   ]
        #               },
        #           ]
        response = self.ec2_client.describe_security_groups(
            Filters=filters,
        )
        return response['SecurityGroups']

    def ec2_security_group_outbound_policies_add(self, outbound):
        # inbound_info = {
        #     'securitygroupid': '{sgid}',
        #     'policy': [
        #         {
        #             'FromPort': 22,
        #             'IpProtocol': 'tcp',
        #             'IpRanges': [
        #                 {
        #                     'CidrIp': '0.0.0.0/0',
        #                     'Description': 'test'
        #                 },
        #             ],
        #             'ToPort': 22,
        #             'UserIdGroupPairs': [
        #                 {
        #                     'Description': 'string',
        #                     'GroupId': 'sg-063cd53fe5cdd4527',
        #                 },
        #             ]
        #         },
        #     ],
        # }
        security_group = self.ec2_resource.SecurityGroup(outbound['securitygroupid'])
        response = security_group.authorize_egress(
            IpPermissions=outbound['policy'],
        )
        print(response)

    def ec2_security_group_outbound_policies_revoke(self, outbound):
        # inbound_info = {
        #     'securitygroupid': '{sgid}',
        #     'policy': [
        #         {
        #             'FromPort': 22,
        #             'IpProtocol': 'tcp',
        #             'IpRanges': [
        #                 {
        #                     'CidrIp': '0.0.0.0/0',
        #                     'Description': 'test'
        #                 },
        #             ],
        #             'ToPort': 22,
        #             'UserIdGroupPairs': [
        #                 {
        #                     'Description': 'string',
        #                     'GroupId': 'sg-063cd53fe5cdd4527',
        #                 },
        #             ]
        #         },
        #     ],
        # }
        security_group = self.ec2_resource.SecurityGroup(outbound['securitygroupid'])
        response = security_group.revoke_ingress(
            IpPermissions=outbound['policy'],
        )
        print(response)

    def ec2_security_group_inbound_policies_add(self, inbound_info):
        # inbound_info = {
        #     'securitygroupid': '{sgid}',
        #     'policy': [
        #         {
        #             'FromPort': 22,
        #             'IpProtocol': 'tcp',
        #             'IpRanges': [
        #                 {
        #                     'CidrIp': '0.0.0.0/0',
        #                     'Description': 'test'
        #                 },
        #             ],
        #             'ToPort': 22,
        #             'UserIdGroupPairs': [
        #                 {
        #                     'Description': 'string',
        #                     'GroupId': 'sg-063cd53fe5cdd4527',
        #                 },
        #             ]
        #         },
        #     ],
        # }
        security_group = self.ec2_resource.SecurityGroup(inbound_info['securitygroupid'])
        response = security_group.authorize_ingress(
            IpPermissions=inbound_info['policy'],
        )
        print(response)

    def ec2_security_group_inbound_policies_revoke(self, inbound):
        # inbound_info = {
        #     'securitygroupid': '{sgid}',
        #     'policy': [
        #         {
        #             'FromPort': 22,
        #             'IpProtocol': 'tcp',
        #             'IpRanges': [
        #                 {
        #                     'CidrIp': '0.0.0.0/0',
        #                     'Description': 'test'
        #                 },
        #             ],
        #             'ToPort': 22,
        #             'UserIdGroupPairs': [
        #                 {
        #                     'Description': 'string',
        #                     'GroupId': 'sg-063cd53fe5cdd4527',
        #                 },
        #             ]
        #         },
        #     ],
        # }
        security_group = self.ec2_resource.SecurityGroup(inbound['securitygroupid'])
        response = security_group.revoke_ingress(
            IpPermissions=inbound['policy'],
        )
        print(response)

    def ec2_key_pair_create(self, key_name):
        response = self.ec2_client.create_key_pair(
            KeyName=key_name,
        )
        # print(response)
        key_pem = response['KeyMaterial']
        file = '%s.pem' % key_name
        if os.path.exists(file):
            os.remove(file)
        f = open(file, 'w')
        f.write(key_pem)
        f.close()

    def ec2_key_pair_delete(self, key_name):
        response = self.ec2_client.delete_key_pair(
            KeyName=key_name,
        )
        print(response)

    def ec2_volume_create(self, volume_info):
        response = self.ec2_client.create_volume(
            AvailabilityZone=volume_info['availabile_zone'],
            Size=volume_info['size'],
            VolumeType=volume_info['volume_type'],
            TagSpecifications=[
                {
                    'Tags': [
                        {
                            'Key': volume_info['tag'],
                            'Value': volume_info['tag_description']
                        },
                    ]
                },
            ]
        )
        print(response)
        volume_id = response['VolumeId']
        self.ec2_tag_create(volume_id, volume_info)
        print(volume_id)

    def ec2_volume_delete(self, volume_id):
        response = self.ec2_client.delete_volume(
            VolumeId=volume_id,
        )
        print(response)

    def ec2_volume_modify(self, volume_info):
        # volume_info = {
        #     'VolumeId': 'aa',
        #     'Size': 500,
        #     'VolumeType': 'gp2',
        # }
        response = self.ec2_client.modify_volume(
            # DryRun=True | False,
            VolumeId=volume_info['VolumeId'],
            Size=volume_info['Size'],
            # VolumeType='standard' | 'io1' | 'gp2' | 'sc1' | 'st1',
            VolumeType=volume_info['VolumeType'],
            # Iops=123
        )
        print(response)

    def ec2_volume_describe(self, volumeid):
        response = self.ec2_client.describe_volumes(
            VolumeIds=[
                volumeid,
            ],
        )
        return response['Volumes'][0]

    def ec2_instance_create(self, instance_info):
        # instance_info = {
        #     'BlockDeviceMappings': [
        #         {
        #             'DeviceName': '/dev/xvda',
        #             'Ebs': {
        #                 'DeleteOnTermination': True,
        #                 'VolumeSize': 10,
        #                 'VolumeType': 'gp2',
        #             },
        #         },
        #     ],
        #     # 'BlockDeviceMappings': [
        #     #     {
        #     #         'DeviceName': '/dev/xvda',
        #     #         'Ebs': {
        #     #             'DeleteOnTermination': True,
        #     #             'VolumeSize': 8,
        #     #             'VolumeType': 'gp2',
        #     #         },
        #     #         'NoDevice': 'string'
        #     #     },
        #     # ],
        #     'ImageId': 'ami-0cad3dea07a7c36f9',
        #     'InstanceType': 't2.micro',
        #     'maxcount': 1,
        #     'mincount': 1,
        #     'KeyName': key_pair,
        #     'SecurityGroupIds': ['sg-0a97d9150f2dfb4a8', ],
        #     'SubnetId': self.subnetid_1,
        #     'TagSpecifications': [
        #         {
        #             'ResourceType': 'instance',
        #             'Tags': [
        #                 {
        #                     'Key': 'Name',
        #                     'Value': 'test'
        #                 },
        #                 {
        #                     'Key': 'System',
        #                     'Value': 'WAF'
        #                 },
        #             ]
        #         },
        #         {
        #             'ResourceType': 'volume',
        #             'Tags': [
        #                 {
        #                     'Key': 'Name',
        #                     'Value': 'test'
        #                 },
        #                 {
        #                     'Key': 'System',
        #                     'Value': 'test'
        #                 },
        #             ]
        #         },
        #     ],
        # }
        response = self.ec2_client.run_instances(
            BlockDeviceMappings=instance_info['BlockDeviceMappings'],
            # BlockDeviceMappings=[
            #     {
            #         'DeviceName': 'string',
            #         'VirtualName': 'string',
            #         'Ebs': {
            #             'DeleteOnTermination': True | False,
            #             'Iops': 123,
            #             'SnapshotId': 'string',
            #             'VolumeSize': 123,
            #             'VolumeType': 'standard' | 'io1' | 'gp2' | 'sc1' | 'st1',
            #             'Encrypted': True | False,
            #             'KmsKeyId': 'string'
            #         },
            #         'NoDevice': 'string'
            #     },
            # ],
            ImageId=instance_info['ImageId'],
            InstanceType=instance_info['InstanceType'],
            # Ipv6AddressCount=123,
            # Ipv6Addresses=[
            #     {
            #         'Ipv6Address': 'string'
            #     },
            # ],
            # KernelId='string',
            KeyName=instance_info['KeyName'],
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': False
            },
            # Placement={
            #     'AvailabilityZone': 'string',
            #     'Affinity': 'string',
            #     'GroupName': 'string',
            #     'PartitionNumber': 123,
            #     'HostId': 'string',
            #     'Tenancy': 'default' | 'dedicated' | 'host',
            #     'SpreadDomain': 'string'
            # },
            # RamdiskId='string',
            SecurityGroupIds=instance_info['SecurityGroupIds'],
            # SecurityGroups=[
            #     'string',
            # ],
            SubnetId=instance_info['SubnetId'],
            # UserData='string',
            # AdditionalInfo='string',
            # ClientToken='string',
            # DisableApiTermination=True | False,
            # DryRun=True | False,
            # EbsOptimized=True | False,
            # IamInstanceProfile={
            #     'Arn': 'string',
            #     'Name': 'string'
            # },
            InstanceInitiatedShutdownBehavior='stop',
            # NetworkInterfaces=[
            # {
            # 'AssociatePublicIpAddress': True | False,
            # 'DeleteOnTermination': True | False,
            # 'Description': 'string',
            # 'DeviceIndex': 123,
            # 'Groups': [
            #     'string',
            # ],
            # 'Ipv6AddressCount': 123,
            # 'Ipv6Addresses': [
            #     {
            #         'Ipv6Address': 'string'
            #     },
            # ],
            # 'NetworkInterfaceId': 'string',
            # 'PrivateIpAddress': 'string',
            # 'PrivateIpAddresses': [
            #     {
            #         'Primary': True | False,
            #         'PrivateIpAddress': 'string'
            #     },
            # ],
            # 'SecondaryPrivateIpAddressCount': 123,
            # 'SubnetId': 'subnet-0b88d4d63456d0dad'
            # },
            # ],
            # PrivateIpAddress='string',
            # ElasticGpuSpecification=[
            #     {
            #         'Type': 'string'
            #     },
            # ],
            # ElasticInferenceAccelerators=[
            #     {
            #         'Type': 'string'
            #     },
            # ],
            TagSpecifications=instance_info['TagSpecifications']
            # TagSpecifications= [
            #     {
            #         'ResourceType': 'instance',
            #         'Tags': [
            #             {
            #                 'Key': 'Name',
            #                 'Value': 'waf-bastion-subnet-1a-ec2'
            #             },
            #             {
            #                 'Key': 'System',
            #                 'Value': 'WAF'
            #             },
            #         ]
            #     },
            #     {
            #         'ResourceType': 'volume',
            #         'Tags': [
            #             {
            #                 'Key': 'Name',
            #                 'Value': 'waf-bastion-subnet-1a-ec2'
            #             },
            #             {
            #                 'Key': 'System',
            #                 'Value': 'WAF'
            #             },
            #         ]
            #     },
            # ],
            # LaunchTemplate={
            #     'LaunchTemplateId': 'string',
            #     'LaunchTemplateName': 'string',
            #     'Version': 'string'
            # },
            # InstanceMarketOptions={
            #     'MarketType': 'spot',
            #     'SpotOptions': {
            #         'MaxPrice': 'string',
            #         'SpotInstanceType': 'one-time' | 'persistent',
            #         'BlockDurationMinutes': 123,
            #         'ValidUntil': datetime(2015, 1, 1),
            #         'InstanceInterruptionBehavior': 'hibernate' | 'stop' | 'terminate'
            #     }
            # },
            # CreditSpecification={
            #     'CpuCredits': 'string'
            # },
            # CpuOptions={
            #     'CoreCount': 123,
            #     'ThreadsPerCore': 123
            # },
            # CapacityReservationSpecification={
            #     'CapacityReservationPreference': 'open' | 'none',
            #     'CapacityReservationTarget': {
            #         'CapacityReservationId': 'string'
            #     }
            # },
            # HibernationOptions={
            #     'Configured': True | False
            # },
            # LicenseSpecifications=[
            #     {
            #         'LicenseConfigurationArn': 'string'
            #     },
            # ]
        )
        print(response)
        instanceids = []
        for instance in response['Instances']:
            instanceid = instance['InstanceId']
            # self.ec2_tag_create(instanceid, instance_info)
            instanceids.append(instanceid)
        return instanceids

    def ec2_instance_delete(self, instanceids):
        # instanceids is list
        response = self.ec2_client.terminate_instances(
            InstanceIds=instanceids,
        )
        print(response)

    def ec2_instance_stop(self, instanceids):
        response = self.ec2_client.stop_instances(
            InstanceIds=instanceids
        )
        print(response)

    def ec2_instance_start(self, instanceids):
        response = self.ec2_client.start_instances(
            InstanceIds=instanceids
        )
        print(response)

    def ec2_instance_describe(self, instanceid):
        response = self.ec2_client.describe_instances(
            InstanceIds=[
                instanceid,
            ],
        )
        return response['Reservations'][0]

    def ec2_instances_describe(self, filters):
        # filters = [
        #     {
        #         'Name': 'tag:System type',
        #         'Values': [
        #             'PROD',
        #         ]
        #     },
        # ]
        response = self.ec2_client.describe_instances(
            Filters=filters,
        )
        return response['Reservations']

    def get_instanceids(self, filters):
        instanceids = []
        instances_info = self.ec2_instances_describe(filters)
        for instance_info in instances_info:
            instanceids.append(instance_info['Instances'][0]['InstanceId'])
        return instanceids

    def ec2_snapshot_create(self, volumeid, description, tag_name_value):
        response = self.ec2_client.create_snapshot(
            Description=description,
            VolumeId=volumeid,
        )
        print(response)
        snapshotid = response['SnapshotId']
        tags = [
            {
                'Key': 'Name',
                'Value': tag_name_value
            },
        ]
        print(response)
        self.ec2_tags_create(snapshotid, tags)

    def ec2_snapshot_delete(self, snapshotid):
        response = self.ec2_client.delete_snapshot(
            SnapshotId=snapshotid,
        )
        print(response)

    def ec2_snapshot_describe(self, snapshotid):
        response = self.ec2_client.describe_snapshots(
            SnapshotIds=[
                snapshotid,
            ],
        )
        return response['Snapshots'][0]

    def ec2_snapshots_describe(self, filters):
        response = self.ec2_client.describe_snapshots(
            Filters=filters,
        )
        return response['Snapshots']

    def ec2_image_create(self, instance_info):
        # instance_info={
        #     'Description':'test',
        #     'Name':'test',
        #     'InstanceId':'i-id',
        #
        # }
        response = self.ec2_client.create_image(
            Description=instance_info['Description'],
            InstanceId=instance_info['InstanceId'],
            Name=instance_info['Description'],
            NoReboot=True
        )
        print(response)
        return response['ImageId']

    def ec2_register_image(self, snapshot_info):
        # snapshot_info={
        #     'DeviceName':'/dev/xvda',
        #     'Description':'test',
        #     'Name':'test',
        #     'SnapshotId':'snap-id',
        #     'RootDeviceName':'/dev/xvda',
        # }
        response = self.ec2_client.register_image(
            BlockDeviceMappings=[
                {
                    'DeviceName': snapshot_info['DeviceName'],
                    'Ebs': {
                        'SnapshotId': snapshot_info['SnapshotId'],
                    },
                },
            ],
            Description=snapshot_info['Description'],
            Name=snapshot_info['Name'],
            RootDeviceName=snapshot_info['RootDeviceName'],
        )
        print(response)
        return response['ImageId']

    def ec2_deregister_image(self, imageid):
        response = self.ec2_client.deregister_image(
            ImageId=imageid,
        )
        print(response)


if __name__ == '__main__':
    app = AWSEC2()
    app.ec2_key_pair_create('keypair')
    # app.ec2_deregister_image('ami-id')
