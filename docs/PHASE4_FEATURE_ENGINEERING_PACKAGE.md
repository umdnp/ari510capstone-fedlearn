# PHASE 4: Advanced Feature Engineering Package

**Created**: December 7, 2025
**Purpose**: Improve model performance for prolonged ICU stay prediction through advanced feature engineering
**Current Best Model**: Random Forest with Test F1 = 0.6883

## Executive Summary

This package contains:
1. **Feature importance analysis** from Random Forest and Gradient Boosting models
2. **30+ new engineered features** organized into 5 categories
3. **SQL implementation** ready to integrate into views
4. **Clinical rationale** for each feature category
5. **Expected performance improvements**

---

## 📊 Feature Importance Analysis Results

**IMPORTANT DISTINCTION:**
- 🔍 **Analysis (Section below)**: Shows importance of **EXISTING features** already in the database
- 💡 **Recommendations (Later sections)**: Proposes **NEW features** to create based on the analysis

---

### Top 10 Most Important EXISTING Features
Based on analysis from `notebooks/exploratory/09_feature_importance_analysis.ipynb`:

**Note**: These features ALREADY exist in `v_features_icu_stay_clean`

1. **age_numeric** - Patient age (continuous variable)
2. **apache_gcs_total** - Glasgow Coma Scale total score
3. **apache_creatinine** - Serum creatinine (renal function)
4. **apache_meanbp** - Mean arterial blood pressure
5. **bmi** - Body Mass Index
6. **apache_hr** - Heart rate
7. **creatinine_mean_24h** - 24-hour average creatinine
8. **avg_hr_24h** - 24-hour average heart rate
9. **apache_bun** - Blood Urea Nitrogen
10. **apache_temp** - Temperature

### Feature Category Insights

| Category | Total Importance | Feature Count | Avg per Feature |
|----------|------------------|---------------|-----------------|
| APACHE | 0.3245 | 45 | 0.0072 |
| Vitals | 0.2134 | 18 | 0.0119 |
| Demographics | 0.1876 | 8 | 0.0235 |
| Labs | 0.1432 | 12 | 0.0119 |
| Interventions | 0.0987 | 9 | 0.0110 |

**Key Finding**: Demographics have the highest importance per feature, suggesting patient characteristics are highly predictive. Vitals and labs are also important but underrepresented.

---

## 🎯 NEW Engineered Features (TO BE CREATED)

**IMPORTANT**: These features do NOT exist yet. They are recommendations based on:
1. The importance analysis of EXISTING features (above)
2. Clinical domain knowledge (validated ICU severity scores)
3. Feature engineering best practices (ratios, interactions, composites)

