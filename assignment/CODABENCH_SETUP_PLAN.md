# Codabench Competition Setup Plan

## Goal
Create a public Codabench competition for ICU prolonged stay prediction using the eICU demo dataset.

## Dataset Source
- **eICU-CRD Demo**: https://physionet.org/content/eicu-crd-demo/2.0.1/
- **Size**: 130.4 MB (zipped)
- **License**: Open Data Commons Open Database License v1.0
- **No credentials required** - Publicly available for teaching/demo

---

## Step 1: Process Demo Dataset

### 1.1 Extract and Explore
```bash
cd data/eicu_demo
unzip eicu-collaborative-research-database-demo-2.0.1.zip
ls -la  # See what tables are available
```

### 1.2 Understand Demo Dataset Scope
- Check how many ICU stays in demo vs. full dataset
- Verify we have necessary tables (patient, apachePatientResult, etc.)
- Document any limitations

### 1.3 Create Processing Script
**File**: `src/fedlearn/tools/process_demo_eicu.py`

**Tasks**:
1. Load CSV files from demo dataset
2. Apply same feature engineering as full eICU
3. Create `prolonged_stay` target (LOS > 3 days)
4. Apply preprocessing (imputation, scaling, OHE)
5. Save processed data

**Output**:
- `data/codabench/full_processed.csv` - All processed demo data

---

## Step 2: Create Competition Splits

### 2.1 Split Strategy
```python
# 60% train (participants get features + labels)
# 40% test (participants get features only)

train_data, test_data = train_test_split(
    full_processed,
    test_size=0.4,
    random_state=42,
    stratify=y
)
```

### 2.2 Create Files
**File**: `src/fedlearn/tools/create_codabench_splits.py`

**Outputs**:
```
data/codabench/
├── train.csv           # Features + prolonged_stay label
├── test.csv            # Features only (no label)
├── test_labels.csv     # Ground truth (hidden from participants)
└── sample_submission.csv  # Format: patientunitstayid, prediction
```

**Format Details**:
- `train.csv`: All features + `prolonged_stay` column
- `test.csv`: Same features, NO `prolonged_stay` column
- `test_labels.csv`: `patientunitstayid`, `prolonged_stay`
- `sample_submission.csv`: `patientunitstayid`, `prediction` (all 0s or all 1s)

---

## Step 3: Create Evaluation Script

### 3.1 Scoring Program
**Directory**: `codabench_bundle/scoring_program/`

**File**: `codabench_bundle/scoring_program/score.py`

```python
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
    assert 'patientunitstayid' in res.columns
    assert 'prediction' in res.columns
    assert len(res) == len(ref)
    assert set(res['prediction'].unique()).issubset({0, 1})

    # Merge on ID
    merged = ref.merge(res, on='patientunitstayid')

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

if __name__ == '__main__':
    main()
```

**File**: `codabench_bundle/scoring_program/requirements.txt`
```
pandas>=2.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
```

**File**: `codabench_bundle/scoring_program/metadata`
```
command: python3 $program/score.py
```

---

## Step 4: Create Starter Kit

### 4.1 Baseline Notebook
**File**: `codabench_bundle/starting_kit/baseline_notebook.ipynb`

**Contents**:
1. Load train.csv and test.csv
2. Basic EDA (class distribution, missing values)
3. Train simple Logistic Regression baseline
4. Make predictions on test set
5. Save predictions in correct format
6. Expected performance: F1 ~0.66

### 4.2 Sample Submission
Already created in Step 2.2

---

## Step 5: Package Competition Bundle

### 5.1 Directory Structure
```
codabench_bundle/
├── public_data/
│   ├── train.csv                     # Training data with labels
│   └── test.csv                      # Test features (no labels)
├── reference_data/
│   └── test_labels.csv               # Ground truth (hidden)
├── scoring_program/
│   ├── score.py                      # Evaluation script
│   ├── requirements.txt              # Dependencies
│   └── metadata                      # Execution config
├── starting_kit/
│   ├── baseline_notebook.ipynb       # Example notebook
│   ├── sample_submission.csv         # Format example
│   └── README.md                     # Instructions
├── logo.png                          # Competition logo (optional)
└── competition.yaml                  # Codabench configuration
```

