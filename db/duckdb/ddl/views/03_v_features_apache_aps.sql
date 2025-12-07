-- Aggregated APACHE APS variables (worst case values per stay)

create or replace view v_features_apache_aps as
select
    patientunitstayid,
    max(intubated)      as apache_intubated,
    max(vent)           as apache_vent,
    max(dialysis)       as apache_dialysis,
    avg(nullif(urine, -1))          as apache_urine_24h,
    avg(nullif(wbc, -1))            as apache_wbc,
    avg(nullif(temperature, -1))    as apache_temp,
    avg(nullif(respiratoryrate, -1)) as apache_rr,
    avg(nullif(sodium, -1))         as apache_sodium,
    avg(nullif(heartrate, -1))      as apache_hr,
    avg(nullif(meanbp, -1))         as apache_meanbp,
    avg(nullif(ph, -1))             as apache_ph,
    avg(nullif(hematocrit, -1))     as apache_hct,
    avg(nullif(creatinine, -1))     as apache_creatinine,
    avg(nullif(albumin, -1))        as apache_albumin,
    avg(nullif(pao2, -1))           as apache_pao2,
    avg(nullif(pco2, -1))           as apache_pco2,
    avg(nullif(bun, -1))            as apache_bun,
    avg(nullif(glucose, -1))        as apache_glucose,
    avg(nullif(bilirubin, -1))      as apache_bilirubin,
    avg(nullif(eyes, -1))           as apache_gcs_eyes,
    avg(nullif(verbal, -1))         as apache_gcs_verbal,
    avg(nullif(motor, -1))          as apache_gcs_motor,
    avg(nullif(fio2, -1))           as apache_fio2
from apacheapsvar
group by patientunitstayid;
