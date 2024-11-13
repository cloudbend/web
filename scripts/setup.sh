#!/bin/bash

APP_DIR=app
IAC_DIR=cdk

# app dependencies
cd $APP_DIR
npm i
cd -

# iac dependencies
cd $IAC_DIR
cd -
