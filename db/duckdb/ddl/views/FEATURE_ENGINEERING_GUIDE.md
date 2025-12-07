# Feature Engineering Guide

SQL additions for `v_features_icu_stay_clean` view based on data preprocessing analysis.

## Summary

**15 new engineered features** ready to add to the view, covering:
- Patient characteristics (BMI, age groups)
- Neurological status (total GCS score, severity)
- Vital sign variability (HR/RR/SaO2 ranges)
- Clinical flags (emergency admission, critical vitals, AKI)
- Physiological changes (creatinine change)

## Feature Catalog

### 1. Body Mass Index (BMI)
**Availability**: 91.2% of records

```sql
bmi                 -- Continuous (kg/m²)
bmi_category       -- Categorical: underweight/normal/overweight/obese_class1/obese_class2/obese_class3
```

**Clinical Significance**:
- BMI correlates with ICU outcomes
- Obesity affects medication dosing, ventilation requirements
- Both extremes (very low/high BMI) associated with worse outcomes

---

### 2. Glasgow Coma Scale (GCS) Total
**Availability**: 85.5% of records

```sql
gcs_total          -- Continuous (3-15, lower = worse)
gcs_severity       -- Categorical: severe (≤8) / moderate (9-12) / mild (≥13)
```

**Clinical Significance**:
- Gold standard for neurological assessment
- GCS ≤8 typically requires intubation
- Strong predictor of mortality and functional outcomes
- Single score easier for models than 3 separate components

---

### 3. Vital Sign Variability (24-hour ranges)
**Availability**: HR (95.8%), RR (88.3%), SaO2 (94.4%)

```sql
hr_range_24h       -- Heart rate variability (max - min)
rr_range_24h       -- Respiratory rate variability
sao2_range_24h     -- Oxygen saturation variability
```

**Clinical Significance**:
- Higher variability indicates physiological instability
- May predict need for prolonged monitoring
- Captures information beyond simple averages
- Useful for identifying patients with fluctuating status

---

### 4. Age Groups
**Availability**: 100% (from age_numeric)

```sql
age_group          -- Categorical: pediatric/<18 / young_adult/18-44 / middle_age/45-64 / elderly/65-79 / very_elderly/≥80
```

**Clinical Significance**:
- Non-linear relationship between age and outcomes
- Elderly patients have different risk profiles
- Allows model to learn age-specific patterns
- Better than treating age as purely continuous

---

### 5. Emergency Admission Flag
**Availability**: 75.4% (where hospitaladmitsource is not null)

```sql
is_emergency_admission  -- Binary: 1 = admitted via ED, 0 = other
```

**Clinical Significance**:
- Emergency admissions often more acute/unpredictable
- Different from elective ICU admissions
- May indicate less preparation time for optimization
- Proxy for acuity of illness

---

### 6. Combined Pressor Use
**Availability**: 33.9% (where pressor data available)

```sql
any_pressor_24h    -- Binary: 1 = any pressor used, 0 = none
```

**Clinical Significance**:
- Simplifies 3 separate pressor flags
- Indicates hemodynamic instability
- Reduces dimensionality while preserving key information
- Often more relevant than specific pressor type

---

### 7. Critical Vital Signs Flags
**Availability**: Variable by vital sign

```sql
had_bradycardia_24h    -- Binary: min HR < 40
had_tachycardia_24h    -- Binary: max HR > 130
had_hypoxemia_24h      -- Binary: min SaO2 < 90
```

**Clinical Significance**:
- Captures presence of critical abnormalities
- More interpretable than raw min/max values
- Clinical thresholds based on standard criteria
- Binary flags easier for some models to learn

---

### 8. Acute Kidney Injury (AKI) Detection
**Availability**: Where both apache_creatinine and creatinine_mean_24h available

```sql
creatinine_change_24h  -- Continuous: change in creatinine
has_aki_24h           -- Binary: >50% increase = AKI
```

**Clinical Significance**:
- AKI is major ICU complication
- Associated with prolonged stays and worse outcomes
- 50% increase is one criterion for KDIGO AKI Stage 1
- Captures acute deterioration in kidney function

---

## Implementation Priority

