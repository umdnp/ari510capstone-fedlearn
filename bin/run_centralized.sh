#!/usr/bin/env bash

PROJECT_DIR=~/git
export PYTHONPATH=$PROJECT_DIR/src

source ${PROJECT_DIR}/activate

echo "Testing centralized models ..."
python -m fedlearn.centralized.centralized_models
