-- One row per ICU stay, with target + all feature blocks

create or replace view v_features_icu_stay as
select
    t.patientunitstayid,
    t.los_days,
    t.prolonged_stay,

    -- patient-level
    p.age,
    p.gender,
    p.ethnicity,
    p.admissionheight,
    p.admissionweight,
    p.unittype,
    p.unitadmitsource,
    p.unitvisitnumber,
    p.hospitaladmitsource,
    p.apacheadmissiondx,
    p.numbedscategory,
    p.teachingstatus,
    p.hospital_region,

    -- APACHE APS
    a_aps.apache_intubated,
    a_aps.apache_vent,
    a_aps.apache_dialysis,
    a_aps.apache_urine_24h,
    a_aps.apache_wbc,
    a_aps.apache_temp,
    a_aps.apache_rr,
    a_aps.apache_sodium,
    a_aps.apache_hr,
    a_aps.apache_meanbp,
    a_aps.apache_ph,
    a_aps.apache_hct,
    a_aps.apache_creatinine,
    a_aps.apache_albumin,
    a_aps.apache_pao2,
    a_aps.apache_pco2,
    a_aps.apache_bun,
    a_aps.apache_glucose,
    a_aps.apache_bilirubin,
    a_aps.apache_fio2,

    -- APACHE predictors
    a_pred.apache_gender_code,
    a_pred.apache_age_years,
    a_pred.apache_teachtype,
    a_pred.apache_region_code,
    a_pred.apache_bedcount,
    a_pred.apache_admitsource_code,
    a_pred.apache_diabetes,
    a_pred.apache_aids,
    a_pred.apache_hepaticfailure,
    a_pred.apache_lymphoma,
    a_pred.apache_metastaticcancer,
    a_pred.apache_leukemia,
    a_pred.apache_immunosuppression,
    a_pred.apache_cirrhosis,
    a_pred.apache_electivesurgery,
    a_pred.apache_readmit,
    a_pred.apache_ventday1,
    a_pred.apache_oobventday1,
    a_pred.apache_oobintubday1,

    -- Vitals 24h
    v.avg_hr_24h,
    v.min_hr_24h,
    v.max_hr_24h,
    v.avg_rr_24h,
    v.min_rr_24h,
    v.max_rr_24h,
    v.avg_sao2_24h,
    v.min_sao2_24h,
    v.max_sao2_24h,
    v.avg_sysbp_24h,
    v.avg_diabp_24h,
    v.avg_meanbp_24h,
    v.avg_temp_24h,

    -- Labs 24h
    l.creatinine_mean_24h,
    l.creatinine_max_24h,
    l.wbc_mean_24h,
    l.glucose_mean_24h,
    l.bilirubin_mean_24h,

    -- Resp features
    r.vent_started_24h,
    r.ever_vented,

    -- Infusion features
    i.pressor_norepi_24h,
    i.pressor_epi_24h,
    i.pressor_vaso_24h,
    i.sedative_propofol_24h

from v_features_target t
left join v_features_patient p
    on t.patientunitstayid = p.patientunitstayid
left join v_features_apache_aps a_aps
    on t.patientunitstayid = a_aps.patientunitstayid
left join v_features_apache_pred a_pred
    on t.patientunitstayid = a_pred.patientunitstayid
left join v_features_vitals_24h v
    on t.patientunitstayid = v.patientunitstayid
left join v_features_labs_24h l
    on t.patientunitstayid = l.patientunitstayid
left join v_features_resp_24h r
    on t.patientunitstayid = r.patientunitstayid
left join v_features_infusions_24h i
    on t.patientunitstayid = i.patientunitstayid;
