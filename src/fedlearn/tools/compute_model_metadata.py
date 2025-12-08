"""
Compute model metadata and save the fitted preprocessor.

This script:
  - Loads data from DuckDB
  - Applies the same preprocessing as the centralized model
  - Computes:
      - n_features (after preprocessing)
      - classes (unique values of prolonged_stay)
      - intercept (zero vector of length n_classes)
  - Saves:
      - configs/model_meta.json
      - configs/preprocessor.pkl

Run:
    python compute_model_metadata.py
"""

import json
from pathlib import Path

import duckdb
import joblib
import numpy as np

from fedlearn.common.preprocessing import build_preprocessor, build_preprocessor_dynamically

# Constants

SOURCE_TABLE = "v_features_icu_stay_clean"
DROP_COLS = ["patientunitstayid", "los_days", "prolonged_stay", "apacheadmissiondx"]

# number of rows to sample for computing feature dimension
SAMPLE_ROWS = 50000

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DUCKDB_PATH = PROJECT_ROOT / "data" / "duckdb" / "fedlearn.duckdb"

CONFIG_DIR = PROJECT_ROOT / "configs"
META_PATH = CONFIG_DIR / "model_meta.json"
PREPROC_PATH = CONFIG_DIR / "preprocessor.pkl"


def main():
    # Ensure config directory exists
    if not CONFIG_DIR.exists():
        print(f"Config directory '{CONFIG_DIR}' does not exist, creating it ...")
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    print("Connecting to DuckDB ...")
    conn = duckdb.connect(DUCKDB_PATH, read_only=True)

    print(f"Loading up to {SAMPLE_ROWS} rows from {SOURCE_TABLE}")
    df = conn.execute(f"SELECT * FROM {SOURCE_TABLE} LIMIT {SAMPLE_ROWS}").df()
    conn.close()

    # normalize missing values
    df = df.where(df.notna(), np.nan)

    # extract target and features
    if "prolonged_stay" not in df.columns:
        raise RuntimeError("Column 'prolonged_stay' not found in dataframe")

    y = df["prolonged_stay"].to_numpy()
    X = df.drop(columns=DROP_COLS)

    # build and fit preprocessor
    print("Fitting preprocessing pipeline ...")
    #preprocessor = build_preprocessor_dynamically(X)
    preprocessor = build_preprocessor()
    preprocessor.fit(X)

    # transform data to compute feature dimension
    print("Transforming data ...")
    X_proc = preprocessor.transform(X)
    n_features = X_proc.shape[1]

    # compute classes from y
    classes = np.unique(y)
    classes_list = [int(c) for c in classes]  # JSON-friendly

    # create initial intercept as zeros, one per class
    intercept = [0.0] * len(classes_list)

    print("\n--------------------------------------------")
    print(f"Computed feature dimension: {n_features}")
    print(f"Classes: {classes_list}")
    print(f"Initial intercept (zeros): {intercept}")
    print("--------------------------------------------\n")

    meta = {
        "n_features": int(n_features),
        "classes": classes_list,
        "intercept": intercept,
    }

    print(f"Saving model metadata to {META_PATH}")
    with META_PATH.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Saving fitted preprocessor to {PREPROC_PATH}")
    joblib.dump(preprocessor, PREPROC_PATH)

    print("Done!")


if __name__ == "__main__":
    main()
