from aws_cdk import core
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_secretsmanager as _secretsmanager

import json


class CustomIamUsersGroupsStack(core.Stack):

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

       
        #Add User2 with Literal Password    
        user2 = _iam.User(self, "user2",
                            password=core.SecretValue.plain_text(
                                "Dont-Use-B@d-Passw0rds"
                            ),
                            user_name="user2")


        #Login Url Autogeneration
        output_1 = core.CfnOutput(self,
                                    "user2LoginUrl",
                                    description="LoginUrl for User2",
                                    value=f"https://{core.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console")

                        