### High Priority (Implement First)
1. **gcs_total** - Strong clinical predictor, simpler than 3 components
2. **bmi** - Well-established risk factor, high availability
3. **age_group** - Captures non-linear age effects
4. **any_pressor_24h** - Simplifies pressor flags, reduces dimensionality

### Medium Priority
5. **hr_range_24h, rr_range_24h, sao2_range_24h** - Adds variability information
6. **has_aki_24h** - Important complication indicator
7. **is_emergency_admission** - Admission context

### Optional (Consider Based on Model Performance)
8. **bmi_category** - Categorical version of BMI
9. **gcs_severity** - Categorical version of GCS
10. **had_bradycardia_24h, had_tachycardia_24h, had_hypoxemia_24h** - Specific alerts
11. **creatinine_change_24h** - Continuous version of AKI

---

## Impact on Multicollinearity

**Features that may increase correlation:**
- `bmi` with `admissionweight` and `admissionheight` (by design - composite feature)
- `gcs_total` with `apache_gcs_eyes/verbal/motor` (by design - composite feature)
- `any_pressor_24h` with individual pressor flags (by design - aggregation)

**Recommendation**:
- When adding composite features (BMI, GCS total, any_pressor), consider removing the individual components during model training to avoid perfect multicollinearity
- Or use regularization (L1/L2) which handles multicollinearity naturally

---

## SQL Integration Steps

1. **Open**: `db/duckdb/ddl/views/10_v_features_icu_stay_clean.sql`

2. **Add after existing features** (after infusion features block):
   ```sql
   -- Infusion features
   pressor_norepi_24h,
   pressor_epi_24h,
   pressor_vaso_24h,
   sedative_propofol_24h,

   -- ===== ENGINEERED FEATURES =====
   -- (paste features from feature_engineering_additions.sql here)
   ```

3. **Test the view**:
   ```sql
   CREATE OR REPLACE VIEW v_features_icu_stay_clean AS ...;

   SELECT
       bmi, gcs_total, hr_range_24h, age_group,
       is_emergency_admission, any_pressor_24h, has_aki_24h
   FROM v_features_icu_stay_clean
   LIMIT 100;
   ```

4. **Verify data quality**:
   ```sql
   -- Check availability
   SELECT
       COUNT(*) as total_records,
       COUNT(bmi) as has_bmi,
       COUNT(gcs_total) as has_gcs,
       COUNT(hr_range_24h) as has_hr_range
   FROM v_features_icu_stay_clean;

   -- Check value ranges
   SELECT
       MIN(bmi) as min_bmi, MAX(bmi) as max_bmi,
       MIN(gcs_total) as min_gcs, MAX(gcs_total) as max_gcs
   FROM v_features_icu_stay_clean;
   ```

---

## Expected Results

After adding these features:
- **Current**: 77 columns in v_features_icu_stay_clean
- **After**: ~92 columns (if all features added)
- **Recommended subset**: ~84 columns (high + medium priority features)

**Feature count by category**:
- Original features: 77
- BMI features: +2 (bmi, bmi_category)
- GCS features: +2 (gcs_total, gcs_severity)
- Vital ranges: +3 (hr_range_24h, rr_range_24h, sao2_range_24h)
- Age group: +1 (age_group)
- Emergency admission: +1 (is_emergency_admission)
- Pressor combination: +1 (any_pressor_24h)
- Critical vitals: +3 (bradycardia, tachycardia, hypoxemia flags)
- AKI features: +2 (creatinine_change_24h, has_aki_24h)

---

## Notes for Preprocessing Pipeline

After Jim adds these features to the view, update the preprocessing code to:

1. **Add to categorical features list**:
   - `bmi_category`
   - `gcs_severity`
   - `age_group`

2. **No changes needed for**:
   - Binary flags (already 0/1, no encoding needed)
   - Continuous features (will be scaled with others)

3. **Consider removing original components** to avoid multicollinearity:
   - If using `gcs_total`: remove `apache_gcs_eyes`, `apache_gcs_verbal`, `apache_gcs_motor`
   - If using `bmi`: consider removing `admissionweight`, `admissionheight` (but keep both available for imputation)
   - If using `any_pressor_24h`: remove individual pressor flags OR use feature selection

4. **Update feature importance analysis**:
   - Check if engineered features improve model performance
   - Compare to using original component features
   - May reveal new insights about prolonged stay predictors
