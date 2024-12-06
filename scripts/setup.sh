#!/bin/bash

APP_DIR=next
IAC_DIR=cdk

# app dependencies
cd $APP_DIR
npm i --force # https://github.com/vercel/next.js/discussions/66259
cd -

# iac dependencies
cd $IAC_DIR
pip install pip-tools
pip install -r requirements.txt
cd -
