#!/usr/bin/env bash

PROJECT_DIR=~/git
export PYTHONPATH=$PROJECT_DIR/src

source ${PROJECT_DIR}/activate

streamlit run src/fedlearn/app/streamlit_app.py