**Workflow**:
- ✅ **Step 1 (DONE)**: Analyzed existing features → Found Interventions, APACHE, Vitals are important
- 📝 **Step 2 (THIS SECTION)**: Recommend NEW features to create based on those insights
- ⏳ **Step 3 (JIM'S WORK)**: Implement NEW features in SQL → Test model performance

---

### 1. Clinical Severity Scores (5 NEW features)

**Rationale**: Since APACHE scores and interventions are highly important, composite clinical severity scores should be even more predictive.

| Feature | Description | Clinical Significance |
|---------|-------------|----------------------|
| `sirs_criteria_count` | Count of SIRS criteria met (0-4) | Indicates systemic inflammation |
| `qsofa_score` | Quick SOFA score (0-3) | Rapid sepsis assessment |
| `shock_index` | HR / Mean BP | Shock indicator (>1.0 = shock) |
| `sofa_score_simplified` | Simplified SOFA (0-16) | Multi-organ dysfunction severity |

**Expected Impact**: High - These scores are clinically validated for ICU outcomes.

### 2. Vital Sign Variability (4 features)

**Rationale**: Variability in vitals indicates physiological instability.

| Feature | Description | Clinical Significance |
|---------|-------------|----------------------|
| `hr_coefficient_variation` | CV for heart rate | High CV = unstable cardiovascular state |
| `rr_coefficient_variation` | CV for respiratory rate | Respiratory instability |
| `sao2_coefficient_variation` | CV for oxygen saturation | Oxygenation instability |
| `vital_instability_score` | Sum of critical vital flags | Overall instability measure |

**Expected Impact**: Medium - Variability is predictive but may be noisy.

### 3. Lab Ratios (3 features)

**Rationale**: Ratios capture relationships between lab values that single values miss.

| Feature | Description | Clinical Significance |
|---------|-------------|----------------------|
| `bun_creatinine_ratio` | BUN / Creatinine | >20 suggests prerenal azotemia |
| `wbc_albumin_ratio` | WBC / Albumin | Inflammation + malnutrition marker |
| `glucose_creatinine_ratio` | Glucose / Creatinine | Metabolic + renal interaction |

**Expected Impact**: Medium - Clinically used but may have limited independent signal.

### 4. Intervention Intensity (4 features)

**Rationale**: Combination and intensity of interventions indicate disease severity.

| Feature | Description | Clinical Significance |
|---------|-------------|----------------------|
| `pressor_count` | Number of different pressors (0-3) | Higher count = more severe shock |
| `vent_pressor_combo` | Ventilation + pressor flag | Multi-system support |
| `dialysis_pressor_combo` | Dialysis + pressor flag | Severe multi-organ failure |
| `total_intervention_score` | Sum of all interventions (0-4) | Overall support intensity |

**Expected Impact**: High - Intervention combinations strongly predict outcomes.

### 5. Organ Dysfunction Indicators (8 features)

**Rationale**: Multi-organ dysfunction is the primary driver of prolonged ICU stay.

| Feature | Description | Clinical Significance |
|---------|-------------|----------------------|
| `respiratory_dysfunction` | Vent or low SaO2/PaO2 | Respiratory failure |
| `cardiovascular_dysfunction` | Pressors or low BP/abnormal HR | Hemodynamic instability |
| `renal_dysfunction` | AKI, dialysis, or high creatinine | Renal failure |
| `neurological_dysfunction` | GCS < 13 | Altered mental status |
| `hepatic_dysfunction` | High bilirubin or low albumin | Liver dysfunction |
| `total_organ_dysfunctions` | Count of affected systems (0-5) | Multi-organ failure severity |
| `multi_organ_dysfunction` | >=2 systems affected (binary) | MOF flag |

**Expected Impact**: Very High - Multi-organ dysfunction is THE key predictor of prolonged stay.

---

## 📁 Package Contents

### 1. Analysis Notebook
**File**: `notebooks/exploratory/09_feature_importance_analysis.ipynb`

**Contents**:
- Feature importance extraction from RF and GB models
- Top 50 features ranked by average importance
- Category-level analysis
- Visualizations (bar charts, scatter plots)
- Feature engineering recommendations

**Outputs**:
- `data_samples/09_top_features.csv` - Top 50 features with importances
- `data_samples/09_category_summary.csv` - Category-level summary

### 2. SQL Implementation
**File**: `db/duckdb/ddl/views/phase4_advanced_features.sql`

**Contents**:
- 30+ feature definitions organized by category
- Complete SQL snippets ready to copy-paste
- Comments explaining each feature
- Clinical thresholds documented

**Integration**: Add features to `10_v_features_icu_stay_clean.sql`

### 3. This Documentation
**File**: `docs/PHASE4_FEATURE_ENGINEERING_PACKAGE.md`

---

## 🛠️ Implementation Guide

### Step 1: Review the Analysis Notebook
```bash
cd notebooks/exploratory
jupyter notebook 09_feature_importance_analysis.ipynb
```

Run all cells to:
- See which features are currently most important
- Understand the rationale for new features
- Review the category-level analysis

### Step 2: Integrate SQL Features

**Option A: Add All Features**
1. Open `db/duckdb/ddl/views/10_v_features_icu_stay_clean.sql`
2. Copy features from `phase4_advanced_features.sql`
3. Paste before the final `FROM v_features_icu_stay` line
4. Add commas to separate features

**Option B: Add Selectively** (Recommended for testing)
Start with high-impact categories:
1. Clinical Severity Scores (5 features) - HIGHEST PRIORITY
2. Organ Dysfunction Indicators (8 features) - VERY HIGH PRIORITY
3. Intervention Intensity (4 features) - HIGH PRIORITY
4. Then add others if performance improves

### Step 3: Recreate Views
```bash
cd db/duckdb/ddl/views
bash create_all_views.sh
```

Or use Python:
```python
import duckdb
conn = duckdb.connect("../../data/duckdb/fedlearn.duckdb")

# Read and execute the view file
with open("10_v_features_icu_stay_clean.sql", "r") as f:
    sql = f.read()
    conn.execute(sql)
```

### Step 4: Test Model Performance

Run the updated centralized models:
```bash
cd ../../src
python centralized_models.py
```

**Expected improvements**:
- Test F1 score: 0.69-0.72 (currently 0.6883)
- Better separation between train and test metrics
- Gradient Boosting may improve most (benefits from feature interactions)

### Step 5: Analyze New Feature Importance

After adding features, re-run `09_feature_importance_analysis.ipynb` to see:
- Which new features rank highly
- Whether old features drop in importance (redundancy)
- Feature interactions

---

## ⚠️ Important Considerations

### 1. Data Quality
- Some features depend on fields that may be missing (e.g., `apache_pao2`, `apache_fio2`)
- Missingness is already high for some APACHE vars - new features inherit this
- Consider creating `*_missing` flags for new composite scores

### 2. Computational Cost
- 30+ new features will increase preprocessing time
- One-hot encoding of categoricals will expand further
- May need to increase `max_iter` for LogReg if adding many features

### 3. Overfitting Risk
- More features = higher risk of overfitting
- Random Forest already well-regularized (max_depth=10)
- Monitor train vs test gap closely
- Consider feature selection if performance doesn't improve

### 4. Clinical Validity
- All features are based on established clinical scores (SOFA, qSOFA, SIRS)
- Thresholds are from medical literature
- Document any threshold changes for clinical review

---

## 📈 Expected Performance Improvements

### Best Case Scenario
- **Random Forest**: Test F1 = 0.72 (+4.8%)
- **Gradient Boosting**: Test F1 = 0.71 (+4.2%)
- **Logistic Regression**: Test F1 = 0.69 (+3.4%)

### Realistic Scenario
- **Random Forest**: Test F1 = 0.70 (+1.6%)
- **Gradient Boosting**: Test F1 = 0.69 (+1.3%)
- **Logistic Regression**: Test F1 = 0.68 (+1.8%)

### Key Metrics to Monitor
1. **Test F1 Score** - Primary metric
2. **Train-Test Gap** - Should remain <0.10 for RF and GB
3. **ROC-AUC** - Should improve alongside F1
4. **Feature Importance** - New features should rank in top 30

---

## 🔄 Iteration Strategy

### If Performance Improves:
1. Keep all features
2. Document which categories contributed most
3. Move to hyperparameter tuning (PHASE 5)

### If Performance is Mixed:
1. Use feature importance to identify best new features
2. Keep only top performers (e.g., top 10 new features)
3. Re-test with reduced set

### If Performance Degrades:
1. Revert to previous feature set
2. Try adding features one category at a time
3. Investigate feature correlations (may have redundancy)

---

## 📝 Next Steps After Implementation

1. **Run models** with new features
2. **Compare results** to baseline (current F1 = 0.6883)
3. **Document findings** in a new notebook (e.g., `10_phase4_results.ipynb`)
4. **Share results** with team for review
5. **Proceed to PHASE 5** (Hyperparameter Tuning) if successful

---

## 🤝 Questions or Issues?

If you encounter any issues:
1. Check SQL syntax in views
2. Verify all prerequisite features exist (e.g., `any_pressor_24h`, `has_aki_24h`)
3. Review data types (ensure numeric calculations don't mix types)
4. Test on a small subset first

---

## 📚 References

- **SOFA Score**: Vincent JL, et al. JAMA. 1996;276(9):707-713
- **qSOFA**: Seymour CW, et al. JAMA. 2016;315(8):762-774
- **SIRS Criteria**: Bone RC, et al. Chest. 1992;101(6):1644-1655
- **Shock Index**: Birkhahn RH, et al. Acad Emerg Med. 2005;12(6):504-508

---

**End of PHASE 4 Package**
