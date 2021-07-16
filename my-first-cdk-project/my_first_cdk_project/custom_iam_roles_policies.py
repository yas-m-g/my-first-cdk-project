from aws_cdk import core
from aws_cdk import aws_ssm as _ssm
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_secretsmanager as _secretsmanager

class CustomRolesPoliciesStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        user1_pass = _secretsmanager.Secret(self,
                                            "user1Pass",
                                            description="Password for user1",
                                            secret_name="user1_pass")

        #Add User1 with SecretsManager Password
        user1 = _iam.User(self, "user1",
                            password=user1_pass.secret_value,
                            user_name="user1")

        # Add IAM Group
        konstone_group = _iam.Group(self,
                                    "konStoneGroup",
                                    group_name="konstone_group" )

        #Add User to Group
        konstone_group.add_user(user1)

        #Add Managed Policy to group
        konstone_group.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )      

        #SSM parameter 1
        param1 = _ssm.StringParameter(
            self,
            "parameter1",
            description="Keys To KonStone",
            parameter_name="/konstone/keys/fish",
            string_value="130481",
            tier=_ssm.ParameterTier.STANDARD
        )

        #SSM parameter 2
        param2 = _ssm.StringParameter(
            self,
            "parameter2",
            description="Keys To KonStone",
            parameter_name="/konstone/keys/fish/gold",
            string_value="130482",
            tier=_ssm.ParameterTier.STANDARD
        )                      

        #Grant Konstone group permission to Param1
        param1.grant_read(konstone_group)

        #Login Url Autogeneration
        output_1 = core.CfnOutput(self,
                                    "user1LoginUrl",
                                    description="LoginUrl for User1",
                                    value=f"https://{core.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console")

                                                    