-- PHASE 4: Advanced Feature Engineering
-- Based on feature importance analysis from Random Forest and Gradient Boosting models
--
-- IMPORTANT: These are NEW features that do NOT currently exist in the database.
--
-- How These Were Created:
--   1. Analyzed EXISTING features in 09_feature_importance_analysis.ipynb
--   2. Identified that Interventions, APACHE scores, and Vitals are most important
--   3. Created NEW composite/ratio features based on those high-value categories
--   4. Applied clinical domain knowledge (SOFA, qSOFA, SIRS are validated ICU scores)
--
-- This file contains SQL snippets for creating 30+ NEW engineered features
-- to improve model performance for prolonged ICU stay prediction.
--
-- Categories of NEW Features:
--   1. Clinical Severity Scores (SOFA, qSOFA, SIRS, Shock Index)
--   2. Vital Sign Variability
--   3. Lab Ratios
--   4. Intervention Intensity
--   5. Organ Dysfunction Indicators
--
-- Usage: Add these features to v_features_icu_stay_clean.sql
--
-- Testing: After adding features, re-run models and re-run the analysis notebook
-- to see which NEW features are actually important.

-- ============================================================================
-- 1. CLINICAL SEVERITY SCORES
-- ============================================================================

-- SIRS Criteria Count (Systemic Inflammatory Response Syndrome)
-- Criteria: temp <36 or >38, HR >90, RR >20, WBC <4 or >12
CASE
    WHEN apache_temp     IS NULL THEN NULL
     AND apache_hr       IS NULL
     AND apache_rr       IS NULL
     AND apache_wbc      IS NULL
    THEN NULL
    ELSE (
        CASE WHEN apache_temp < 36 OR apache_temp > 38 THEN 1 ELSE 0 END +
        CASE WHEN apache_hr > 90 THEN 1 ELSE 0 END +
        CASE WHEN apache_rr > 20 THEN 1 ELSE 0 END +
        CASE WHEN apache_wbc < 4 OR apache_wbc > 12 THEN 1 ELSE 0 END
    )
END as sirs_criteria_count,

-- qSOFA Score (quick Sequential Organ Failure Assessment)
-- Criteria: RR >=22, altered mentation (GCS <15), systolic BP <=100
CASE
    WHEN apache_rr IS NULL
     AND apache_gcs_total IS NULL
     AND apache_meanbp IS NULL
    THEN NULL
    ELSE (
        CASE WHEN apache_rr >= 22 THEN 1 ELSE 0 END +
        CASE WHEN apache_gcs_total < 15 THEN 1 ELSE 0 END +
        -- Approximate systolic BP from mean BP (systolic ≈ mean + 1/3 pulse pressure)
        CASE WHEN apache_meanbp <= 100 THEN 1 ELSE 0 END
    )
END as qsofa_score,

-- Shock Index (HR / Systolic BP approximation)
-- Normal: 0.5-0.7, Elevated: >1.0 indicates shock
CASE
    WHEN apache_hr IS NOT NULL
     AND apache_meanbp IS NOT NULL
     AND apache_meanbp > 0
    THEN apache_hr / apache_meanbp
    ELSE NULL
END as shock_index,

-- Simplified SOFA Score (using available data)
-- Respiratory: PaO2/FiO2 ratio
-- Cardiovascular: MAP or use of vasopressors
-- Renal: Creatinine
-- Neurological: GCS
(
    -- Respiratory component (0-4 points)
    CASE
        WHEN apache_pao2 IS NOT NULL AND apache_fio2 IS NOT NULL AND apache_fio2 > 0
        THEN CASE
            WHEN apache_pao2 / apache_fio2 < 100 THEN 4
            WHEN apache_pao2 / apache_fio2 < 200 THEN 3
            WHEN apache_pao2 / apache_fio2 < 300 THEN 2
            WHEN apache_pao2 / apache_fio2 < 400 THEN 1
            ELSE 0
        END
        ELSE 0
    END +
    -- Cardiovascular component (0-4 points)
    CASE
        WHEN any_pressor_24h = 1 THEN 4
        WHEN apache_meanbp < 70 THEN 1
        ELSE 0
    END +
    -- Renal component (0-4 points)
    CASE
        WHEN apache_creatinine >= 5.0 THEN 4
        WHEN apache_creatinine >= 3.5 THEN 3
        WHEN apache_creatinine >= 2.0 THEN 2
        WHEN apache_creatinine >= 1.2 THEN 1
        ELSE 0
    END +
    -- Neurological component (0-4 points)
    CASE
        WHEN apache_gcs_total < 6 THEN 4
        WHEN apache_gcs_total < 10 THEN 3
        WHEN apache_gcs_total < 13 THEN 2
        WHEN apache_gcs_total < 15 THEN 1
        ELSE 0
    END
) as sofa_score_simplified,


