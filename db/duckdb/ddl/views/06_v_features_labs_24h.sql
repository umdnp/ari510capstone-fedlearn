-- Example lab summaries in the first 24h

create or replace view v_features_labs_24h as
with labs_24h as (
    select
        patientunitstayid,
        lower(labname) as labname,
        labresultoffset,
        labresult
    from lab
    where labresultoffset between 0 and 24 * 60
      and labresult is not null
)
select
    patientunitstayid,

    -- Creatinine
    avg(case when labname like '%creatinine%' then labresult end) as creatinine_mean_24h,
    max(case when labname like '%creatinine%' then labresult end) as creatinine_max_24h,

    -- WBC
    avg(case 
            when labname like '%wbc%' 
              or labname like '%white blood%' 
         then labresult end) as wbc_mean_24h,

    -- Glucose
    avg(case when labname like '%glucose%' then labresult end) as glucose_mean_24h,

    -- Bilirubin
    avg(case when labname like '%bilirubin%' then labresult end) as bilirubin_mean_24h

from labs_24h
group by patientunitstayid;
