## DuckDB Build Scripts

After downloading the data files for the [eICU Collaborative Research Database](https://physionet.org/content/eicu-crd/2.0), follow the steps below to create a DuckDB database and import the data.

### 1. Create a new DuckDB database
```bash
duckdb fedlearn.duckdb < duckdb_create_tables.sql
```

### 2. Import the data files
You don’t need to uncompress the files before loading them:
```bash
duckdb fedlearn.duckdb -cmd ".cd '/data/physionet.org/eicu-crd/2.0'" < duckdb_load_data_gz.sql
```

### 3. Verify the import
Run the following command to check that all data was imported successfully:
```bash
duckdb fedlearn.duckdb < duckdb_checks.sql
```