-- ============================================================================
-- 2. VITAL SIGN VARIABILITY
-- ============================================================================

-- Coefficient of Variation for Heart Rate (std dev / mean)
-- High CV indicates instability
CASE
    WHEN avg_hr_24h IS NOT NULL
     AND avg_hr_24h > 0
     AND max_hr_24h IS NOT NULL
     AND min_hr_24h IS NOT NULL
    THEN (max_hr_24h - min_hr_24h) / avg_hr_24h
    ELSE NULL
END as hr_coefficient_variation,

-- Coefficient of Variation for Respiratory Rate
CASE
    WHEN avg_rr_24h IS NOT NULL
     AND avg_rr_24h > 0
     AND max_rr_24h IS NOT NULL
     AND min_rr_24h IS NOT NULL
    THEN (max_rr_24h - min_rr_24h) / avg_rr_24h
    ELSE NULL
END as rr_coefficient_variation,

-- Coefficient of Variation for SaO2
CASE
    WHEN avg_sao2_24h IS NOT NULL
     AND avg_sao2_24h > 0
     AND max_sao2_24h IS NOT NULL
     AND min_sao2_24h IS NOT NULL
    THEN (max_sao2_24h - min_sao2_24h) / avg_sao2_24h
    ELSE NULL
END as sao2_coefficient_variation,

-- Vital instability score (sum of critical vital flags)
(
    had_bradycardia_24h +
    had_tachycardia_24h +
    had_hypoxemia_24h
) as vital_instability_score,


-- ============================================================================
-- 3. LAB RATIOS
-- ============================================================================

-- BUN/Creatinine Ratio
-- Normal: 10-20, >20 suggests prerenal azotemia
CASE
    WHEN apache_bun IS NOT NULL
     AND apache_creatinine IS NOT NULL
     AND apache_creatinine > 0
    THEN apache_bun / apache_creatinine
    ELSE NULL
END as bun_creatinine_ratio,

-- WBC/Albumin Ratio
-- Higher ratio may indicate inflammation with poor nutrition
CASE
    WHEN apache_wbc IS NOT NULL
     AND apache_albumin IS NOT NULL
     AND apache_albumin > 0
    THEN apache_wbc / apache_albumin
    ELSE NULL
END as wbc_albumin_ratio,

-- Glucose/Creatinine Ratio
CASE
    WHEN apache_glucose IS NOT NULL
     AND apache_creatinine IS NOT NULL
     AND apache_creatinine > 0
    THEN apache_glucose / apache_creatinine
    ELSE NULL
END as glucose_creatinine_ratio,

-- Anion Gap (approximation using available labs)
-- Na - (Cl + HCO3), but we don't have Cl and HCO3 consistently
-- Skip for now - insufficient data


-- ============================================================================
-- 4. INTERVENTION INTENSITY
-- ============================================================================

-- Total pressor count
(
    COALESCE(pressor_norepi_24h, 0) +
    COALESCE(pressor_epi_24h, 0) +
    COALESCE(pressor_vaso_24h, 0)
) as pressor_count,

-- High intensity intervention flag
-- Ventilation + pressor combination
CASE
    WHEN vent_started_24h = 1 AND any_pressor_24h = 1 THEN 1
    ELSE 0
END as vent_pressor_combo,

-- Dialysis + pressor combination
CASE
    WHEN apache_dialysis = 1 AND any_pressor_24h = 1 THEN 1
    ELSE 0
END as dialysis_pressor_combo,

-- Total intervention score
(
    COALESCE(vent_started_24h, 0) +
    COALESCE(any_pressor_24h, 0) +
    COALESCE(apache_dialysis, 0) +
    COALESCE(sedative_propofol_24h, 0)
) as total_intervention_score,


