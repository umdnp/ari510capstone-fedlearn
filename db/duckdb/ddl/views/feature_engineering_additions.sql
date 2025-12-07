-- ============================================================================
-- FEATURE ENGINEERING SQL ADDITIONS
-- ============================================================================
-- Suggested additions to v_features_icu_stay_clean view based on preprocessing analysis
--
-- These features can be added to the SELECT statement in 10_v_features_icu_stay_clean.sql
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. BMI (Body Mass Index)
-- ----------------------------------------------------------------------------
-- Formula: weight (kg) / (height (m))^2
-- Available for 91.2% of records (182,123 patients)
--
CASE
    WHEN admissionheight IS NOT NULL
     AND admissionweight IS NOT NULL
     AND admissionheight > 0
    THEN admissionweight / POWER(admissionheight / 100.0, 2)
    ELSE NULL
END as bmi,

-- Optional: BMI category (clinical interpretation)
CASE
    WHEN admissionheight IS NULL OR admissionweight IS NULL OR admissionheight = 0 THEN NULL
    WHEN admissionweight / POWER(admissionheight / 100.0, 2) < 18.5 THEN 'underweight'
    WHEN admissionweight / POWER(admissionheight / 100.0, 2) < 25.0 THEN 'normal'
    WHEN admissionweight / POWER(admissionheight / 100.0, 2) < 30.0 THEN 'overweight'
    WHEN admissionweight / POWER(admissionheight / 100.0, 2) < 35.0 THEN 'obese_class1'
    WHEN admissionweight / POWER(admissionheight / 100.0, 2) < 40.0 THEN 'obese_class2'
    ELSE 'obese_class3'
END as bmi_category,


-- ----------------------------------------------------------------------------
-- 2. Total GCS Score (Glasgow Coma Scale)
-- ----------------------------------------------------------------------------
-- Sum of eyes (1-4) + verbal (1-5) + motor (1-6) = total (3-15)
-- Lower scores = worse neurological status
-- Available for 85.5% of records (170,602 patients)
-- Note: Excludes -1.0 values which should be converted to NULL first
--
CASE
    WHEN apache_gcs_eyes IS NOT NULL
     AND apache_gcs_verbal IS NOT NULL
     AND apache_gcs_motor IS NOT NULL
     AND apache_gcs_eyes > 0    -- Exclude -1.0 if not already converted to NULL
     AND apache_gcs_verbal > 0
     AND apache_gcs_motor > 0
    THEN apache_gcs_eyes + apache_gcs_verbal + apache_gcs_motor
    ELSE NULL
END as gcs_total,

-- Optional: GCS severity category
CASE
    WHEN apache_gcs_eyes IS NULL OR apache_gcs_verbal IS NULL OR apache_gcs_motor IS NULL THEN NULL
    WHEN apache_gcs_eyes <= 0 OR apache_gcs_verbal <= 0 OR apache_gcs_motor <= 0 THEN NULL
    WHEN (apache_gcs_eyes + apache_gcs_verbal + apache_gcs_motor) <= 8 THEN 'severe'
    WHEN (apache_gcs_eyes + apache_gcs_verbal + apache_gcs_motor) <= 12 THEN 'moderate'
    ELSE 'mild'
END as gcs_severity,


-- ----------------------------------------------------------------------------
-- 3. Vital Sign Ranges (24-hour variability indicators)
-- ----------------------------------------------------------------------------
-- Higher variability may indicate instability
-- Available for: HR (95.8%), RR (88.3%), SaO2 (94.4%)
--

-- Heart Rate Range
CASE
    WHEN max_hr_24h IS NOT NULL AND min_hr_24h IS NOT NULL
    THEN max_hr_24h - min_hr_24h
    ELSE NULL
END as hr_range_24h,

-- Respiratory Rate Range
CASE
    WHEN max_rr_24h IS NOT NULL AND min_rr_24h IS NOT NULL
    THEN max_rr_24h - min_rr_24h
    ELSE NULL
END as rr_range_24h,

-- Oxygen Saturation Range
CASE
    WHEN max_sao2_24h IS NOT NULL AND min_sao2_24h IS NOT NULL
    THEN max_sao2_24h - min_sao2_24h
    ELSE NULL
