-- Clean, modeling-ready version of v_features_icu_stay

create or replace view v_features_icu_stay_clean as
select
    -- identifiers / labels
    patientunitstayid,
    los_days,
    prolonged_stay,

    -- derived age (numeric)
    case 
        when age = '> 89' or age = '>89' then 90
        else try_cast(age as integer)
    end as age_numeric,

    -- patient-level
    coalesce(lower(trim(gender)), 'unknown') as gender,
    ethnicity,
    admissionheight,
    admissionweight,
    unittype,
    unitadmitsource,
    unitvisitnumber,
    hospitaladmitsource,
    apacheadmissiondx,
    admissiondx_category,
    numbedscategory,
    teachingstatus,
    hospital_region,

    -- APACHE APS
    apache_intubated,
    apache_vent,
    apache_dialysis,
    apache_urine_24h,
    apache_wbc,
    apache_temp,
    apache_rr,
    apache_sodium,
    apache_hr,
    apache_meanbp,
    apache_ph,
    apache_hct,
    apache_creatinine,
    apache_albumin,
    apache_pao2,
    apache_pco2,
    apache_bun,
    apache_glucose,
    apache_bilirubin,
    apache_gcs_eyes,
    apache_gcs_verbal,
    apache_gcs_motor,
    apache_fio2,

    -- GCS missingness flags (for modeling)
    case when apache_gcs_eyes   is null then 1 else 0 end as is_missing_gcs_eyes,
    case when apache_gcs_verbal is null then 1 else 0 end as is_missing_gcs_verbal,
    case when apache_gcs_motor  is null then 1 else 0 end as is_missing_gcs_motor,

    -- APACHE predictors
    apache_bedcount,
    apache_admitsource_code,
    apache_diabetes,
    apache_aids,
    apache_hepaticfailure,
    apache_lymphoma,
    apache_metastaticcancer,
    apache_leukemia,
    apache_immunosuppression,
    apache_cirrhosis,
    apache_electivesurgery,
    apache_readmit,
    apache_ventday1,
    apache_oobventday1,
    apache_oobintubday1,

    -- Vitals 24h
    avg_hr_24h,
    min_hr_24h,
    max_hr_24h,
    avg_rr_24h,
    min_rr_24h,
    max_rr_24h,
    avg_sao2_24h,
    min_sao2_24h,
    max_sao2_24h,

    -- Labs 24h
    creatinine_mean_24h,
    creatinine_max_24h,
    wbc_mean_24h,
    glucose_mean_24h,

    -- Resp features
    vent_started_24h,
    ever_vented,

    -- Infusion features
    pressor_norepi_24h,
    pressor_epi_24h,
    pressor_vaso_24h,
    sedative_propofol_24h

from v_features_icu_stay;
