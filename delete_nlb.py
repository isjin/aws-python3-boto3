from function.aws_elb import AWSELB

nlb_arn = 'arn:aws-cn:elasticloadbalancing:cn-north-1:168677335524:loadbalancer/net/bpm-prod-test/2b69ffd174423ae4'
target_group_arn = 'arn:aws-cn:elasticloadbalancing:cn-north-1:168677335524:targetgroup/bpm-prod-app-k8s-master/d2f69602875ca8d0'


class NLB(object):
    def __init__(self):
        self.client = AWSELB()

    def delete_nlb(self):
        self.client.elbv2_load_balancer_delete(nlb_arn)

    def delete_target_group(self):
        self.client.elbv2_target_group_delete(target_group_arn)

    def main(self):
        self.delete_nlb()
        self.delete_target_group()


if __name__ == '__main__':
    app = NLB()
    app.main()
