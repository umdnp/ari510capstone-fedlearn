#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$PWD"
SERVER_ADDRESS="0.0.0.0:8080"

source "${PROJECT_DIR}/activate"

echo "Starting Flower server on ${SERVER_ADDRESS} ..."
python "${PROJECT_DIR}/src/federated_server.py"
