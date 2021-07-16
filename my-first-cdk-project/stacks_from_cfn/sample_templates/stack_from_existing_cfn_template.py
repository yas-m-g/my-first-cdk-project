from aws_cdk import core

import json


class StackFromCloudformationTemplate(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import Existing Cloudformation Template
        try:
            with open("stacks_from_cfn/sample_templates/create_s3_bucket_template.json", mode="r") as file:
                cfn_template = json.load(file)
        except OSError:
            print("Unable to read Cfn Template")

        resources_from_cfn_template = core.CfnInclude(self,
                                                        "KonstoneInfra",
                                                        template=cfn_template
                                                        )    

        encrypted_bkt_arn = core.Fn.get_att("EncryptedS3Bucket", "Arn")

        #Output Arn of encrypted BUucket 
        output_1 = core.CfnOutput(self,
                                    "EncryptedBucketArn",
                                     value=f"{encrypted_bkt_arn.to_string()}",
                                     description="Arn of Encrypted Bucket from Cfn Template"
                                   )                                    