#!/usr/bin/env python3
"""
Codabench evaluation script for ICU Prolonged Stay Prediction.
Computes F1 (macro), Accuracy, Precision, Recall.
"""

import pandas as pd
import json
from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report
)


def main():
    # Paths
    input_dir = Path('/app/input')  # Codabench mounts here
    output_dir = Path('/app/output')

    # Load reference (ground truth)
    ref = pd.read_csv(input_dir / 'ref' / 'test_labels.csv')

    # Load submission (participant predictions)
    res = pd.read_csv(input_dir / 'res' / 'predictions.csv')

    # Validate submission
    assert 'patientunitstayid' in res.columns, "Submission must have 'patientunitstayid' column"
    assert 'prediction' in res.columns, "Submission must have 'prediction' column"
    assert len(res) == len(ref), f"Submission has {len(res)} rows, expected {len(ref)}"
    assert set(res['prediction'].unique()).issubset({0, 1}), "Predictions must be binary (0 or 1)"

    # Merge on ID
    merged = ref.merge(res, on='patientunitstayid')
    assert len(merged) == len(ref), "Submission IDs do not match reference IDs"

    # Compute metrics
    y_true = merged['prolonged_stay']
    y_pred = merged['prediction']

    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average='macro',
        zero_division=0
    )

    # Prepare scores
    scores = {
        'f1_macro': float(f1),
        'accuracy': float(accuracy),
        'precision_macro': float(precision),
        'recall_macro': float(recall),
    }

    # Save to scores.json
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / 'scores.json', 'w') as f:
        json.dump(scores, f, indent=2)

    print(f"Evaluation complete: F1 (macro) = {f1:.4f}")
    print(f"Scores: {json.dumps(scores, indent=2)}")


if __name__ == '__main__':
    main()
