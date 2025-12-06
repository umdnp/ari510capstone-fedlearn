-- basic demographics and admission context + hospital characteristics

create or replace view v_features_patient as
select
    p.patientunitstayid,
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
    h.numbedscategory,
    h.teachingstatus,
    h.region as hospital_region
from patient p
left join hospital h
    on p.hospitalid = h.hospitalid
where p.unitdischargeoffset is not null
  and p.unitdischargeoffset > 0;
