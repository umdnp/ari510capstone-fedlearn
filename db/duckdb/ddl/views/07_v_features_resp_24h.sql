-- Ventilation-related indicators

create or replace view v_features_resp_24h as
select
    patientunitstayid,
    case 
        when count(*) filter (
            where ventstartoffset between 0 and 24 * 60
        ) > 0 then 1 else 0
    end as vent_started_24h,
    case 
        when count(*) filter (
            where ventstartoffset is not null
        ) > 0 then 1 else 0
    end as ever_vented
from respiratorycare
group by patientunitstayid;
