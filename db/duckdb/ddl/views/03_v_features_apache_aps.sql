-- Aggregated APACHE APS variables (worst case values per stay)

create or replace view v_features_apache_aps as
select
    patientunitstayid,
    max(intubated)      as apache_intubated,
    max(vent)           as apache_vent,
    max(dialysis)       as apache_dialysis,
    avg(urine)          as apache_urine_24h,
    avg(wbc)            as apache_wbc,
    avg(temperature)    as apache_temp,
    avg(respiratoryrate) as apache_rr,
    avg(sodium)         as apache_sodium,
    avg(heartrate)      as apache_hr,
    avg(meanbp)         as apache_meanbp,
    avg(ph)             as apache_ph,
    avg(hematocrit)     as apache_hct,
    avg(creatinine)     as apache_creatinine,
    avg(albumin)        as apache_albumin,
    avg(pao2)           as apache_pao2,
    avg(pco2)           as apache_pco2,
    avg(bun)            as apache_bun,
    avg(glucose)        as apache_glucose,
    avg(bilirubin)      as apache_bilirubin,
    avg(fio2)           as apache_fio2
from apacheapsvar
group by patientunitstayid;
