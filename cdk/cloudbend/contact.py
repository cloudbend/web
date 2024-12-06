from pathlib import Path
from constructs import Construct
from aws_cdk import Aws, BundlingFileAccess
from aws_cdk.aws_route53 import IHostedZone, ARecord, RecordTarget
from aws_cdk.aws_route53_targets import ApiGatewayv2DomainProperties
from aws_cdk.aws_certificatemanager import ICertificate
from aws_cdk.aws_logs import LogGroup, RetentionDays
from aws_cdk.aws_iam import Role, ServicePrincipal, PolicyStatement
from aws_cdk.aws_apigatewayv2 import (
    HttpApi,
    CorsPreflightOptions,
    CorsHttpMethod,
    IntegrationCredentials,
    HttpIntegration,
    HttpIntegrationType,
    HttpIntegrationSubtype,
    PayloadFormatVersion,
    ParameterMapping,
    DomainName,
    DomainMappingOptions,
    CfnRoute
)
from aws_cdk.aws_events import IEventBus, EventPattern, Rule, Match
from aws_cdk.aws_events_targets import (
    CloudWatchLogGroup as CloudWatchLogGroupTarget,
    LambdaFunction as LambdaFunctionTarget
)
from aws_cdk.aws_lambda import Runtime, Architecture, Tracing
from aws_cdk.aws_lambda_python_alpha import PythonFunction, BundlingOptions


FUNCTIONS_DIR = Path(__file__).parent / "functions"


class ContactEmailFunction(PythonFunction):
    def __init__(self, scope: Construct, construct_id: str):
        entry_path = FUNCTIONS_DIR / "contact_email"

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
            environment={"SOURCE_EMAIL_ADDRESS": "contact@cloudbend.dev",
                         "DESTINATION_EMAIL_ADDRESS": "help@cloudbend.dev"},
        )

        self.add_to_role_policy(
            PolicyStatement(
                actions=["ses:SendEmail"],
                resources=[
                    f"arn:aws:ses:{Aws.REGION}:{Aws.ACCOUNT_ID}:identity/cloudbend.dev"],
            )
        )


class ContactApi(HttpApi):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        hosted_zone: IHostedZone,
        certificate: ICertificate,
        event_bus: IEventBus,
    ):
        subdomain = "contact"
        fqdn = f"{subdomain}.{hosted_zone.zone_name}"

        domain_name = DomainName(
            scope,
            f"{construct_id}DomainName",
            domain_name=fqdn,
            certificate=certificate,
        )

        super().__init__(
            scope,
            construct_id,
            api_name="ContactApi",
            default_domain_mapping=DomainMappingOptions(
                domain_name=domain_name,
            ),
            cors_preflight=CorsPreflightOptions(
                allow_origins=["http://localhost:3000",
                               "https://cloudbend.dev"],
                allow_methods=[CorsHttpMethod.POST, CorsHttpMethod.OPTIONS],
                allow_headers=["Content-Type"],
            ),
        )

        integration_role = Role(
            self,
            "EventBridgeIntegrationRole",
            assumed_by=ServicePrincipal("apigateway.amazonaws.com"),
        )

        event_bus.grant_put_events_to(integration_role)

        integration = HttpIntegration(
            self,
            "EventBridgeIntegration",
            http_api=self,
            integration_type=HttpIntegrationType.AWS_PROXY,
            integration_subtype=HttpIntegrationSubtype.EVENTBRIDGE_PUT_EVENTS,
            payload_format_version=PayloadFormatVersion.VERSION_1_0,
            credentials=IntegrationCredentials.from_role(integration_role),
            parameter_mapping=(
                ParameterMapping()
                .custom("EventBusName", event_bus.event_bus_arn)
                .custom("Source", "cloudbend")
                .custom("DetailType", "contact.requested")
                .custom("Detail", "$request.body")
            ),
        )

        CfnRoute(
            self,
            "Route",
            api_id=self.http_api_id,
            route_key="POST /",
            target=f"integrations/{integration.integration_id}",
        )

        ARecord(
            self,
            "AliasRecord",
            zone=hosted_zone,
            record_name=subdomain,
            target=RecordTarget.from_alias(
                ApiGatewayv2DomainProperties(
                    domain_name.regional_domain_name,
                    domain_name.regional_hosted_zone_id,
                )
            ),
        )


class ContactService(Construct):
    api: HttpApi

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        hosted_zone: IHostedZone,
        certificate: ICertificate,
        event_bus: IEventBus,
    ):
        super().__init__(scope, construct_id)

        self.api = ContactApi(self, "Api", hosted_zone, certificate, event_bus)

        log_group = LogGroup(
            self, "LogGroup", retention=RetentionDays.ONE_MONTH
        )

        email_function = ContactEmailFunction(self, "EmailFn")

        Rule(
            self,
            "ContactLogRule",
            event_bus=event_bus,
            event_pattern=EventPattern(
                source=["cloudbend"],
                detail_type=Match.prefix("contact.")
            ),
            targets=[CloudWatchLogGroupTarget(log_group)],
        )

        Rule(
            self,
            "ContactEmailRule",
            event_bus=event_bus,
            event_pattern=EventPattern(
                source=["cloudbend"], detail_type=["contact.requested"]
            ),
            targets=[LambdaFunctionTarget(email_function)],
        )
