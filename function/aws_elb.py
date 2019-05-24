import boto3


class AWSELB(object):
    def __init__(self):
        self.elb_client = boto3.client('elb')
        self.elbv2_client = boto3.client('elbv2')

    def elb_tags_create(self, loadbalancer_name, tags):
        # tags = [
        #     {
        #         'Key': 'string',
        #         'Value': 'string'
        #     },
        # ]
        response = self.elb_client.add_tags(
            LoadBalancerNames=[
                loadbalancer_name,
            ],
            Tags=tags
        )
        print(response)

    def elbv2_tags_create(self, arn, tags):
        # tags=[
        #         {
        #             'Key': 'string',
        #             'Value': 'string'
        #         },
        #     ]
        response = self.elbv2_client.add_tags(
            ResourceArns=[
                arn,
            ],
            Tags=tags
        )
        print(response)

    def elb_load_balancer_create(self, elb_info):
        # elb_info = {
        #     'LoadBalancerName': 'bpm-prod-test',
        #     'Listeners': [
        #         {
        #             'Protocol': 'HTTP, HTTPS, TCP, or SSL',
        #             'LoadBalancerPort': 123,
        #             'InstanceProtocol': 'HTTP, HTTPS, TCP, or SSL',
        #             'InstancePort': 123,
        #             'SSLCertificateId': 'string'
        #         },
        #     ],
        #     'Subnets': [
        #         'string',
        #     ],
        #     'SecurityGroups': [
        #         'string',
        #     ],
        #     'Scheme': 'internal |Internet-facing',
        #     'Tags': [
        #         {
        #             'Key': 'string',
        #             'Value': 'string'
        #         },
        #     ]
        # }
        response = self.elb_client.create_load_balancer(
            LoadBalancerName=elb_info[''],
            Listeners=elb_info[''],
            # AvailabilityZones=[
            #     'string',
            # ],
            Subnets=elb_info['Subnets'],
            SecurityGroups=elb_info['SecurityGroups'],
            # Scheme='internal |Internet-facing',
            Scheme=elb_info['Scheme'],
            Tags=elb_info['Tags'],
        )
        print(response)
        return response

    def elbv2_load_balancer_create(self, elb_info):
        # elb_info={
        #     'Name':'bpm-prod-test',
        #     'Subnets':['subnet-0c2085fe6974c518c','subnet-05c6866bcc1315c27'],
        #     'SecurityGroups':[],
        #     'Scheme':'internal',
        #     'Tags':[
        #         {
        #             'Key': 'System',
        #             'Value': 'BPM'
        #         },
        #         {
        #             'Key': 'System type',
        #             'Value': 'PROD'
        #         },
        #     ],
        #     'Type': 'network',
        #
        # }
        response = self.elbv2_client.create_load_balancer(
            Name=elb_info['Name'],
            Subnets=elb_info['Subnets'],
            SecurityGroups=elb_info['SecurityGroups'],
            Scheme=elb_info['Scheme'],
            Tags=elb_info['Tags'],
            # Type='application' | 'network',
            Type=elb_info['Type'],
        )
        print(response)
        return response['LoadBalancers'][0]['LoadBalancerArn']

    def elb_load_balancer_delete(self, loadbalancer_name):
        response = self.elb_client.delete_load_balancer(
            LoadBalancerName=loadbalancer_name
        )
        print(response)

    def elbv2_load_balancer_delete(self, lbarn):
        response = self.elbv2_client.delete_load_balancer(
            LoadBalancerArn=lbarn
        )
        print(response)

    def elbv2_load_balancer_describe(self, elb_arn):
        response = self.elbv2_client.describe_load_balancers(
            LoadBalancerArns=[
                elb_arn,
            ],
        )
        return response['LoadBalancers'][0]

    def elbv2_load_balancers_describe(self):
        response = self.elbv2_client.describe_load_balancers(
        )
        return response

    def elbv2_listener_create(self, listeners_info):
        # listeners_info = {
        #     'LoadBalancerArn': 'arn:id',
        #     'Protocol': 'TCP',
        #     'Port': 22,
        #     'Certificates': [
        #         # {
        #         #     'CertificateArn': 'string',
        #         #     'IsDefault': True | False
        #         # },
        #     ],
        #     'Type': 'forward',
        #     'TargetGroupArn': 'arn:id',
        # }
        response = self.elbv2_client.create_listener(
            LoadBalancerArn=listeners_info['LoadBalancerArn'],
            # Protocol='HTTP' | 'HTTPS' | 'TCP' | 'TLS',
            Protocol=listeners_info['Protocol'],
            Port=listeners_info['Port'],
            # SslPolicy='string',
            Certificates=listeners_info['Certificates'],
            DefaultActions=[
                {
                    # 'Type': 'forward' | 'authenticate-oidc' | 'authenticate-cognito' | 'redirect' | 'fixed-response',
                    'Type': listeners_info['Type'],
                    'TargetGroupArn': listeners_info['TargetGroupArn'],
                    # 'AuthenticateOidcConfig': {
                    #     'Issuer': 'string',
                    #     'AuthorizationEndpoint': 'string',
                    #     'TokenEndpoint': 'string',
                    #     'UserInfoEndpoint': 'string',
                    #     'ClientId': 'string',
                    #     'ClientSecret': 'string',
                    #     'SessionCookieName': 'string',
                    #     'Scope': 'string',
                    #     'SessionTimeout': 123,
                    #     'AuthenticationRequestExtraParams': {
                    #         'string': 'string'
                    #     },
                    #     'OnUnauthenticatedRequest': 'deny' | 'allow' | 'authenticate',
                    #     'UseExistingClientSecret': True | False
                    # },
                    # 'AuthenticateCognitoConfig': {
                    #     'UserPoolArn': 'string',
                    #     'UserPoolClientId': 'string',
                    #     'UserPoolDomain': 'string',
                    #     'SessionCookieName': 'string',
                    #     'Scope': 'string',
                    #     'SessionTimeout': 123,
                    #     'AuthenticationRequestExtraParams': {
                    #         'string': 'string'
                    #     },
                    #     'OnUnauthenticatedRequest': 'deny' | 'allow' | 'authenticate'
                    # },
                    # 'Order': 123,
                    # 'RedirectConfig': {
                    #     'Protocol': 'string',
                    #     'Port': 'string',
                    #     'Host': 'string',
                    #     'Path': 'string',
                    #     'Query': 'string',
                    #     'StatusCode': 'HTTP_301' | 'HTTP_302'
                    # },
                    # 'FixedResponseConfig': {
                    #     'MessageBody': 'string',
                    #     'StatusCode': 'string',
                    #     'ContentType': 'string'
                    # }
                },
            ]
        )
        print(response)
        return response['Listeners'][0]['ListenerArn']

    def elbv2_listeners_delete(self, listenerarn):
        response = self.elbv2_client.delete_listener(
            ListenerArn=listenerarn
        )
        print(response)

    def elbv2_listener_describe(self, listener_arn):
        response = self.elbv2_client.describe_listeners(
            # LoadBalancerArn=lb_arn,
            ListenerArns=[
                listener_arn,
            ]
        )
        print(response)

    def elbv2_listeners_describe(self, lb_arn):
        response = self.elbv2_client.describe_listeners(
            LoadBalancerArn=lb_arn,
        )
        return response['Listeners']

    def elbv2_listener_certificates_add(self,certificate_info):
        # certificate_info={
        #     'ListenerArn':'',
        #     'Certificates':[
        #         {
        #             'CertificateArn': 'string',
        #         }
        #     ],
        # }
        response = self.elbv2_client.add_listener_certificates(
            ListenerArn=certificate_info['ListenerArn'],
            Certificates=certificate_info['Certificates'],
        )
        print(response)

    def elbv2_listener_certificates_remove(self,certificate_info):
        # certificate_info={
        #     'ListenerArn':'',
        #     'Certificates':[
        #         {
        #             'CertificateArn': 'string',
        #         }
        #     ],
        # }
        response = self.elbv2_client.remove_listener_certificates(
            ListenerArn=certificate_info['ListenerArn'],
            Certificates=certificate_info['Certificates'],
        )
        print(response)

    def elbv2_listener_certificates_describe(self,listener_arn):
        response = self.elbv2_client.describe_listener_certificates(
            ListenerArn=listener_arn,
            # Marker='string',
            # PageSize=123
        )
        return response


    def elbv2_rule_describe(self, rule_arn):
        response = self.elbv2_client.describe_rules(
            # ListenerArn=listener_arn,
            RuleArns=[
                rule_arn,
            ]
        )
        print(response)

    def elbv2_rules_describe(self, listener_arn):
        response = self.elbv2_client.describe_rules(
            ListenerArn=listener_arn,
        )
        return response['Rules']

    def elbv2_rule_delete(self, rule_arn):
        response = self.elbv2_client.delete_rule(
            RuleArn=rule_arn
        )
        print(response)

    def elbv2_rule_create(self, rule_info):
        # rule_info = {
        #     'ListenerArn': 'arn:aws-cn:elasticloadbalancing:cn-north-1:168677335524:listener/app/waf-app-internet-alb/e972ef0e9ff5c03c/f8dbc1fbccb0dab5',
        #     'Conditions': [
        #         {
        #             "Field": "host-header",
        #             "Values": [
        #                 "baidu.com"
        #             ]
        #         }
        #     ],
        #     'Priority': 2,
        #     'Actions': [
        #         {
        #             'Type': 'forward',
        #             'TargetGroupArn': 'arn:aws-cn:elasticloadbalancing:cn-north-1:168677335524:targetgroup/waf-app-internet-9009/25ce751a0b2b58c5',
        #             'Order': 1,
        #         }
        #     ],
        # }
        response = self.elbv2_client.create_rule(
            ListenerArn=rule_info['ListenerArn'],
            Conditions=rule_info['Conditions'],
            # Conditions=[
            #     {
            #         'Field': 'string',
            #         'Values': [
            #             'string',
            #         ],
            #         'HostHeaderConfig': {
            #             'Values': [
            #                 'string',
            #             ]
            #         },
            #         'PathPatternConfig': {
            #             'Values': [
            #                 'string',
            #             ]
            #         },
            #         'HttpHeaderConfig': {
            #             'HttpHeaderName': 'string',
            #             'Values': [
            #                 'string',
            #             ]
            #         },
            #         'QueryStringConfig': {
            #             'Values': [
            #                 {
            #                     'Key': 'string',
            #                     'Value': 'string'
            #                 },
            #             ]
            #         },
            #         'HttpRequestMethodConfig': {
            #             'Values': [
            #                 'string',
            #             ]
            #         },
            #         'SourceIpConfig': {
            #             'Values': [
            #                 'string',
            #             ]
            #         }
            #     },
            # ],
            Priority=rule_info['Priority'],
            Actions=rule_info['Actions'],
            # Actions=[
            #     {
            #         'Type': 'forward' | 'authenticate-oidc' | 'authenticate-cognito' | 'redirect' | 'fixed-response',
            #         'TargetGroupArn': 'string',
            # 'AuthenticateOidcConfig': {
            #     'Issuer': 'string',
            #     'AuthorizationEndpoint': 'string',
            #     'TokenEndpoint': 'string',
            #     'UserInfoEndpoint': 'string',
            #     'ClientId': 'string',
            #     'ClientSecret': 'string',
            #     'SessionCookieName': 'string',
            #     'Scope': 'string',
            #     'SessionTimeout': 123,
            #     'AuthenticationRequestExtraParams': {
            #         'string': 'string'
            #     },
            #     'OnUnauthenticatedRequest': 'deny' | 'allow' | 'authenticate',
            #     'UseExistingClientSecret': True | False
            # },
            # 'AuthenticateCognitoConfig': {
            #     'UserPoolArn': 'string',
            #     'UserPoolClientId': 'string',
            #     'UserPoolDomain': 'string',
            #     'SessionCookieName': 'string',
            #     'Scope': 'string',
            #     'SessionTimeout': 123,
            #     'AuthenticationRequestExtraParams': {
            #         'string': 'string'
            #     },
            #     'OnUnauthenticatedRequest': 'deny' | 'allow' | 'authenticate'
            # },
            # 'Order': 123,
            # 'RedirectConfig': {
            #     'Protocol': 'string',
            #     'Port': 'string',
            #     'Host': 'string',
            #     'Path': 'string',
            #     'Query': 'string',
            #     'StatusCode': 'HTTP_301' | 'HTTP_302'
            # },
            # 'FixedResponseConfig': {
            #     'MessageBody': 'string',
            #     'StatusCode': 'string',
            #     'ContentType': 'string'
            # }
            # },
            # ]
        )
        print(response)
        return response['Rules'][0]['RuleArn']

    def elbv2_target_group_create(self, target_group_info):
        # target_group_info={
        #     'Name':'bpm-prod-app-test',
        #     'Protocol':'TCP',
        #     'Port':22,
        #     'VpcId':'vpc-id',
        #     'TargetType':'instance',
        #     'HealthCheckProtocol':'HTTP' | 'HTTPS' | 'TCP' | 'TLS',
        #     'HealthCheckPort':'443'|'traffic-port',
        # }
        response = self.elbv2_client.create_target_group(
            Name=target_group_info['Name'],
            # Protocol='HTTP' | 'HTTPS' | 'TCP' | 'TLS',
            Protocol=target_group_info['Protocol'],
            Port=target_group_info['Port'],
            VpcId=target_group_info['VpcId'],
            HealthCheckProtocol=target_group_info['HealthCheckProtocol'],
            HealthCheckPort=target_group_info['HealthCheckPort'],
            # HealthCheckEnabled=True | False,
            # HealthCheckPath='string',
            # HealthCheckIntervalSeconds=123,
            # HealthCheckTimeoutSeconds=123,
            # HealthyThresholdCount=123,
            # UnhealthyThresholdCount=123,
            # Matcher={
            #     'HttpCode': 'string'
            # },
            # TargetType='instance' | 'ip' | 'lambda'
            TargetType=target_group_info['TargetType']
        )
        print(response)
        return response['TargetGroups'][0]['TargetGroupArn']

    def elbv2_target_group_delete(self, target_group_arn):
        response = self.elbv2_client.delete_target_group(
            TargetGroupArn=target_group_arn,
        )
        print(response)

    def elbv2_target_group_describe(self, target_group_arn):
        response = self.elbv2_client.describe_target_groups(
            TargetGroupArns=[
                target_group_arn,
            ],
            # Names=[
            #     group_name,
            # ],
        )
        return response['TargetGroups'][0]

    def elbv2_target_groups_describe(self):
        response = self.elbv2_client.describe_target_groups(
        )
        print(response)

    def elb_instances_register(self, info):
        # info = {
        #     'LoadBalancerName': 'name',
        #     'Instances': [
        #         {
        #             'InstanceId': 'string'
        #         },
        #     ],
        # }
        response = self.elb_client.register_instances_with_load_balancer(
            LoadBalancerName=info['LoadBalancerName'],
            Instances=info['Instances']
        )
        print(response)

    def elbv2_target_register(self, target_info):
        # target_info = {
        #     'TargetGroupArn': 'arn:aws-cn:id',
        #     'Targets': [
        #         {
        #             'Id': 'i-03a1c9ed8eb9b637e',
        #             'Port': 22,
        #         },
        #         {
        #             'Id': 'i-0a162b830a0a09307',
        #             'Port': 22,
        #         },
        #     ],
        # }
        response = self.elbv2_client.register_targets(
            TargetGroupArn=target_info['TargetGroupArn'],
            Targets=target_info['Targets']
        )
        print(response)

    def elb_instances_deregister(self, info):
        # info = {
        #     'LoadBalancerName': 'name',
        #     'Instances': [
        #         {
        #             'InstanceId': 'string'
        #         },
        #     ],
        # }
        response = self.elb_client.deregister_instances_from_load_balancer(
            LoadBalancerName=info['LoadBalancerName'],
            Instances=info['Instances']
        )
        print(response)

    def elbv2_target_deregister(self, target_info):
        # target_info = {
        #     'TargetGroupArn': 'arn:id',
        #     'Targets': [
        #         {
        #             'Id': 'i-03a1c9ed8eb9b637e',
        #             'Port': 22,
        #         },
        #         {
        #             'Id': 'i-0a162b830a0a09307',
        #             'Port': 22,
        #         },
        #     ],
        # }
        response = self.elbv2_client.deregister_targets(
            TargetGroupArn=target_info['TargetGroupArn'],
            Targets=target_info['Targets']
        )
        print(response)


if __name__ == '__main__':
    app = AWSELB()
    # app.elbv2_listeners_delete()
