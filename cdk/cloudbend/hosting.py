from constructs import Construct
from aws_cdk import SecretValue
from aws_cdk.aws_route53 import IHostedZone
from aws_cdk.aws_apigatewayv2 import IHttpApi
from aws_cdk.aws_amplify_alpha import (
    App,
    SubDomain,
    GitHubSourceCodeProvider,
    Platform,
)


class WebHosting(Construct):
    def __init__(self, scope: Construct, construct_id: str, hosted_zone: IHostedZone, contact_api: IHttpApi):
        super().__init__(scope, construct_id)

        app = App(
            self,
            "AmplifyApp",
            app_name="web",
            platform=Platform.WEB,  # ssg
            source_code_provider=GitHubSourceCodeProvider(
                owner="cloudbend",
                repository="web",
                oauth_token=SecretValue.secrets_manager(
                    "amplify/github/token"
                ),
            ),
            environment_variables={
                # https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/1299
                "_CUSTOM_IMAGE": "public.ecr.aws/docker/library/node:22.11.0",
                "CONTACT_API_URL": contact_api.url,
            },
        )

        branch = app.add_branch(
            "main",
            performance_mode=True,
        )

        app.add_domain(
            hosted_zone.zone_name,
            sub_domains=[
                SubDomain(branch=branch, prefix="")
            ],
        )
