#!/usr/bin/env bash

DB_PATH="../../../../data/duckdb/fedlearn.duckdb"

duckdb "$DB_PATH" < 01_v_features_target.sql
duckdb "$DB_PATH" < 02_v_features_patient.sql
duckdb "$DB_PATH" < 03_v_features_apache_aps.sql
duckdb "$DB_PATH" < 04_v_features_apache_pred.sql
duckdb "$DB_PATH" < 05_v_features_vitals_24h.sql
duckdb "$DB_PATH" < 06_v_features_labs_24h.sql
duckdb "$DB_PATH" < 07_v_features_resp_24h.sql
duckdb "$DB_PATH" < 08_v_features_infusions_24h.sql
duckdb "$DB_PATH" < 09_v_features_icu_stay.sql
