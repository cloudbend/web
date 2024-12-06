import os
import logging

import boto3

from templates import CONTACT_TEMPLATE

logger = logging.getLogger()

ses = boto3.client("ses")

source_email_address = os.getenv("SOURCE_EMAIL_ADDRESS")
destination_email_address = os.getenv("DESTINATION_EMAIL_ADDRESS")


def contact_requested_handler(event, context):
    email = event["detail"]["email"]
    message = event["detail"]["message"]

    ses.send_email(
        Source=source_email_address,
        Destination={"ToAddresses": [destination_email_address]},
        ReplyToAddresses=[email],
        Message={
            "Subject": {"Data": "Cloudbend Contact"},
            "Body": {
                "Html": {
                    "Data": CONTACT_TEMPLATE.substitute(message=message)
                }
            },
        },
    )


def handler(event, context):
    source = event["source"]
    detail_type = event["detail-type"]

    if source == "cloudbend" and detail_type == "contact.requested":
        contact_requested_handler(event, context)
    else:
        logger.error(f"Unsupported event source: {
                     source} and detail type: {detail_type}")
