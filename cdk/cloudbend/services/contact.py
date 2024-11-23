from pathlib import Path
from constructs import Construct
from aws_cdk import BundlingFileAccess
from aws_cdk.aws_route53 import IHostedZone, ARecord, RecordTarget
from aws_cdk.aws_route53_targets import ApiGatewayv2DomainProperties
from aws_cdk.aws_lambda import Architecture, Runtime, Tracing
from aws_cdk.aws_lambda_python_alpha import PythonFunction, BundlingOptions
from aws_cdk.aws_certificatemanager import Certificate, CertificateValidation
from aws_cdk.aws_logs import LogGroup
from aws_cdk.aws_apigatewayv2 import (
    HttpApi,
    DomainName,
    DomainMappingOptions,
)
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_events import IEventBus, EventPattern, Rule, Match
from aws_cdk.aws_events_targets import (
    LambdaFunction as LambdaFunctionTarget,
    CloudWatchLogGroup as CloudWatchLogGroupTarget,
)

FUNCTION_DIR = Path("cdk/cloudbend/functions")


class ContactRequest(PythonFunction):
    def __init__(self, scope: Construct, construct_id: str, event_bus: IEventBus):
        entry_path = FUNCTION_DIR / "contact-request"

        super().__init__(
            scope,
            construct_id,
            runtime=Runtime.PYTHON_3_12,
            architecture=Architecture.ARM_64,
            tracing=Tracing.ACTIVE,
            entry=str(entry_path),
            index="app.py",
            bundling=BundlingOptions(
                asset_excludes=["tests"],
                bundling_file_access=BundlingFileAccess.VOLUME_COPY,
            ),
            environment={
                "EVENT_BUS_NAME": event_bus.event_bus_name,
            },
        )

        event_bus.grant_put_events_to(self)


class ContactApi(HttpApi):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        event_bus: IEventBus,
        hosted_zone: IHostedZone,
    ):
        certificate = Certificate(
            scope,
            f"{construct_id}Certificate",
            domain_name=hosted_zone.zone_name,
            validation=CertificateValidation.from_dns(hosted_zone),
        )

        domain_name = DomainName(
            scope,
            f"{construct_id}DomainName",
            domain_name=domain_name,
            certificate=certificate,
        )

        handler_function = ContactRequest(
            scope, f"{construct_id}IntakeFn", event_bus
        )

        super().__init__(
            scope,
            construct_id,
            default_domain_mapping=DomainMappingOptions(
                domain_name=domain_name,
            ),
            default_integration=HttpLambdaIntegration(
                "HandlerIntegration",
                handler_function,
            ),
        )

        ARecord(
            self,
            "AliasRecord",
            zone=hosted_zone,
            record_name="contact",
            target=RecordTarget.from_alias(
                ApiGatewayv2DomainProperties(
                    domain_name.regional_domain_name,
                    domain_name.regional_hosted_zone_id,
                )
            ),
        )


class ContactService(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        hosted_zone: IHostedZone,
        event_bus: IEventBus,
    ):
        super().__init__(scope, construct_id)

        ContactApi(self, "Api", event_bus, hosted_zone)

        log_group = LogGroup(self, "LogGroup")

        Rule(
            self,
            "ContactLogRule",
            event_bus=event_bus,
            event_pattern=EventPattern(source=["cloudbend.contact"]),
            targets=[CloudWatchLogGroupTarget(log_group)],
        )
