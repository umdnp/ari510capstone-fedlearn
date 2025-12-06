-- Creates the binary target "prolonged_stay" based on ICU LOS > 3 days

create or replace view v_features_target as
select
    patientunitstayid,
    unitdischargeoffset / (60.0 * 24) as los_days,
    case
        when unitdischargeoffset / (60.0 * 24) > 3 then 1
        else 0
    end as prolonged_stay
from patient
where unitdischargeoffset is not null
  and unitdischargeoffset > 0;
