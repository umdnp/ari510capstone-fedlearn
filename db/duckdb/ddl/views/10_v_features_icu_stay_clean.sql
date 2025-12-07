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

    -- derived age group (categorical)
    case 
        when age = '> 89' or age = '>89' then 'elderly'
        else case 
            when try_cast(age as integer) < 40 then 'young'
            when try_cast(age as integer) < 60 then 'middle'
            when try_cast(age as integer) < 80 then 'older'
            else 'elderly'
        end
    end as age_group,

    -- patient-level
    coalesce(lower(trim(gender)), 'unknown') as gender,
    ethnicity,
    admissionheight,
    admissionweight,
    case 
        when admissionheight is not null 
             and admissionweight is not null 
             and admissionheight > 0
        then admissionweight / power(admissionheight / 100.0, 2)
        else null
    end as bmi,
    unittype,
    unitadmitsource,
    unitvisitnumber,
    hospitaladmitsource,
    case 
        when lower(coalesce(unitadmitsource, '')) like '%emergency%'
          or lower(coalesce(hospitaladmitsource, '')) like '%emergency%'
        then 1
        else 0
    end as emergency_admit,
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
    apache_hct,
    apache_creatinine,
    apache_albumin,
    apache_bun,
    apache_glucose,
    apache_bilirubin,
    apache_gcs_eyes,
    apache_gcs_verbal,
    apache_gcs_motor,
    apache_gcs_eyes + apache_gcs_verbal + apache_gcs_motor as apache_gcs_total,

    -- APACHE missingness flags
    case when apache_gcs_eyes      is null then 1 else 0 end as is_missing_gcs_eyes,
    case when apache_gcs_verbal    is null then 1 else 0 end as is_missing_gcs_verbal,
    case when apache_gcs_motor     is null then 1 else 0 end as is_missing_gcs_motor,
    case when apache_albumin       is null then 1 else 0 end as apache_albumin_missing,
    case when apache_bilirubin     is null then 1 else 0 end as apache_bilirubin_missing,
    case when apache_urine_24h     is null then 1 else 0 end as apache_urine_24h_missing,
    case when apache_wbc           is null then 1 else 0 end as apache_wbc_missing,
    case when apache_temp          is null then 1 else 0 end as apache_temp_missing,
    case when apache_sodium        is null then 1 else 0 end as apache_sodium_missing,
    case when apache_creatinine    is null then 1 else 0 end as apache_creatinine_missing,
    case when apache_hct           is null then 1 else 0 end as apache_hct_missing,
    case when apache_bun           is null then 1 else 0 end as apache_bun_missing,
    case when apache_glucose       is null then 1 else 0 end as apache_glucose_missing,

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

    -- APACHE predictor missingness flags
    case when apache_bedcount         is null then 1 else 0 end as apache_bedcount_missing,
    case when apache_admitsource_code is null then 1 else 0 end as apache_admitsource_code_missing,

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

    -- Vitals ranges
    max_hr_24h - min_hr_24h       as hr_range_24h,
    max_rr_24h - min_rr_24h       as rr_range_24h,
    max_sao2_24h - min_sao2_24h   as sao2_range_24h,

    -- Critical vital sign flags
    case
        when min_hr_24h is not null and min_hr_24h < 40 then 1
        else 0
    end as had_bradycardia_24h,
    case
        when max_hr_24h is not null and max_hr_24h > 130 then 1
        else 0
    end as had_tachycardia_24h,
    case
        when min_sao2_24h is not null and min_sao2_24h < 90 then 1
        else 0
    end as had_hypoxemia_24h,

    -- Labs 24h
    creatinine_mean_24h,
    creatinine_max_24h,
    wbc_mean_24h,
    glucose_mean_24h,

    -- Renal function change
    case
        when apache_creatinine   is not null
         and creatinine_mean_24h is not null
        then creatinine_mean_24h - apache_creatinine
        else null
    end as creatinine_change_24h,
    case
        when apache_creatinine   is not null
         and creatinine_mean_24h is not null
         and apache_creatinine > 0
         and (creatinine_mean_24h - apache_creatinine) / apache_creatinine > 0.5
        then 1
        else 0
    end as has_aki_24h,

    -- Resp features
    vent_started_24h,

    -- Infusion features
    pressor_norepi_24h,
    pressor_epi_24h,
    pressor_vaso_24h,
    sedative_propofol_24h,
    case
        when pressor_norepi_24h = 1
          or pressor_epi_24h   = 1
          or pressor_vaso_24h  = 1
        then 1
        else 0
    end as any_pressor_24h,

    -- Resp / infusion missingness flags
    case when vent_started_24h       is null then 1 else 0 end as vent_started_24h_missing,
    case when apache_electivesurgery is null then 1 else 0 end as apache_electivesurgery_missing,
    case when pressor_norepi_24h     is null then 1 else 0 end as pressor_norepi_24h_missing,
    case when pressor_epi_24h        is null then 1 else 0 end as pressor_epi_24h_missing,
    case when pressor_vaso_24h       is null then 1 else 0 end as pressor_vaso_24h_missing,
    case when sedative_propofol_24h  is null then 1 else 0 end as sedative_propofol_24h_missing

from v_features_icu_stay;
