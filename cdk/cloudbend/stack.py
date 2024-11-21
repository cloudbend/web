from constructs import Construct
from aws_cdk import Stack, Environment
from constructs import Construct
from aws_cdk.aws_route53 import PublicHostedZone
from aws_cdk.aws_ses import EmailIdentity

from cloudbend.hosting import WebHosting


class WebStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env: Environment):
        super().__init__(scope, construct_id, env=env)

        domain = "cloudbend.dev"

        zone = PublicHostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name=domain,
        )

        email = EmailIdentity.from_email_identity_name(
            self,
            "EmailIdentity",
            email_identity_name=domain,
        )

        WebHosting(self, "Hosting")
