from __future__ import annotations

from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from pandas.api.types import (
    is_object_dtype,
    is_bool_dtype,
    is_numeric_dtype,
    is_datetime64_any_dtype,
)

# Constants

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DUCKDB_PATH = PROJECT_ROOT / "data" / "duckdb" / "fedlearn.duckdb"
VIEW_NAME = "v_features_icu_stay_clean"

TARGET_COL = "prolonged_stay"
DROP_COLS = ["patientunitstayid", "los_days", "prolonged_stay", "apacheadmissiondx"]

conn = duckdb.connect(DUCKDB_PATH, read_only=True)
df = conn.execute(f"SELECT * FROM {VIEW_NAME}").df()

# normalize pandas.NA -> np.nan so sklearn imputers are happy
df = df.where(df.notna(), np.nan)

print(f"Loaded dataframe shape: {df.shape}")
print()

y = df[TARGET_COL]
X = df.drop(columns=DROP_COLS)

print("Feature matrix shape:", X.shape)
print()

# Infer categorical vs numeric columns

categorical_cols: list[str] = []
numeric_cols: list[str] = []
other_cols: list[str] = []

for col in X.columns:
    s = X[col]
    dtype = s.dtype

    if is_object_dtype(dtype) or isinstance(dtype, pd.CategoricalDtype) or is_bool_dtype(dtype):
        categorical_cols.append(col)
    elif is_numeric_dtype(dtype):
        numeric_cols.append(col)
    elif is_datetime64_any_dtype(dtype):
        other_cols.append(col)  # datetime-like
    else:
        other_cols.append(col)  # anything weird/unexpected

# Print results

print("=" * 80)
print("CATEGORICAL FEATURE COLUMNS")
print("=" * 80)
print(f"Count: {len(categorical_cols)}")
for name in sorted(categorical_cols):
    print(f"  - {name} (dtype={X[name].dtype})")
print()

print("=" * 80)
print("NUMERIC FEATURE COLUMNS")
print("=" * 80)
print(f"Count: {len(numeric_cols)}")
for name in sorted(numeric_cols):
    print(f"  - {name} (dtype={X[name].dtype})")
print()

if other_cols:
    print("=" * 80)
    print("OTHER / UNKNOWN-TYPE FEATURE COLUMNS")
    print("=" * 80)
    print(f"Count: {len(other_cols)}")
    for name in sorted(other_cols):
        print(f"  - {name} (dtype={X[name].dtype})")
    print()

print("=" * 80)
print("ALL FEATURE DTYPES (for reference)")
print("=" * 80)

with pd.option_context("display.max_rows", None):
    print(X.dtypes.sort_index())
