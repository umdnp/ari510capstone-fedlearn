# PHASE 5: Hyperparameter Tuning Package

**Created**: December 7, 2025
**Purpose**: Optimize model hyperparameters to maximize prediction performance
**Current Best Model**: Random Forest with Test F1 = 0.6883

## Executive Summary

This package contains:
1. **Hyperparameter tuning notebook** with Grid Search and Randomized Search
2. **Parameter grids** for each model (Random Forest, Gradient Boosting, Logistic Regression)
3. **Ready-to-run code** for hyperparameter optimization
4. **Best practices** for tuning strategy
5. **Expected performance improvements**

---

## 📊 Current Model Performance (Baseline)

**From PHASE 3 (before tuning)**:

| Model | Test F1 Score | Train-Test Gap | Status |
|-------|---------------|----------------|--------|
| **Random Forest** | 0.6883 | 0.0198 | Best current model |
| **Gradient Boosting** | 0.6811 | 0.0234 | Close second |
| **Logistic Regression** | 0.6673 | -0.0001 | No overfitting |
| **SGD Classifier** | 0.5752 | -0.0017 | Underperforming |

**Key Observations**:
- Random Forest and Gradient Boosting are top performers
- Minimal overfitting across all models (good regularization)
- Logistic Regression has zero overfitting but lower performance
- Room for improvement through hyperparameter tuning

---

## 🎯 Expected Performance Improvements

### Realistic Targets:

| Model | Current F1 | Target F1 | Expected Gain | Priority |
|-------|------------|-----------|---------------|----------|
| **Random Forest** | 0.6883 | 0.70-0.71 | +1-3% | HIGH |
| **Gradient Boosting** | 0.6811 | 0.70-0.71 | +2-4% | HIGH |
| **Logistic Regression** | 0.6673 | 0.68-0.69 | +1-2% | MEDIUM |

### Why These Targets?

1. **Random Forest**: Currently using conservative parameters (max_depth=10). Increasing depth and trees should help.

2. **Gradient Boosting**: Has most room for improvement. Learning rate and subsample tuning often yield significant gains.

3. **Logistic Regression**: Less sensitive to hyperparameters, but C (regularization strength) can help.

---

## 📁 Package Contents

### 1. Hyperparameter Tuning Notebook
**File**: `notebooks/exploratory/10_hyperparameter_tuning.ipynb`

**Contents**:
- Data loading and train/val/test split (60/20/20)
- Grid Search for Random Forest (108 combinations)
- Randomized Search for Gradient Boosting (30 random samples)
- Grid Search for Logistic Regression (12 combinations)
- Validation set evaluation
- Final test set evaluation
- Visualization of results
- Export of best hyperparameters

**Runtime Estimates**:
- Random Forest Grid Search: 30-60 minutes
- Gradient Boosting Randomized Search: 20-40 minutes
- Logistic Regression Grid Search: 5-10 minutes
- **Total**: ~1-2 hours on modern hardware

---

## 🔧 Hyperparameter Grids

### Random Forest Parameters

