# Evaluation

## Evaluation Metric

Submissions are ranked by **F1 Score (macro-averaged)**.

### Why Macro-Averaged F1?

F1 Score (macro) gives equal weight to both classes:
- **Not Prolonged** (≤3 days) - 78.2% of cases
- **Prolonged** (>3 days) - 21.8% of cases

This is important because:
1. The dataset is imbalanced (78/22 split)
2. Both classes are clinically important
3. Simple accuracy would favor predicting "not prolonged" always
4. Healthcare applications need balanced sensitivity and specificity

### Calculation

```python
from sklearn.metrics import f1_score

# F1 for each class
f1_class_0 = f1_score(y_true, y_pred, pos_label=0)
f1_class_1 = f1_score(y_true, y_pred, pos_label=1)

# Macro average (unweighted mean)
f1_macro = (f1_class_0 + f1_class_1) / 2
```

### Additional Metrics

The leaderboard also displays:
- **Accuracy**: Overall correct predictions
- **Precision (Macro)**: Average precision across both classes
- **Recall (Macro)**: Average recall across both classes

These metrics are for informational purposes. Ranking is based solely on F1 (macro).

## Submission Format

### Required Format

Your submission must be a CSV file with exactly 2 columns:

```csv
patientunitstayid,prediction
3186183,0
1718412,0
349322,0
1318254,1
3142950,1
...
```

### Requirements

1. **Column names**: Must be `patientunitstayid` and `prediction` (case-sensitive)
2. **Row count**: Must have exactly 1,008 rows (one per test sample)
3. **Predictions**: Must be binary (0 or 1)
   - `0` = Not prolonged (≤3 days)
   - `1` = Prolonged (>3 days)
4. **Patient IDs**: Must match the test set exactly
5. **No header duplication**: Only one header row
6. **No index column**: Do not include row numbers

### Common Errors

❌ **Wrong column names**
```csv
id,label  # Wrong!
```

✅ **Correct column names**
```csv
patientunitstayid,prediction  # Correct!
```

❌ **Float predictions**
```csv
patientunitstayid,prediction
3186183,0.8  # Wrong! Must be 0 or 1
```

✅ **Binary predictions**
```csv
patientunitstayid,prediction
3186183,1  # Correct!
```

❌ **Wrong number of rows**
```csv
# Only 1000 rows submitted (need 1008)
```

### Creating a Valid Submission

```python
import pandas as pd

# Load test data
test_df = pd.read_csv('test.csv')

# Get predictions from your model
predictions = model.predict(X_test)  # Binary: 0 or 1

# Create submission
submission = pd.DataFrame({
    'patientunitstayid': test_df['patientunitstayid'],
    'prediction': predictions
})

# Validate
assert len(submission) == 1008, "Must have 1008 rows"
assert set(submission['prediction'].unique()).issubset({0, 1}), "Predictions must be 0 or 1"

# Save
submission.to_csv('predictions.csv', index=False)
```

## Submission Limits

- **Development Phase**: Maximum 5 submissions per day
- **Final Phase**: Maximum 2 submissions (select your best from development)

## Evaluation Process

1. Your prediction file is uploaded
2. Format validation checks (columns, row count, binary values)
3. Predictions are compared against hidden test labels
4. Metrics are computed (F1 macro, accuracy, precision, recall)
5. Results appear on the leaderboard

## Leaderboard

The leaderboard shows:
- Your username
- F1 Score (Macro) - **RANKING METRIC**
- Accuracy
- Precision (Macro)
- Recall (Macro)
- Submission date/time

Ties are broken by submission time (earlier is better).

## Tips for Good Scores

1. **Handle class imbalance**
   - Use `class_weight='balanced'` in sklearn models
   - Try SMOTE or other oversampling techniques
   - Tune classification threshold

2. **Optimize for F1, not accuracy**
   - High accuracy can hide poor minority class performance
   - Focus on balanced precision and recall

3. **Validate locally**
   - Create your own validation split
   - Compute F1 (macro) during development
   - Ensure both classes are predicted reasonably

4. **Use the baseline**
   - Start with the baseline notebook (F1 = 0.7547)
   - Understand what's working
   - Incrementally improve

## Example Evaluation Output

```json
{
  "f1_macro": 0.7547,
  "accuracy": 0.8075,
  "precision_macro": 0.7362,
  "recall_macro": 0.7999
}
```

Your score will be the `f1_macro` value.

Good luck! 🎯
