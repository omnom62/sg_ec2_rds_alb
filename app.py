#!/usr/bin/env python3

from aws_cdk import core

from sg_ec2_rds_alb.sg_ec2_stack import SG_EC2
from sg_ec2_rds_alb.sg_vpc_stack import SG_VPC
from sg_ec2_rds_alb.sg_rds_stack import SG_RDS



app = core.App()

#env = core.Environment(account="107161814468", region="ap-southeast-2")

vpc_stack = SG_VPC(app, "cdk-vpc", env=env)
ec2_stack = SG_EC2(app, "cdk-ec2", env=env, vpc=vpc_stack.vpc)
rds_stack = SG_RDS(app, "cdk-rds", env=env, vpc=vpc_stack.vpc)

app.synth()
