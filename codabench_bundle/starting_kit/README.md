# ICU Prolonged Stay Prediction - Starting Kit

Welcome to the ICU Prolonged Stay Prediction Challenge!

## Challenge Overview

**Task**: Predict whether ICU patients will have a prolonged stay (>3 days) based on clinical features available at admission.

**Dataset**: eICU Collaborative Research Database (demo version)
- Training set: 1,512 ICU stays with labels
- Test set: 1,008 ICU stays (labels hidden)
- Features: 80+ clinical features including demographics, vital signs, lab values, and APACHE scores

**Evaluation Metric**: F1 Score (macro-averaged)
- Gives equal weight to both classes (prolonged vs. not prolonged)
- Appropriate for imbalanced medical datasets

## Files in This Kit

1. **baseline_notebook.ipynb** - Complete baseline solution with ~0.66 F1 score
2. **sample_submission.csv** - Example submission format

## Data Files (in public_data/)

1. **train.csv** - Training data with features + labels
   - Columns: patientunitstayid (ID), 80 features, prolonged_stay (target)
   - 1,512 samples

2. **test.csv** - Test data with features only (NO labels)
   - Columns: patientunitstayid (ID), 80 features
   - 1,008 samples

## Quick Start

### 1. Load the Data

```python
import pandas as pd

train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
```

### 2. Prepare Features

```python
# Separate features and target
X_train = train_df.drop(['patientunitstayid', 'prolonged_stay'], axis=1)
y_train = train_df['prolonged_stay']
X_test = test_df.drop(['patientunitstayid'], axis=1)
```

### 3. Train a Model

```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Preprocess (example)
imputer = SimpleImputer(strategy='median')
scaler = StandardScaler()

X_train_processed = scaler.fit_transform(imputer.fit_transform(X_train))
X_test_processed = scaler.transform(imputer.transform(X_test))

# Train
model = LogisticRegression(class_weight='balanced', random_state=42)
model.fit(X_train_processed, y_train)
```

### 4. Make Predictions

```python
predictions = model.predict(X_test_processed)
```

### 5. Create Submission

```python
submission = pd.DataFrame({
    'patientunitstayid': test_df['patientunitstayid'],
    'prediction': predictions
})
submission.to_csv('predictions.csv', index=False)
```

## Submission Format

Your submission must be a CSV file with exactly 2 columns:

- `patientunitstayid` - Patient unit stay ID (must match test set)
- `prediction` - Binary prediction (0 = not prolonged, 1 = prolonged)

**Example:**
```
patientunitstayid,prediction
141203,0
141245,1
141277,0
...
```

**Requirements:**
- Must have 1,008 rows (one per test sample)
- Predictions must be binary (0 or 1)
- Patient IDs must match the test set

## Evaluation

Submissions are evaluated using **F1 Score (macro-averaged)**:

```python
from sklearn.metrics import f1_score
f1 = f1_score(y_true, y_pred, average='macro')
```

**Macro-averaging** computes F1 for each class independently, then takes the unweighted mean. This ensures both classes are equally important, even though the dataset is imbalanced (78% not prolonged, 22% prolonged).

## Baseline Performance

The baseline Logistic Regression model (see `baseline_notebook.ipynb`) achieves:
- **F1 (macro)**: **0.7547** (test set)
- **Accuracy**: **0.8075** (test set)
- **Validation F1**: 0.7945

You can beat this by:
1. Using categorical features (gender, ethnicity)
2. Better imputation strategies
3. Feature engineering
4. Advanced models (Random Forest, Gradient Boosting, XGBoost)
5. Hyperparameter tuning
6. Ensemble methods
7. Handling class imbalance (SMOTE, etc.)

## Feature Descriptions

### Demographics
- `age` - Patient age (years)
- `gender` - Male/Female
- `ethnicity` - Patient ethnicity
- `admissionweight` - Admission weight (kg)

### Vital Signs (mean, std, min, max)
- `temperature` - Body temperature (°C)
- `sao2` - Oxygen saturation (%)
- `heartrate` - Heart rate (bpm)
- `respiration` - Respiratory rate (breaths/min)
- `systemicsystolic`, `systemicdiastolic`, `systemicmean` - Blood pressure (mmHg)

### Laboratory Values (mean, std, min, max)
- `WBC_x_1000` - White blood cell count
- `creatinine` - Kidney function marker
- `BUN` - Blood urea nitrogen
- `glucose` - Blood glucose
- `sodium`, `potassium`, `bicarbonate` - Electrolytes
- `platelets_x_1000` - Platelet count
- `Hct` - Hematocrit
- `Hgb` - Hemoglobin
- `total_bilirubin` - Liver function marker

### Clinical Scores
- `acutephysiologyscore` - APACHE acute physiology score
- `apachescore` - APACHE IV score
- `predictedicumortality` - Predicted ICU mortality
- `predictedhospitalmortality` - Predicted hospital mortality

## Tips

1. **Handle missing values carefully** - Many clinical features have missing data
2. **Use class weighting** - Dataset is imbalanced (78/22 split)
3. **Validate locally** - Create a validation split to tune your model
4. **Feature engineering** - Interaction terms, ratios, trends can help
5. **Don't overfit** - Keep it simple and validate thoroughly

## Dataset Citation

This competition uses the eICU Collaborative Research Database (demo version):

> Pollard, T. J., Johnson, A. E. W., Raffa, J. D., Celi, L. A., Mark, R. G., & Badawi, O. (2018). The eICU Collaborative Research Database, a freely available multi-center database for critical care research. Scientific Data, 5, 180178.

**License**: Open Data Commons Open Database License v1.0

## Questions?

- Review the baseline notebook for a complete example
- Check the competition forum for discussions
- Read the evaluation code to understand scoring

Good luck!
