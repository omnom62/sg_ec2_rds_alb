from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class SG_VPC(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ASI VPC definition

        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=2,
                           cidr="10.10.0.0/16",
                           vpn_gateway=False,
                           nat_gateways=0,
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="sg-pubnet",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.ISOLATED,
                               name="sg-privnet",
                               cidr_mask=24
                           )
                           ]
                           )
        core.CfnOutput(self, "Output", value=self.vpc.vpc_id)