import os
from aws_cdk import App, Environment

from cloudbend.stack import WebStack

env = Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]
)

app = App()

WebStack(app, "Web", env=env)

app.synth()