**Current (PHASE 3)**:
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=20,
    min_samples_leaf=10,
    class_weight="balanced",
    random_state=42,
)
```

**Tuning Grid**:
```python
{
    'n_estimators': [100, 200, 300],         # More trees = better ensemble
    'max_depth': [8, 10, 12, 15],            # Deeper trees = more complex patterns
    'min_samples_split': [10, 20, 30],       # Lower = more splits (risk overfitting)
    'min_samples_leaf': [5, 10, 15],         # Lower = finer predictions
}
```

**Total combinations**: 108
**Strategy**: Grid Search (exhaustive)
**Rationale**: Random Forest is our best model, worth thorough search

---

### Gradient Boosting Parameters

**Current (PHASE 3)**:
```python
GradientBoostingClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42,
)
```

**Tuning Grid**:
```python
{
    'n_estimators': [100, 200, 300],         # More iterations
    'max_depth': [3, 5, 7],                  # Shallower than RF (boosting uses weak learners)
    'learning_rate': [0.05, 0.1, 0.2],       # Lower = slower but more accurate
    'subsample': [0.8, 0.9, 1.0],            # Stochastic gradient boosting
}
```

**Total combinations**: 81
**Strategy**: Randomized Search (30 iterations)
**Rationale**: Gradient Boosting is slower, randomized search more efficient

---

### Logistic Regression Parameters

**Current (PHASE 3)**:
```python
LogisticRegression(
    max_iter=1000,
    C=1.0,                 # Default
    solver='lbfgs',
    penalty='l2',
    class_weight="balanced",
    random_state=42,
)
```

**Tuning Grid**:
```python
{
    'C': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],  # Regularization strength (lower = more regularization)
    'solver': ['lbfgs', 'liblinear'],            # Different optimization algorithms
    'penalty': ['l2'],                           # L2 regularization
}
```

**Total combinations**: 12
**Strategy**: Grid Search (small grid, fast)
**Rationale**: Logistic Regression is fast, can afford exhaustive search

---

## 🛠️ Implementation Guide

### Step 1: Review Current Performance
Make sure you understand the baseline performance from PHASE 3:
```bash
python -m fedlearn.centralized.centralized_models
```

### Step 2: Run Hyperparameter Tuning Notebook

**Option A: Run All Models** (Recommended, ~1-2 hours)
```bash
cd notebooks/exploratory
jupyter notebook 10_hyperparameter_tuning.ipynb
```
Run all cells sequentially.

**Option B: Run Selectively** (Faster)
Run only the highest priority models:
1. Random Forest (HIGH priority, best current model)
2. Gradient Boosting (HIGH priority, most room for improvement)
3. Skip Logistic Regression initially (MEDIUM priority)

### Step 3: Analyze Results

After running the notebook:
1. Check the "HYPERPARAMETER TUNING RESULTS" table
2. Identify which models improved most
3. Review the "Improvement from Hyperparameter Tuning" bar chart
4. Export results: `data_samples/10_best_hyperparameters.csv`

### Step 4: Update centralized_models.py

Replace the old parameters with the best parameters from the tuning results.

**Note**: After directory restructure, the file is now located at `src/fedlearn/centralized/centralized_models.py`

**Example**:
If tuning found these best parameters for Random Forest:
```python
{
    'classifier__n_estimators': 200,
    'classifier__max_depth': 12,
    'classifier__min_samples_split': 10,
    'classifier__min_samples_leaf': 5,
}
```

Update `src/fedlearn/centralized/centralized_models.py`:
```python
RF = Pipeline([
    ("preprocessor", build_preprocessor(X)),
    ("classifier", RandomForestClassifier(
        n_estimators=200,        # Updated from 100
        max_depth=12,            # Updated from 10
        min_samples_split=10,    # Updated from 20
        min_samples_leaf=5,      # Updated from 10
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )),
])
```

### Step 5: Validate on Test Set

After updating parameters, run:
```bash
python -m fedlearn.centralized.centralized_models
```

Verify that test F1 scores match or exceed the notebook results.

---

## ⚠️ Important Considerations

### 1. Computational Resources
- **Grid Search** is exhaustive but slow
- **Randomized Search** is faster and often finds good solutions
- Use `n_jobs=-1` to parallelize across all CPU cores
- Expect 1-2 hours for full tuning on modern hardware

### 2. Overfitting Risk
- Tuning on validation set is safe (that's what it's for!)
- **Never tune on test set** - it's for final evaluation only
- Monitor train-test gap - should stay < 0.10 for RF and GB

### 3. Cross-Validation
- Using 3-fold CV during tuning (trade-off: speed vs accuracy)
- 5-fold CV would be more robust but 1.7x slower
- 3-fold is sufficient for dataset of 199k samples

### 4. When to Re-Tune
Re-run hyperparameter tuning if:
- New features are added (PHASE 4)
- Data distribution changes significantly
- Model performance degrades over time
- Switching to a different metric (e.g., from F1 to AUC)

---

## 📈 Interpreting Results

### Good Signs:
- ✅ Validation F1 > Baseline F1 (improvement)
- ✅ Test F1 ≈ Validation F1 (not overfit to validation set)
- ✅ Train-Test gap < 0.10 (well-regularized)

### Warning Signs:
- ⚠️ Validation F1 >> Test F1 (overfit to validation set - rare with CV)
- ⚠️ Train F1 >> Test F1 (overfit to training data - need more regularization)
- ⚠️ No improvement from tuning (parameters may already be optimal)

### If No Improvement:
1. **Check parameter ranges** - May need wider ranges
2. **Try different metrics** - Maybe F1 isn't the best for this task
3. **Feature engineering** - May need better features (PHASE 4)
4. **Ensemble methods** - Combine multiple models

---

## 🔄 Integration Workflow

### After Successful Tuning:

1. **Document Best Parameters**
   - Save `data_samples/10_best_hyperparameters.csv`
   - Note improvements in project documentation

2. **Update Production Code**
   - Modify `src/fedlearn/centralized/centralized_models.py` with best parameters
   - Add comments noting these are tuned parameters

3. **Re-Run Full Pipeline**
   - Verify test scores match notebook results
   - Confirm no overfitting

4. **Share Results**
   - Commit updated code and results
   - Share performance improvements with team

---

## 📊 Expected Notebook Output

After running the notebook, you should see:

### Validation Set Results Table:
```
Model                  Baseline F1  Tuned Val F1  Improvement  Tuning Time (min)
Random Forest          0.6883       0.7012        +0.0129      45.2
Gradient Boosting      0.6811       0.7034        +0.0223      32.8
Logistic Regression    0.6673       0.6842        +0.0169      8.1
```

### Final Test Set Results:
```
Model                  Test F1
Random Forest          0.7001
Gradient Boosting      0.7018
Logistic Regression    0.6831
```

**Note**: Actual results will vary based on the specific dataset and random seeds.

---

## 🎓 Hyperparameter Tuning Best Practices

### 1. Start Coarse, Then Refine
- First pass: Wide range, coarse grid (e.g., [10, 100, 1000])
- Second pass: Narrow around best values (e.g., [80, 90, 100, 110, 120])

### 2. Use Domain Knowledge
- Random Forest: Typically max_depth 10-20 for tabular data
- Gradient Boosting: learning_rate 0.01-0.2, max_depth 3-7
- Logistic Regression: C from 0.01-100

### 3. Balance Speed and Thoroughness
- Grid Search for small grids (<50 combinations)
- Randomized Search for large grids (>50 combinations)
- Bayesian Optimization for expensive evaluations (advanced)

### 4. Monitor Training Time
- If a single model takes >10 minutes, reduce grid size
- Prioritize high-impact parameters (e.g., n_estimators, max_depth)

---

## 📝 Next Steps After PHASE 5

### If Tuning Succeeds:
1. ✅ Update `src/fedlearn/centralized/centralized_models.py` with best parameters
2. ✅ Document improvements in project notes
3. ✅ Move to **PHASE 6: Federated Learning Implementation**

### If Results Are Mixed:
1. Implement PHASE 4 features first
2. Re-run hyperparameter tuning on new feature set
3. Compare: baseline → tuned → tuned + new features

### If No Improvement:
1. Review feature engineering (PHASE 4)
2. Try ensemble methods (stacking, voting)
3. Consider different model architectures

---

## 🤝 Questions or Issues?

### Common Issues:

**Q: Tuning takes too long**
A: Reduce grid size, use Randomized Search, or reduce cv folds to 2

**Q: No improvement from tuning**
A: Parameters may already be near-optimal. Focus on feature engineering instead.

**Q: Results don't match when re-running**
A: Ensure random_state=42 is set consistently. Check data preprocessing.

**Q: Different results on test vs validation**
A: Some variance is normal. Large differences suggest overfitting to validation set.

---

## 📚 References

- **Scikit-learn Grid Search**: https://scikit-learn.org/stable/modules/grid_search.html
- **Random Forest Tuning Guide**: https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74
- **Gradient Boosting Best Practices**: https://machinelearningmastery.com/configure-gradient-boosting-algorithm/

---

**End of PHASE 5 Package**
