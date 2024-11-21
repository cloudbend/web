from aws_cdk import App, Environment

from cloudbend.stack import WebStack

env = Environment(account="898546127587", region="us-west-2")

app = App()

WebStack(app, "Web", env=env)

app.synth()