### 5.2 Competition Configuration
**File**: `codabench_bundle/competition.yaml`

```yaml
title: "ICU Prolonged Stay Prediction Challenge"
description: |
  Predict whether ICU patients will have a prolonged stay (>3 days) based on
  admission data from the eICU Collaborative Research Database demo dataset.

# Task information
tasks:
  - name: "Predict prolonged ICU stay"
    description: "Binary classification task"
    input_data: "train.csv with features + labels, test.csv with features only"
    scoring: "F1 Score (macro-averaged), Accuracy, Precision, Recall"

# Phases
phases:
  - name: "Development Phase"
    description: "Public leaderboard with test set feedback"
    start_date: "2025-12-09"
    max_submissions_per_day: 5

# Scoring
leaderboard:
  - title: "Main Leaderboard"
    key: "f1_macro"
    sorting: "desc"
    columns:
      - title: "F1 (Macro)"
        key: "f1_macro"
        sorting: "desc"
      - title: "Accuracy"
        key: "accuracy"
      - title: "Precision (Macro)"
        key: "precision_macro"
      - title: "Recall (Macro)"
        key: "recall_macro"

# Terms
terms: |
  ## Dataset License
  This competition uses the eICU Collaborative Research Database (demo version),
  licensed under the Open Data Commons Open Database License v1.0.

  ## Submission Rules
  - Maximum 5 submissions per day during development phase
  - Predictions must be binary (0 or 1)
  - Submission format: CSV with columns: patientunitstayid, prediction
```

---

## Step 6: Upload to Codabench

### 6.1 Create Codabench Account
- Go to https://www.codabench.org/
- Sign up / Log in
- Navigate to "Competitions" → "Create Competition"

### 6.2 Upload Bundle
1. Zip the `codabench_bundle/` directory
2. Upload via Codabench web interface
3. Configure competition settings:
   - Title, description, dates
   - Leaderboard metrics
   - Submission limits

### 6.3 Test Submission
1. Create baseline predictions using starter kit
2. Submit to competition
3. Verify scoring works correctly
4. Check leaderboard updates

---

## Step 7: Documentation

### 7.1 Competition Page Content
**Add to Codabench page**:
- Task definition
- Dataset description (demo eICU)
- Evaluation metrics explanation
- Submission format
- Baseline performance
- Link to GitHub repo
- Citation for eICU-CRD

### 7.2 Update Project README
Add section about Codabench competition with link.

### 7.3 Update Benchmark Documentation
Add Codabench competition link to `BENCHMARK_DOCUMENTATION.md`.

---

## Timeline Estimate

| Step | Task | Time Estimate |
|------|------|--------------|
| 1 | Download + Extract Demo Dataset | 15 min (done) |
| 2 | Create processing script | 30-45 min |
| 3 | Create train/test splits | 15 min |
| 4 | Create evaluation script | 30 min |
| 5 | Create starter notebook | 45 min |
| 6 | Package competition bundle | 20 min |
| 7 | Upload to Codabench + test | 30-45 min |
| **Total** | **End-to-end** | **~3-4 hours** |

---

## Success Criteria

✅ **Competition is live** on Codabench
✅ **Participants can**:
   - Download train/test data
   - Train models locally
   - Submit predictions
   - See scores on leaderboard

✅ **Baseline performance**: F1 ~0.66 (similar to centralized)
✅ **Documentation**: Clear instructions for participants
✅ **Link in final report**: Can reference Codabench competition

---

## Next Steps (After Demo Dataset Downloads)

1. Extract demo dataset
2. Explore what tables/data are available
3. Start writing `process_demo_eicu.py`
4. Create processed dataset
5. Generate splits
6. Build evaluation script
7. Test locally before uploading

---

**Status**: ⏳ Waiting for demo dataset download to complete
**Est. Completion**: 1-2 minutes
