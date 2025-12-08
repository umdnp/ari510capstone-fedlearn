#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$PWD"
PYTHONPATH="src"

source "${PROJECT_DIR}/activate"

echo "Starting Flower server ..."
flwr run serverapp
