from constructs import Construct
from aws_cdk import SecretValue
from aws_cdk.aws_iam import (
    Role,
    ServicePrincipal,
    ManagedPolicy,
    PolicyStatement,
    Effect,
)
from aws_cdk.aws_amplify_alpha import (
    App,
    SubDomain,
    GitHubSourceCodeProvider,
    CustomRule,
    RedirectStatus,
    Platform,
)


class WebHosting(Construct):
    def __init__(self, scope: Construct, construct_id: str, domain_name: str):
        super().__init__(scope, construct_id)

        service_role = Role(
            self,
            "AmplifyServiceRole",
            assumed_by=ServicePrincipal("amplify.amazonaws.com"),
            description="Service role permitting Amplify to create required resources for Next SSR app.",
        )

        service_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        app = App(
            self,
            "AmplifyApp",
            app_name="web",
            role=service_role,
            platform=Platform.WEB_COMPUTE,
            source_code_provider=GitHubSourceCodeProvider(
                owner="cloudbend",
                repository="web",
                oauth_token=SecretValue.secrets_manager(
                    "amplify/github/token"
                ),
            ),
            environment_variables={
                # https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/1299
                "_CUSTOM_IMAGE": "public.ecr.aws/docker/library/node:22.11.0"
            },
        )

        branch = app.add_branch(
            "main",
            performance_mode=True,
        )

        app.add_domain(
            domain_name,
            sub_domains=[
                SubDomain(branch=branch, prefix=""),
                SubDomain(branch=branch, prefix="www"),
            ],
        )

        # redirect www to root
        app.add_custom_rule(
            CustomRule(
                source=f"www.{domain_name}",
                target=f"https://{domain_name}",
                status=RedirectStatus.PERMANENT_REDIRECT,
            )
        )
