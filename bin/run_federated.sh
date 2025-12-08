#!/usr/bin/env bash

PROJECT_DIR=~/git
export PYTHONPATH=$PROJECT_DIR/src

source ${PROJECT_DIR}/activate

echo "Testing federated environment ..."
cd $PROJECT_DIR
flwr run
