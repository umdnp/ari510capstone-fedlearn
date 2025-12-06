-- Summary statistics of vitalperiodic in the first 24h

create or replace view v_features_vitals_24h as
with vitals_24h as (
    select
        patientunitstayid,
        observationoffset,
        heartrate,
        sao2,
        respiration,
        systemicsystolic,
        systemicdiastolic,
        systemicmean,
        temperature
    from vitalperiodic
    where observationoffset between 0 and 24 * 60
)
select
    patientunitstayid,

    -- Heart rate
    avg(heartrate)     as avg_hr_24h,
    min(heartrate)     as min_hr_24h,
    max(heartrate)     as max_hr_24h,

    -- Respiratory rate
    avg(respiration)   as avg_rr_24h,
    min(respiration)   as min_rr_24h,
    max(respiration)   as max_rr_24h,

    -- Oxygen saturation
    avg(sao2)          as avg_sao2_24h,
    min(sao2)          as min_sao2_24h,
    max(sao2)          as max_sao2_24h
from vitals_24h
group by patientunitstayid;
