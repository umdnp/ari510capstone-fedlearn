# DuckDB Build Scripts

Run using:

duckdb fedlearn.duckdb < duckdb_create_tables.sql
duckdb fedlearn.duckdb -cmd ".cd '/data/physionet.org/eicu-crd/2.0'" < duckdb_load_data_gz.sql
duckdb fedlearn.duckdb < duckdb_checks.sql

