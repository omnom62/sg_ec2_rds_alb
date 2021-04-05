from aws_cdk.aws_ec2 import SubnetType
from aws_cdk import ( 
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    aws_certificatemanager as acm
#    aws_iam as iam
)

ec2_type = "t2.micro"

certificateArn = "arn:aws:acm:ap-southeast-2:107161814468:certificate/062bebaf-f90b-41c7-8d3a-63a335227e89"


linux = ec2.MachineImage.lookup(name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20200924")

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class SG_EC2(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
    
        certificate = acm.Certificate.from_certificate_arn(self, 'Certificate', certificateArn)

        #certificate = iam.CfnServerCertificate.certificate_body

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        # Create ALB
        alb = elbv2.ApplicationLoadBalancer(self, "SG-alb",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="SG-alb"
                                          )

        alb.set_attribute(key="routing.http.drop_invalid_header_fields.enabled", value="true")

        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(443), "Internet access ALB 443")


        httpsListener = alb.add_listener("SG-alb-httpsList",
                                    port=443,
                                    certificates=[certificate])    

        alb.add_redirect(
            source_port=80,
            target_port=443
        ) 

       # Create Autoscaling Group with fixed 1*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "SG-asg",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux,
                                                role=role,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=1,
                                                min_capacity=1,
                                                max_capacity=1,
        )

        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        httpsListener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        core.CfnOutput(self, "Instance Id:", value=alb.load_balancer_dns_name)
app = core.App()