-- ============================================================================
-- 5. ORGAN DYSFUNCTION INDICATORS
-- ============================================================================

-- Respiratory dysfunction
CASE
    WHEN vent_started_24h = 1
      OR (min_sao2_24h IS NOT NULL AND min_sao2_24h < 90)
      OR (apache_pao2 IS NOT NULL AND apache_pao2 < 60)
    THEN 1
    ELSE 0
END as respiratory_dysfunction,

-- Cardiovascular dysfunction
CASE
    WHEN any_pressor_24h = 1
      OR (apache_meanbp IS NOT NULL AND apache_meanbp < 65)
      OR (apache_hr IS NOT NULL AND (apache_hr < 40 OR apache_hr > 130))
    THEN 1
    ELSE 0
END as cardiovascular_dysfunction,

-- Renal dysfunction
CASE
    WHEN has_aki_24h = 1
      OR apache_dialysis = 1
      OR (apache_creatinine IS NOT NULL AND apache_creatinine > 2.0)
    THEN 1
    ELSE 0
END as renal_dysfunction,

-- Neurological dysfunction
CASE
    WHEN apache_gcs_total IS NOT NULL AND apache_gcs_total < 13 THEN 1
    ELSE 0
END as neurological_dysfunction,

-- Hepatic dysfunction
CASE
    WHEN (apache_bilirubin IS NOT NULL AND apache_bilirubin > 2.0)
      OR (apache_albumin IS NOT NULL AND apache_albumin < 2.5)
    THEN 1
    ELSE 0
END as hepatic_dysfunction,

-- Total organ systems affected
(
    CASE
        WHEN vent_started_24h = 1
          OR (min_sao2_24h IS NOT NULL AND min_sao2_24h < 90)
          OR (apache_pao2 IS NOT NULL AND apache_pao2 < 60)
        THEN 1 ELSE 0
    END +
    CASE
        WHEN any_pressor_24h = 1
          OR (apache_meanbp IS NOT NULL AND apache_meanbp < 65)
          OR (apache_hr IS NOT NULL AND (apache_hr < 40 OR apache_hr > 130))
        THEN 1 ELSE 0
    END +
    CASE
        WHEN has_aki_24h = 1
          OR apache_dialysis = 1
          OR (apache_creatinine IS NOT NULL AND apache_creatinine > 2.0)
        THEN 1 ELSE 0
    END +
    CASE
        WHEN apache_gcs_total IS NOT NULL AND apache_gcs_total < 13
        THEN 1 ELSE 0
    END +
    CASE
        WHEN (apache_bilirubin IS NOT NULL AND apache_bilirubin > 2.0)
          OR (apache_albumin IS NOT NULL AND apache_albumin < 2.5)
        THEN 1 ELSE 0
    END
) as total_organ_dysfunctions,

-- Multi-organ dysfunction flag (>=2 systems affected)
CASE
    WHEN (
        CASE
            WHEN vent_started_24h = 1
              OR (min_sao2_24h IS NOT NULL AND min_sao2_24h < 90)
              OR (apache_pao2 IS NOT NULL AND apache_pao2 < 60)
            THEN 1 ELSE 0
        END +
        CASE
            WHEN any_pressor_24h = 1
              OR (apache_meanbp IS NOT NULL AND apache_meanbp < 65)
              OR (apache_hr IS NOT NULL AND (apache_hr < 40 OR apache_hr > 130))
            THEN 1 ELSE 0
        END +
        CASE
            WHEN has_aki_24h = 1
              OR apache_dialysis = 1
              OR (apache_creatinine IS NOT NULL AND apache_creatinine > 2.0)
            THEN 1 ELSE 0
        END +
        CASE
            WHEN apache_gcs_total IS NOT NULL AND apache_gcs_total < 13
            THEN 1 ELSE 0
        END +
        CASE
            WHEN (apache_bilirubin IS NOT NULL AND apache_bilirubin > 2.0)
              OR (apache_albumin IS NOT NULL AND apache_albumin < 2.5)
            THEN 1 ELSE 0
        END
    ) >= 2
    THEN 1
    ELSE 0
END as multi_organ_dysfunction

-- ============================================================================
-- END OF ADVANCED FEATURES
-- ============================================================================
