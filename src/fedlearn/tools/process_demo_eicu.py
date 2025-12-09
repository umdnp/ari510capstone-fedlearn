"""
Process eICU demo dataset for Codabench competition.

This script:
1. Loads CSV files from the eICU demo dataset
2. Applies same feature engineering as full eICU
3. Creates 'prolonged_stay' target (LOS > 3 days)
4. Saves processed data for Codabench splits

Usage:
    python -m fedlearn.tools.process_demo_eicu
"""

from __future__ import annotations

import gzip
from pathlib import Path

import pandas as pd
import numpy as np

# Constants
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEMO_DIR = PROJECT_ROOT / "data" / "eicu_demo" / "eicu-collaborative-research-database-demo-2.0.1"
OUTPUT_DIR = PROJECT_ROOT / "data" / "codabench"


def load_csv_gz(filename: str) -> pd.DataFrame:
    """Load a gzipped CSV file from the demo dataset."""
    filepath = DEMO_DIR / filename
    with gzip.open(filepath, 'rt') as f:
        return pd.read_csv(f)


def calculate_prolonged_stay(patient_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate prolonged_stay target (LOS > 3 days).

    LOS = unitdischargeoffset / 1440 (minutes to days)
    prolonged_stay = 1 if LOS > 3, else 0
    """
    # unitdischargeoffset is in minutes
    patient_df['los_days'] = patient_df['unitdischargeoffset'] / 1440.0
    patient_df['prolonged_stay'] = (patient_df['los_days'] > 3).astype(int)

    return patient_df


def get_vital_stats(vital_df: pd.DataFrame, patient_ids: list) -> pd.DataFrame:
    """
    Extract vital sign statistics from vitalPeriodic table.

    Computes mean, std, min, max for each vital sign per patient.
    """
    # Filter to relevant patients
    vital_df = vital_df[vital_df['patientunitstayid'].isin(patient_ids)]

    # Vital signs to extract
    vital_columns = [
        'temperature', 'sao2', 'heartrate', 'respiration',
        'systemicsystolic', 'systemicdiastolic', 'systemicmean'
    ]

    agg_dict = {}
    for col in vital_columns:
        if col in vital_df.columns:
            agg_dict[col] = ['mean', 'std', 'min', 'max']

    if not agg_dict:
        return pd.DataFrame({'patientunitstayid': patient_ids})

    vital_stats = vital_df.groupby('patientunitstayid').agg(agg_dict)
    vital_stats.columns = ['_'.join(col).strip() for col in vital_stats.columns.values]
    vital_stats = vital_stats.reset_index()

    return vital_stats


def get_lab_stats(lab_df: pd.DataFrame, patient_ids: list) -> pd.DataFrame:
    """
    Extract lab value statistics.

    Pivot lab values and compute statistics per patient.
    """
    lab_df = lab_df[lab_df['patientunitstayid'].isin(patient_ids)]

    # Common lab tests
    important_labs = [
        'WBC x 1000', 'creatinine', 'BUN', 'glucose',
        'sodium', 'potassium', 'bicarbonate', 'platelets x 1000',
        'Hct', 'Hgb', 'total bilirubin'
    ]

    lab_df = lab_df[lab_df['labname'].isin(important_labs)]

    if lab_df.empty:
        return pd.DataFrame({'patientunitstayid': patient_ids})

    # Pivot and aggregate
    lab_pivot = lab_df.pivot_table(
        index='patientunitstayid',
        columns='labname',
        values='labresult',
        aggfunc=['mean', 'std', 'min', 'max']
    )

    lab_pivot.columns = ['_'.join(col).strip().replace(' ', '_') for col in lab_pivot.columns.values]
    lab_pivot = lab_pivot.reset_index()

    return lab_pivot


def get_apache_scores(apache_df: pd.DataFrame, patient_ids: list) -> pd.DataFrame:
    """Extract APACHE scores and predictions."""
    apache_df = apache_df[apache_df['patientunitstayid'].isin(patient_ids)]

    apache_features = [
        'patientunitstayid',
        'acutephysiologyscore',
        'apachescore',
        'predictedicumortality',
        'predictedhospitalmortality'
    ]

    # Select available columns
    available_cols = [col for col in apache_features if col in apache_df.columns]
    apache_subset = apache_df[available_cols]

    # Handle duplicates: keep first record per patient
    apache_subset = apache_subset.drop_duplicates(subset=['patientunitstayid'], keep='first')

    return apache_subset


def main():
    """Main processing pipeline."""
    print("=" * 80)
    print("Processing eICU Demo Dataset for Codabench")
    print("=" * 80)
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load patient table
    print("1. Loading patient data...")
    patient_df = load_csv_gz("patient.csv.gz")
    print(f"   Loaded {len(patient_df)} ICU stays")

    # 2. Calculate prolonged stay
    print("2. Calculating prolonged_stay target...")
    patient_df = calculate_prolonged_stay(patient_df)

    # Remove patients with missing LOS
    patient_df = patient_df[patient_df['los_days'].notna()]
    print(f"   {len(patient_df)} stays with valid LOS")
    print(f"   Prolonged stay distribution:")
    print(f"     - Not prolonged (<=3 days): {(patient_df['prolonged_stay'] == 0).sum()}")
    print(f"     - Prolonged (>3 days):      {(patient_df['prolonged_stay'] == 1).sum()}")
    print()

    patient_ids = patient_df['patientunitstayid'].tolist()

    # 3. Load vital signs
    print("3. Loading vital signs...")
    vital_df = load_csv_gz("vitalPeriodic.csv.gz")
    vital_stats = get_vital_stats(vital_df, patient_ids)
    print(f"   Extracted vital signs for {len(vital_stats)} patients")

    # 4. Load labs
    print("4. Loading lab values...")
    lab_df = load_csv_gz("lab.csv.gz")
    lab_stats = get_lab_stats(lab_df, patient_ids)
    print(f"   Extracted lab values for {len(lab_stats)} patients")

    # 5. Load APACHE scores
    print("5. Loading APACHE scores...")
    apache_df = load_csv_gz("apachePatientResult.csv.gz")
    apache_features = get_apache_scores(apache_df, patient_ids)
    print(f"   Extracted APACHE features for {len(apache_features)} patients")

    # 6. Merge all features
    print("6. Merging features...")

    # Start with patient demographics
    features_df = patient_df[[
        'patientunitstayid', 'age', 'gender', 'ethnicity',
        'admissionweight', 'los_days', 'prolonged_stay', 'apacheadmissiondx'
    ]].copy()

    # Merge vital signs
    features_df = features_df.merge(vital_stats, on='patientunitstayid', how='left')

    # Merge labs
    features_df = features_df.merge(lab_stats, on='patientunitstayid', how='left')

    # Merge APACHE
    features_df = features_df.merge(apache_features, on='patientunitstayid', how='left')

    print(f"   Final dataset shape: {features_df.shape}")
    print(f"   Total features: {features_df.shape[1] - 3}")  # -3 for ID, los_days, prolonged_stay
    print()

    # 7. Basic preprocessing
    print("7. Basic preprocessing...")

    # Convert age to numeric (handle "> 89" as 90)
    features_df['age'] = features_df['age'].replace('> 89', '90')
    features_df['age'] = pd.to_numeric(features_df['age'], errors='coerce')

    # Handle categorical variables
    # For now, keep as-is for train/test split
    # Preprocessing will be done by participants

    print(f"   Missing values per column:")
    missing_pct = (features_df.isnull().sum() / len(features_df) * 100).sort_values(ascending=False)
    print(missing_pct.head(10))
    print()

    # 8. Save processed data
    output_file = OUTPUT_DIR / "processed_demo.csv"
    features_df.to_csv(output_file, index=False)
    print(f"8. Saved processed data to: {output_file}")
    print(f"   Rows: {len(features_df)}")
    print(f"   Columns: {features_df.shape[1]}")
    print()

    # 9. Summary statistics
    print("=" * 80)
    print("Summary Statistics")
    print("=" * 80)
    print(f"Total ICU stays:          {len(features_df)}")
    print(f"Prolonged stays (>3d):    {(features_df['prolonged_stay'] == 1).sum()} ({(features_df['prolonged_stay'] == 1).sum() / len(features_df) * 100:.1f}%)")
    print(f"Not prolonged (<=3d):     {(features_df['prolonged_stay'] == 0).sum()} ({(features_df['prolonged_stay'] == 0).sum() / len(features_df) * 100:.1f}%)")
    print()
    print(f"Mean LOS: {features_df['los_days'].mean():.2f} days")
    print(f"Median LOS: {features_df['los_days'].median():.2f} days")
    print(f"Max LOS: {features_df['los_days'].max():.2f} days")
    print()
    print("Processing complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