END as sao2_range_24h,


-- ----------------------------------------------------------------------------
-- 4. Age Groups (categorical)
-- ----------------------------------------------------------------------------
-- Clinical age categories for ICU patients
--
CASE
    WHEN age_numeric IS NULL THEN NULL
    WHEN age_numeric < 18 THEN 'pediatric'      -- Should be rare in adult ICU
    WHEN age_numeric < 45 THEN 'young_adult'
    WHEN age_numeric < 65 THEN 'middle_age'
    WHEN age_numeric < 80 THEN 'elderly'
    ELSE 'very_elderly'                          -- >= 80
END as age_group,


-- ----------------------------------------------------------------------------
-- 5. Emergency Admission Flag
-- ----------------------------------------------------------------------------
-- Indicates if patient was admitted through emergency department
-- Useful as emergency admissions may have different characteristics
--
CASE
    WHEN LOWER(hospitaladmitsource) LIKE '%emergency%' THEN 1
    ELSE 0
END as is_emergency_admission,


-- ----------------------------------------------------------------------------
-- 6. ICU Readmission Flag (already exists as apache_readmit)
-- ----------------------------------------------------------------------------
-- Note: apache_readmit already captures this
-- No additional feature needed


-- ----------------------------------------------------------------------------
-- 7. Any Pressor Use (24h)
-- ----------------------------------------------------------------------------
-- Combines all pressor types into single indicator
-- Useful alternative to having separate pressor flags
--
CASE
    WHEN pressor_norepi_24h = 1 OR pressor_epi_24h = 1 OR pressor_vaso_24h = 1
    THEN 1
    ELSE 0
END as any_pressor_24h,


-- ----------------------------------------------------------------------------
-- 8. Critical Vital Signs Flags
-- ----------------------------------------------------------------------------
-- Binary indicators for critically abnormal values in first 24h
--

-- Critically low heart rate (bradycardia)
CASE
    WHEN min_hr_24h IS NOT NULL AND min_hr_24h < 40 THEN 1
    ELSE 0
END as had_bradycardia_24h,

-- Critically high heart rate (tachycardia)
CASE
    WHEN max_hr_24h IS NOT NULL AND max_hr_24h > 130 THEN 1
    ELSE 0
END as had_tachycardia_24h,

-- Critically low oxygen saturation (hypoxemia)
CASE
    WHEN min_sao2_24h IS NOT NULL AND min_sao2_24h < 90 THEN 1
    ELSE 0
END as had_hypoxemia_24h,


-- ----------------------------------------------------------------------------
-- 9. Creatinine Change (if both APACHE and 24h available)
-- ----------------------------------------------------------------------------
-- Indicates acute kidney injury if creatinine increased
--
CASE
    WHEN apache_creatinine IS NOT NULL
     AND creatinine_mean_24h IS NOT NULL
     AND apache_creatinine > 0  -- Exclude -1.0 if not already NULL
    THEN creatinine_mean_24h - apache_creatinine
    ELSE NULL
END as creatinine_change_24h,

-- Acute Kidney Injury flag (>50% increase in creatinine)
CASE
    WHEN apache_creatinine IS NOT NULL
     AND creatinine_mean_24h IS NOT NULL
     AND apache_creatinine > 0
     AND (creatinine_mean_24h - apache_creatinine) / apache_creatinine > 0.5
    THEN 1
    ELSE 0
END as has_aki_24h


-- ============================================================================
-- USAGE INSTRUCTIONS FOR JIM:
-- ============================================================================
--
-- 1. Add these features to the SELECT clause in 10_v_features_icu_stay_clean.sql
-- 2. Place them after the existing feature blocks (after infusion features)
-- 3. Ensure APACHE -1.0 values are already converted to NULL using NULLIF()
-- 4. Add a comment block indicating "Engineered Features" section
--
-- Example placement in view:
--
--     -- Infusion features
--     i.pressor_norepi_24h,
--     i.pressor_epi_24h,
--     i.pressor_vaso_24h,
--     i.sedative_propofol_24h,
--
--     -- Engineered Features
--     CASE WHEN admissionheight IS NOT NULL ... END as bmi,
--     ... (rest of engineered features)
--
-- ============================================================================
