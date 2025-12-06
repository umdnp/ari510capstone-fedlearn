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
    case
        when lower(p.apacheadmissiondx) like '%sepsis%' then 'sepsis'
        when lower(p.apacheadmissiondx) like '%pneumonia%' then 'respiratory'
        when lower(p.apacheadmissiondx) like '%respiratory%' then 'respiratory'
        when lower(p.apacheadmissiondx) like '%ards%' then 'respiratory'
        when lower(p.apacheadmissiondx) like '%copd%' then 'respiratory'
        when lower(p.apacheadmissiondx) like '%asthma%' then 'respiratory'
        when lower(p.apacheadmissiondx) like '%stroke%' then 'neurologic'
        when lower(p.apacheadmissiondx) like '%intracran%' then 'neurologic'
        when lower(p.apacheadmissiondx) like '%subarach%' then 'neurologic'
        when lower(p.apacheadmissiondx) like '%seizure%' then 'neurologic'
        when lower(p.apacheadmissiondx) like '%coma%' then 'neurologic'
        when lower(p.apacheadmissiondx) like '%myocardial%' then 'cardiac'
        when lower(p.apacheadmissiondx) like '%acute coronary%' then 'cardiac'
        when lower(p.apacheadmissiondx) like '%heart failure%' then 'cardiac'
        when lower(p.apacheadmissiondx) like '%cardiogenic%' then 'cardiac'
        when lower(p.apacheadmissiondx) like '%arrhythm' then 'cardiac'
        when lower(p.apacheadmissiondx) like '%trauma%' then 'trauma'
        when lower(p.apacheadmissiondx) like '%fracture%' then 'trauma'
        when lower(p.apacheadmissiondx) like '%stab%' then 'trauma'
        when lower(p.apacheadmissiondx) like '%gunshot%' then 'trauma'
        when lower(p.apacheadmissiondx) like '%liver%' then 'hepatic'
        when lower(p.apacheadmissiondx) like '%cirrhosis%' then 'hepatic'
        when lower(p.apacheadmissiondx) like '%hepatic%' then 'hepatic'
        else 'other'
    end as admissiondx_category,
    h.numbedscategory,
    h.teachingstatus,
    h.region as hospital_region
from patient p
left join hospital h
    on p.hospitalid = h.hospitalid
where p.unitdischargeoffset is not null
  and p.unitdischargeoffset > 0;
