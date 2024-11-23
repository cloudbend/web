from constructs import Construct
from aws_cdk import Stack, Environment
from constructs import Construct
from aws_cdk.aws_route53 import PublicHostedZone
from aws_cdk.aws_ses import EmailIdentity
from aws_cdk.aws_events import EventBus

from cloudbend.hosting import WebHosting


class WebStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env: Environment):
        super().__init__(scope, construct_id, env=env)

        domain_name = "cloudbend.dev"

        dns = PublicHostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name="cloudbend.dev",
        )

        email = EmailIdentity.from_email_identity_name(
            self,
            "EmailIdentity",
            email_identity_name=dns.zone_name,
        )

        event_bus = EventBus(self, "EventBus")

        WebHosting(self, "Hosting", hosted_zone=dns)
