# Codabench Competition Bundle

This directory contains all files needed to create the **ICU Prolonged Stay Prediction Challenge** on Codabench.

## Directory Structure

```
codabench_bundle/
├── public_data/
│   ├── train.csv                     # Training data with labels (1,512 samples)
│   └── test.csv                      # Test features only (1,008 samples)
├── reference_data/
│   └── test_labels.csv               # Ground truth labels (hidden from participants)
├── scoring_program/
│   ├── score.py                      # Evaluation script
│   ├── test_score.py                 # Local test script
│   ├── requirements.txt              # Python dependencies
│   └── metadata                      # Execution configuration
├── starting_kit/
│   ├── baseline_notebook.ipynb       # Complete baseline solution
│   ├── sample_submission.csv         # Submission format example
│   └── README.md                     # Participant instructions
├── competition.yaml                  # Codabench configuration
└── README.md                         # This file
```

## Competition Details

**Task**: Binary classification to predict prolonged ICU stays (>3 days)

**Dataset**: eICU Collaborative Research Database (demo version)
- 2,520 total ICU stays
- 60/40 train/test split (stratified)
- 80+ clinical features
- Class distribution: 78.2% not prolonged, 21.8% prolonged

**Evaluation Metric**: F1 Score (macro-averaged)

**Baseline Performance**: **F1 = 0.7547** (Logistic Regression on test set)

## Files Description

### Public Data (Visible to Participants)

1. **train.csv** (1,512 samples)
   - Features: demographics, vital signs, lab values, APACHE scores
   - Labels: `prolonged_stay` (0 = ≤3 days, 1 = >3 days)
   - Participants train their models on this data

2. **test.csv** (1,008 samples)
   - Same features as training data
   - NO labels (hidden for evaluation)
   - Participants make predictions on this data

### Reference Data (Hidden from Participants)

3. **test_labels.csv** (1,008 samples)
   - Ground truth labels for test set
   - Used by scoring program to evaluate submissions
   - Format: `patientunitstayid, prolonged_stay`

### Scoring Program

4. **score.py**
   - Main evaluation script run by Codabench
   - Computes: F1 (macro), Accuracy, Precision (macro), Recall (macro)
   - Validates submission format
   - Outputs `scores.json` with results

5. **requirements.txt**
   - Python dependencies: pandas, scikit-learn, numpy
   - Installed by Codabench before running scoring

6. **metadata**
   - Execution command: `python3 $program/score.py`

### Starting Kit (Help for Participants)

7. **baseline_notebook.ipynb**
   - Complete walkthrough from data loading to submission
   - Achieves **F1 = 0.7547** on test set (validation F1 = 0.7945)
   - Includes EDA, preprocessing, training, evaluation
   - Ready to run on the competition data

8. **sample_submission.csv**
   - Example submission format
   - All predictions set to 0 (placeholder)
   - Participants replace with their predictions

9. **README.md** (starting_kit/)
   - Detailed participant guide
   - Quick start instructions
   - Feature descriptions
   - Submission format requirements

### Configuration

10. **competition.yaml**
    - Codabench competition configuration
    - Defines phases, leaderboard, rules
    - Two phases: Development (5 subs/day), Final (2 subs)
    - HTML description for competition page

## How to Use This Bundle

### Option 1: Upload to Codabench (Recommended)

1. **Zip the bundle**:
   ```bash
   cd /path/to/ari510capstone-fedlearn
   zip -r codabench_competition.zip codabench_bundle/
   ```

2. **Upload to Codabench**:
   - Go to https://www.codabench.org/
   - Create account / Login
   - Navigate to "Competitions" → "Create Competition"
   - Upload `codabench_competition.zip`
   - Follow the web interface prompts

3. **Test submission**:
   - Download the starting kit
   - Run baseline notebook to generate predictions
   - Submit `predictions.csv`
   - Verify scoring works and leaderboard updates

### Option 2: Local Testing

Test the evaluation script locally before uploading:

```bash
# Setup test environment
mkdir -p /tmp/codabench_test/input/ref /tmp/codabench_test/input/res /tmp/codabench_test/output

# Copy reference data
cp codabench_bundle/reference_data/test_labels.csv /tmp/codabench_test/input/ref/

# Create predictions (using sample submission as example)
cp codabench_bundle/starting_kit/sample_submission.csv /tmp/codabench_test/input/res/predictions.csv

# Run scoring
cd codabench_bundle/scoring_program
python test_score.py

# Check output
cat /tmp/codabench_test/output/scores.json
```

