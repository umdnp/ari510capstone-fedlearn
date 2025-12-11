#!/usr/bin/env bash

PROJECT_DIR=~/git
export PYTHONPATH=$PROJECT_DIR/src
export RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0

source ${PROJECT_DIR}/activate

echo "Testing federated environment ..."
cd $PROJECT_DIR
flwr run
