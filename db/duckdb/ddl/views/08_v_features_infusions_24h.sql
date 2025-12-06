-- pressor / sedative indicators in first 24h (template)

create or replace view v_features_infusions_24h as
with inf_24h as (
    select
        patientunitstayid,
        lower(drugname) as drugname,
        infusionoffset
    from infusiondrug
    where infusionoffset between 0 and 24 * 60
)
select
    patientunitstayid,

    max(case 
            when drugname like '%norepinephrine%' 
              or drugname like '%levophed%' 
         then 1 else 0 end) as pressor_norepi_24h,

    max(case 
            when drugname like '%epinephrine%' 
         then 1 else 0 end) as pressor_epi_24h,

    max(case 
            when drugname like '%vasopressin%' 
         then 1 else 0 end) as pressor_vaso_24h,

    max(case 
            when drugname like '%propofol%' 
         then 1 else 0 end) as sedative_propofol_24h

from inf_24h
group by patientunitstayid;
