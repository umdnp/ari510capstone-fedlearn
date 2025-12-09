"""
Create train/test splits for Codabench competition.

This script:
1. Loads processed demo data
2. Creates stratified 60/40 train/test split
3. Generates competition files:
   - train.csv (features + labels)
   - test.csv (features only)
   - test_labels.csv (hidden ground truth)
   - sample_submission.csv (submission format)

Usage:
    python -m fedlearn.tools.create_codabench_splits
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

# Constants
PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_FILE = PROJECT_ROOT / "data" / "codabench" / "processed_demo.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "codabench"


def main():
    """Main pipeline to create competition splits."""
    print("=" * 80)
    print("Creating Codabench Competition Splits")
    print("=" * 80)
    print()

    # 1. Load processed data
    print("1. Loading processed data...")
    df = pd.read_csv(INPUT_FILE)
    print(f"   Total samples: {len(df)}")
    print(f"   Total features: {df.shape[1]}")
    print()

    # 2. Identify columns
    print("2. Identifying columns...")
    id_col = 'patientunitstayid'
    target_col = 'prolonged_stay'
    exclude_cols = [id_col, target_col, 'los_days', 'apacheadmissiondx']  # Exclude los_days (leakage) and diagnosis (text)

    feature_cols = [col for col in df.columns if col not in exclude_cols]
    print(f"   ID column: {id_col}")
    print(f"   Target column: {target_col}")
    print(f"   Feature columns: {len(feature_cols)}")
    print()

    # 3. Create stratified split
    print("3. Creating 60/40 train/test split (stratified)...")
    train_df, test_df = train_test_split(
        df,
        test_size=0.4,
        random_state=42,
        stratify=df[target_col]
    )

    print(f"   Train samples: {len(train_df)} ({len(train_df) / len(df) * 100:.1f}%)")
    print(f"   Test samples:  {len(test_df)} ({len(test_df) / len(df) * 100:.1f}%)")
    print()

    print("   Train class distribution:")
    print(f"     - Not prolonged: {(train_df[target_col] == 0).sum()} ({(train_df[target_col] == 0).sum() / len(train_df) * 100:.1f}%)")
    print(f"     - Prolonged:     {(train_df[target_col] == 1).sum()} ({(train_df[target_col] == 1).sum() / len(train_df) * 100:.1f}%)")
    print()

    print("   Test class distribution:")
    print(f"     - Not prolonged: {(test_df[target_col] == 0).sum()} ({(test_df[target_col] == 0).sum() / len(test_df) * 100:.1f}%)")
    print(f"     - Prolonged:     {(test_df[target_col] == 1).sum()} ({(test_df[target_col] == 1).sum() / len(test_df) * 100:.1f}%)")
    print()

    # 4. Create train.csv (features + labels)
    print("4. Creating train.csv (features + labels)...")
    train_output = train_df[[id_col] + feature_cols + [target_col]]
    train_file = OUTPUT_DIR / "train.csv"
    train_output.to_csv(train_file, index=False)
    print(f"   Saved to: {train_file}")
    print(f"   Shape: {train_output.shape}")
    print()

    # 5. Create test.csv (features only, NO labels)
    print("5. Creating test.csv (features only, NO labels)...")
    test_output = test_df[[id_col] + feature_cols]
    test_file = OUTPUT_DIR / "test.csv"
    test_output.to_csv(test_file, index=False)
    print(f"   Saved to: {test_file}")
    print(f"   Shape: {test_output.shape}")
    print()

    # 6. Create test_labels.csv (hidden ground truth for evaluation)
    print("6. Creating test_labels.csv (hidden ground truth)...")
    test_labels = test_df[[id_col, target_col]]
    test_labels_file = OUTPUT_DIR / "test_labels.csv"
    test_labels.to_csv(test_labels_file, index=False)
    print(f"   Saved to: {test_labels_file}")
    print(f"   Shape: {test_labels.shape}")
    print()

    # 7. Create sample_submission.csv (format example)
    print("7. Creating sample_submission.csv (submission format)...")
    sample_submission = test_df[[id_col]].copy()
    sample_submission['prediction'] = 0  # All zeros as placeholder
    sample_file = OUTPUT_DIR / "sample_submission.csv"
    sample_submission.to_csv(sample_file, index=False)
    print(f"   Saved to: {sample_file}")
    print(f"   Shape: {sample_submission.shape}")
    print()

    # 8. Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print("Competition files created:")
    print(f"  1. train.csv              - {len(train_df):,} samples with labels")
    print(f"  2. test.csv               - {len(test_df):,} samples (no labels)")
    print(f"  3. test_labels.csv        - {len(test_df):,} ground truth labels (hidden)")
    print(f"  4. sample_submission.csv  - {len(test_df):,} sample predictions")
    print()
    print("Participants will:")
    print("  - Train on train.csv (features + labels)")
    print("  - Predict on test.csv (features only)")
    print("  - Submit predictions in format of sample_submission.csv")
    print()
    print("Evaluation will:")
    print("  - Compare predictions to test_labels.csv")
    print("  - Compute F1 (macro), Accuracy, Precision, Recall")
    print()
    print("Competition data ready for Codabench!")
    print("=" * 80)


if __name__ == "__main__":
    main()
