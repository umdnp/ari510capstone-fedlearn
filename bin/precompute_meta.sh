#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$PWD"

source "${PROJECT_DIR}/activate"

python "${PROJECT_DIR}/src/compute_model_metadata.py"
