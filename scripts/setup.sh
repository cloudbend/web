#!/bin/bash

APP_DIR=next
IAC_DIR=cdk

# app dependencies
cd $APP_DIR
npm i --force
cd -

# iac dependencies
cd $IAC_DIR
npm i -g aws-cdk
pip install pip-tools
pip install -r requirements.txt
cd -
