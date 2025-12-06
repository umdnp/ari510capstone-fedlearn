-- APACHE comorbidities and predictor variables

create or replace view v_features_apache_pred as
select
    patientunitstayid,
    max(bedcount)            as apache_bedcount,
    max(admitsource)         as apache_admitsource_code,
    max(diabetes)            as apache_diabetes,
    max(aids)                as apache_aids,
    max(hepaticfailure)      as apache_hepaticfailure,
    max(lymphoma)            as apache_lymphoma,
    max(metastaticcancer)    as apache_metastaticcancer,
    max(leukemia)            as apache_leukemia,
    max(immunosuppression)   as apache_immunosuppression,
    max(cirrhosis)           as apache_cirrhosis,
    max(electivesurgery)     as apache_electivesurgery,
    max(readmit)             as apache_readmit,
    max(ventday1)            as apache_ventday1,
    max(oobventday1)         as apache_oobventday1,
    max(oobintubday1)        as apache_oobintubday1
from apachepredvar
group by patientunitstayid;
