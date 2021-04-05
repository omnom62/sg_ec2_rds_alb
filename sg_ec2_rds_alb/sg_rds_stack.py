import aws_cdk.aws_rds as rds
import aws_cdk.aws_ec2 as ec2

from aws_cdk import core

class SG_RDS(core.Stack):
    def __init__(self, app: core.App, id: str, vpc, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        rds.DatabaseInstance(
            self, "RDS",
            database_name="db1",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_5
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
            port=3306,
            instance_type= ec2.InstanceType(instance_type_identifier="t2.micro"),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False
        )