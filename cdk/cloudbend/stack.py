from constructs import Construct
from aws_cdk import Stack, Environment
from constructs import Construct
from aws_cdk.aws_route53 import PublicHostedZone
from aws_cdk.aws_certificatemanager import Certificate, CertificateValidation
from aws_cdk.aws_ses import EmailIdentity
from aws_cdk.aws_events import EventBus

from cloudbend.contact import ContactService
from cloudbend.hosting import WebHosting


class WebStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env: Environment):
        super().__init__(scope, construct_id, env=env)

        hosted_zone = PublicHostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name="cloudbend.dev",
        )

        certificate = Certificate(
            self,
            "Certificate",
            domain_name=f"*.{hosted_zone.zone_name}",
            validation=CertificateValidation.from_dns(hosted_zone),
        )

        email = EmailIdentity.from_email_identity_name(
            self,
            "EmailIdentity",
            email_identity_name=hosted_zone.zone_name,
        )

        event_bus = EventBus(self, "EventBus")

        contact_svc = ContactService(
            self, "ContactSvc", hosted_zone, certificate, event_bus
        )

        WebHosting(self, "Hosting", hosted_zone, contact_svc.api)