Expected output:
```json
{
  "f1_macro": 0.4388,
  "accuracy": 0.7817,
  "precision_macro": 0.3909,
  "recall_macro": 0.5000
}
```

## Submission Format

Participants must submit a CSV file with exactly 2 columns:

| patientunitstayid | prediction |
|-------------------|------------|
| 141203            | 0          |
| 141245            | 1          |
| 141277            | 0          |
| ...               | ...        |

**Requirements**:
- Must have 1,008 rows (one per test sample)
- Column names: `patientunitstayid`, `prediction`
- Predictions must be binary: 0 (not prolonged) or 1 (prolonged)
- Patient IDs must match test set

## Evaluation Metrics

### Primary Metric: F1 Score (Macro)

```python
from sklearn.metrics import f1_score
f1 = f1_score(y_true, y_pred, average='macro')
```

Macro-averaging:
1. Compute F1 for class 0 (not prolonged)
2. Compute F1 for class 1 (prolonged)
3. Take unweighted mean: `(F1_class0 + F1_class1) / 2`

**Why macro?** Gives equal importance to both classes, even though dataset is imbalanced (78/22 split). Important in medical contexts where minority class (prolonged stays) is critical.

### Secondary Metrics

- **Accuracy**: Overall correct predictions
- **Precision (Macro)**: Average precision across both classes
- **Recall (Macro)**: Average recall across both classes

All metrics displayed on leaderboard.

## Dataset Information

### Source
**eICU Collaborative Research Database (demo version)**
- Published by: MIT Laboratory for Computational Physiology
- Available: https://physionet.org/content/eicu-crd-demo/2.0.1/
- License: Open Data Commons Open Database License v1.0
- No credentials required (public demo dataset)

### Citation
```
Pollard, T. J., Johnson, A. E. W., Raffa, J. D., Celi, L. A., Mark, R. G.,
& Badawi, O. (2018). The eICU Collaborative Research Database, a freely
available multi-center database for critical care research. Scientific Data,
5, 180178. https://doi.org/10.1038/sdata.2018.178
```

### Processing
Original demo dataset (2,520 ICU stays) was processed using:
- Feature engineering from raw tables (patient, vitalPeriodic, lab, apachePatientResult)
- Aggregation of time-series data (mean, std, min, max)
- Target creation: `prolonged_stay = 1 if LOS > 3 days, else 0`
- Stratified 60/40 train/test split (random_state=42)

See `src/fedlearn/tools/process_demo_eicu.py` for details.

## Competition Rules

1. **Submission Limits**:
   - Development phase: 5 submissions per day, 100 total
   - Final phase: 2 submissions (best from development)

2. **Allowed**:
   - Any ML algorithm or ensemble
   - Feature engineering from provided features
   - Cross-validation on training data

3. **Not Allowed**:
   - External data sources
   - Manual labeling
   - Using test.csv labels (obviously not available!)

4. **Evaluation**:
   - Predictions evaluated on hidden test_labels.csv
   - Immediate feedback in development phase
   - Final ranking in final phase

## Troubleshooting

### Validation Errors

If your submission fails validation:

1. **Check column names**: Must be `patientunitstayid` and `prediction` (case-sensitive)
2. **Check row count**: Must have exactly 1,008 rows
3. **Check predictions**: Must be 0 or 1 (no floats, no other values)
4. **Check patient IDs**: Must match test.csv exactly

### Scoring Errors

If scoring fails:

1. Check `scoring_program/test_score.py` works locally
2. Ensure predictions file is named `predictions.csv`
3. Verify no NaN or missing values
4. Check file encoding (should be UTF-8)

### Performance Issues

If your model doesn't improve:

1. Review baseline notebook for ideas
2. Handle missing values better (median imputation → KNN imputation)
3. Use categorical features (gender, ethnicity)
4. Try different models (Random Forest, XGBoost)
5. Tune hyperparameters
6. Handle class imbalance (SMOTE, class weights)

## Contact

**Project Team**: Jamie Ontiveros, Jim Prantzalos
**Institution**: University of Michigan-Flint
**Course**: ARI 510 (Fall 2025)
**Repository**: https://github.com/umdnp/ari510capstone-fedlearn

## License

Competition data: Open Data Commons Open Database License v1.0
Competition code: MIT License

---

**Ready to upload to Codabench!** 🚀
