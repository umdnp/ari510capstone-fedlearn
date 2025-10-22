# eICU-CRD Data Dictionary (Enriched)

This data dictionary combines schema information with detailed descriptions from eICU-CRD documentation.

## Column Legend

- **Null**: Indicates if the column can contain NULL values
- **Description**: Detailed description of the column's purpose and content
- **Key**: Indicates if the column is a Primary Key (PK) or Foreign Key (FK)

---

### patient

**Description:** Core patient demographics and ICU stay information

**Row Count:** 200,859

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| patientunitstayid | INTEGER | NOT NULL | surrogate key for ICU Stay  PK  C |  |
| patienthealthsystemstayid | INTEGER | NOT NULL | surrogate key for the patient health system stay (hospital stay) | FK |
| gender | VARCHAR | NULL | gender of the patient: Male, Female, Unknown, Other, NULL |  |
| age | VARCHAR | varchar(10) | NULL |  |
| ethnicity | VARCHAR | NULL | picklist ethnicity of the patient: Asian, Caucasian, African American, Native American, Hispanic, Other/Unknown, NULL |  |
| hospitalid | INTEGER | NOT NULL | surrogate key for the hospital associated with the patient unit stay |  |
| wardid | INTEGER | NOT NULL | surrogate key for the ward associated with the patient unit stay |  |
| apacheadmissiondx | VARCHAR | Full path string of admission diagnosis for patients unit stay e.g.: Pulmonary valve surgery, Chest pain, unknown origin, Restrictive lung disease (i.e., Sarcoidosis, pulmonary fibrosis), etc. | S |  |
| admissionheight | DECIMAL(10,2) | decimal(10,2)   NULL | admission height of the patient in cm e.g.: 160.0000, 182.9000, 175.3000, etc. |  |
| hospitaladmittime24 | VARCHAR | time(0) | NOT NULL |  |
| hospitaladmitoffset | INTEGER | int | NOT NULL |  |
| hospitaladmitsource | VARCHAR | varchar(30) | NULL |  |
| hospitaldischargeyear | SMALLINT | NOT NULL | year of the hospital discharge date |  |
| hospitaldischargetime24 | VARCHAR | time(0) | NOT NULL |  |
| hospitaldischargeoffset | INTEGER | int | NOT NULL |  |
| hospitaldischargelocation | VARCHAR | NULL | Structured list of location where the patient was discharged to from the hospital e.g.: Home, Nursing Home, Death, etc. |  |
| hospitaldischargestatus | VARCHAR | varchar(10) | NULL |  |
| unittype | VARCHAR | varchar(50) | NULL |  |
| unitadmittime24 | VARCHAR | time(0) | NOT NULL |  |
| unitadmitsource | VARCHAR | varchar(100) | NULL |  |
| unitvisitnumber | INTEGER | int | NOT NULL |  |
| unitstaytype | VARCHAR | varchar(15) | NULL |  |
| admissionweight | DECIMAL(10,2) | decimal(10,2)   NULL | admission weight of the patient in kilograms e.g.: 69.7000, 70.9000, 173.0000, etc. |  |
| dischargeweight | DECIMAL(10,2) | decimal(10,2)   NULL | patient weight at time of unit discharge in kilograms e.g.: 69.7000, 70.9000, 173.0000, etc. |  |
| unitdischargetime24 | VARCHAR | time(0) | NOT NULL |  |
| unitdischargeoffset | INTEGER | int | NOT NULL |  |
| unitdischargelocation | VARCHAR | NULL | Structured list of locations where the patient was discharged to from the unit e.g.: Other ICU (CABG), Other Hospital, Telemetry, Other Internal, Other ICU, Floor, Step-Down Unit (SDU), etc. |  |
| unitdischargestatus | VARCHAR | varchar(10) | NULL |  |
| uniquepid | VARCHAR | NOT NULL | ID for a unique patient. |  |

### hospital

**Description:** Hospital characteristics and metadata

**Row Count:** 208

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| hospitalid | INTEGER | NOT NULL | surrogate key for the hospital  PK  S |  |
| numbedscategory | VARCHAR | int | number of beds |  |
| teachingstatus | BOOLEAN | teaching status of hospital | S |  |
| region | VARCHAR | region of hospital | S |  |

### lab

**Description:** Laboratory test results (~160 standardized measurements)

**Row Count:** 39,132,531

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| labid | INTEGER | IDENTITY | surrogate ID for the labs data  PK  C |  |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| labresultoffset | INTEGER | int | NOT NULL |  |
| labtypeid | DECIMAL(3,0) | NOT NULL | the type of lab that is represented in the values, 1 for chemistry, 2 for drug level, 3 for hemo, 4 for misc, 5 for non-mapped, 6 for sensitive, 7 for ABG lab |  |
| labname | VARCHAR | varchar(255) | NULL | PK |
| labresult | DECIMAL(11,4) | the numeric value of the lab e.g.: 7.3230,, 58.0000, 24.8000 | S |  |
| labresulttext | VARCHAR | NULL | the text of the lab value e.g.: 7.257, 58.0 24.8 |  |
| labmeasurenamesystem | VARCHAR | varchar(255) | NULL |  |
| labmeasurenameinterface | VARCHAR | varchar(255) | NULL |  |
| labresultrevisedoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the revised lab value was entered |  |

### customlab

**Description:** Non-standard laboratory measurements

**Row Count:** 1,082

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| customlabid | INTEGER | bigint  not null | PK |  |
| patientunitstayid | INTEGER |  |  |  |
| labotheroffset | INTEGER |  |  |  |
| labothertypeid | INTEGER |  |  |  |
| labothername | VARCHAR |  |  |  |
| labotherresult | VARCHAR |  |  |  |
| labothervaluetext | VARCHAR |  |  |  |

### vitalaperiodic

**Description:** Aperiodic (intermittent) vital signs

**Row Count:** 25,075,074

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| vitalaperiodicid | INTEGER | int | IDENTITY | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| observationoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the aperiodic value was entered |  |
| noninvasivesystolic | DOUBLE | real | NULL |  |
| noninvasivediastolic | DOUBLE | real | NULL |  |
| noninvasivemean | DOUBLE | real | NULL |  |
| paop | DOUBLE | real | NULL |  |
| cardiacoutput | DOUBLE | NULL | patient cardiac output value e.g.: 4.71, 5.81, 5.63, etc. |  |
| cardiacinput | DOUBLE | real | NULL |  |
| svr | DOUBLE | real | NULL |  |
| svri | DOUBLE | real | NULL |  |
| pvr | DOUBLE | real | NULL |  |
| pvri | DOUBLE | real | NULL |  |

### vitalperiodic

**Description:** Periodic (continuous) vital signs monitoring

**Row Count:** 146,671,642

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| vitalperiodicid | BIGINT |  |  |  |
| patientunitstayid | INTEGER |  |  |  |
| observationoffset | INTEGER |  |  |  |
| temperature | DECIMAL(11,4) |  |  |  |
| sao2 | INTEGER |  |  |  |
| heartrate | INTEGER |  |  |  |
| respiration | INTEGER |  |  |  |
| cvp | INTEGER |  |  |  |
| etco2 | INTEGER |  |  |  |
| systemicsystolic | INTEGER |  |  |  |
| systemicdiastolic | INTEGER |  |  |  |
| systemicmean | INTEGER |  |  |  |
| pasystolic | INTEGER |  |  |  |
| padiastolic | INTEGER |  |  |  |
| pamean | INTEGER |  |  |  |
| st1 | DOUBLE |  |  |  |
| st2 | DOUBLE |  |  |  |
| st3 | DOUBLE |  |  |  |
| icp | INTEGER |  |  |  |

### diagnosis

**Description:** Patient diagnoses and conditions

**Row Count:** 2,710,672

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| diagnosisid | INTEGER |  |  |  |
| patientunitstayid | INTEGER |  |  |  |
| activeupondischarge | VARCHAR |  |  |  |
| diagnosisoffset | INTEGER |  |  |  |
| diagnosisstring | VARCHAR |  |  |  |
| icd9code | VARCHAR |  |  |  |
| diagnosispriority | VARCHAR |  |  |  |

### admissiondx

**Description:** Admission diagnoses

**Row Count:** 626,858

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| admissiondxid | INTEGER | IDENTITY | surrogate key for the admission diagnosis   PK  C |  |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| admitdxenteredoffset | INTEGER | int | NOT NULL |  |
| admitdxpath | VARCHAR | varchar(500) | NOT NULL |  |
| admitdxname | VARCHAR | varchar(255) | NULL |  |
| admitdxtext | VARCHAR | varchar(255) | NULL |  |

### allergy

**Description:** Patient allergies

**Row Count:** 251,949

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| allergyid | INTEGER | IDENTITY | surrogate key for the allergy   PK  C |  |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| allergyoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the allergy was detected |  |
| allergyenteredoffset | INTEGER | int | NOT NULL |  |
| allergynotetype | VARCHAR | varchar(255) | NOT NULL |  |
| specialtytype | VARCHAR | NOT NULL | physician specialty picklist types e.g.: anesthesiology gastroenterology oncology |  |
| usertype | VARCHAR | varchar(255) | NULL |  |
| rxincluded | VARCHAR | Does the Note have associated Rx data: True or False | S |  |
| writtenineicu | VARCHAR | Was the Note written in the eICU: True or False | S |  |
| drugname | VARCHAR | varchar(255) | NULL |  |
| allergytype | VARCHAR | varchar(255) | NOT NULL |  |
| allergyname | VARCHAR | varchar(255) | NOT NULL |  |
| drughiclseqno | INTEGER | NULL | HICL sequence number for the drug if drug allergy e.g.: 2734, 33199, 20492 |  |

### pasthistory

**Description:** Past medical history

**Row Count:** 1,149,180

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| pasthistoryid | INTEGER | IDENTITY | surrogate key for the past history item | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| pasthistoryoffset | INTEGER | NOT NULL | number of minutes from unit admit time for the past history item |  |
| pasthistoryenteredoffset | INTEGER | int | NOT NULL |  |
| pasthistorynotetype | VARCHAR | varchar(20) | NULL |  |
| pasthistorypath | VARCHAR | varchar(255) | NOT NULL |  |
| pasthistoryvalue | VARCHAR | varchar(100) | NULL |  |
| pasthistoryvaluetext | VARCHAR | varchar(255) | NULL |  |

### admissiondrug

**Description:** Drugs administered at admission

**Row Count:** 874,920

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| admissiondrugid | INTEGER | int | IDENTITY |  |
| patientunitstayid | INTEGER | int | NOT NULL |  |
| drugoffset | INTEGER | int | NOT NULL |  |
| drugenteredoffset | INTEGER | int | NOT NULL |  |
| drugnotetype | VARCHAR | varchar(255) | NOT NULL |  |
| specialtytype | VARCHAR | varchar(255) | NOT NULL |  |
| usertype | VARCHAR | varchar(255) | NOT NULL |  |
| rxincluded | VARCHAR | varchar(5) | NOT NULL |  |
| writtenineicu | VARCHAR | varchar(5) | NOT NULL |  |
| drugname | VARCHAR | varchar(255) | NOT NULL |  |
| drugdosage | DECIMAL(11,4) | decimal(11,4) | NULL |  |
| drugunit | VARCHAR | varchar(1000) | NULL |  |
| drugadmitfrequency | VARCHAR | varchar(1000) | NULL |  |
| drughiclseqno | INTEGER | int | NULL |  |

### infusiondrug

**Description:** Infusion drug administration records

**Row Count:** 4,803,719

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| infusiondrugid | INTEGER | IDENTITY | surrogate key for infusion drugs | PK |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| infusionoffset | INTEGER | NOT NULL | number of minutes from unit admit time that infusion drug column was entered |  |
| drugname | VARCHAR | varchar(255) | NOT NULL |  |
| drugrate | VARCHAR | varchar(255) | NULL |  |
| infusionrate | VARCHAR | varchar(255) | NULL |  |
| drugamount | VARCHAR | NULL | the amount of drug given e.g.: 250, 100, 50, etc. |  |
| volumeoffluid | VARCHAR | NULL | volume of fluid for the infusion e.g.: 250, 100, 50, etc. |  |
| patientweight | VARCHAR | NULL | the patient weight recorded during the drug infusion in kilograms e.g.: 87.9, 76.3, 65.8, etc. |  |

### medication

**Description:** Medication administration records

**Row Count:** 7,301,853

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| medicationid | INTEGER | int | IDENTITY |  |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| drugorderoffset | INTEGER | int | NOT NULL |  |
| drugstartoffset | INTEGER | int | NOT NULL |  |
| drugivadmixture | VARCHAR | varchar(3)  NOT NULL | contains “Yes” if an IV admixture, “No” otherwise |  |
| drugordercancelled | VARCHAR | contains “Yes” if drug order was cancelled, “No” otherwise | S |  |
| drugname | VARCHAR | varchar(255) | NOT NULL |  |
| drughiclseqno | INTEGER | NULL | HICL for the drug e.g.: 8255, 6055, 1694, etc. |  |
| dosage | VARCHAR | NOT NULL | the dosage of the drug e.g.: 500 ml, 1 mcg/kg/min, 2.4 units/hour, etc. |  |
| routeadmin | VARCHAR | NOT NULL | the picklist route of administration for the drug e.g.: IV (intravenous), IV - continuous infusion (intravenous), PO (oral), etc. |  |
| frequency | VARCHAR | NOT NULL | the picklist frequency with which the drug is taken e.g.: Every 6 hour(s), twice a day, four times per day, etc. |  |
| loadingdose | VARCHAR | varchar(100) | NOT NULL |  |
| prn | VARCHAR | varchar(25) | NOT NULL |  |
| drugstopoffset | INTEGER | NULL | number of minutes from unit admit time that the drug was stopped |  |
| gtc | INTEGER | int | NULL |  |

### apacheapsvar

**Description:** APACHE Acute Physiology Score variables

**Row Count:** 171,177

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| apacheapsvarid | INTEGER |  |  |  |
| patientunitstayid | INTEGER |  |  |  |
| intubated | SMALLINT |  |  |  |
| vent | SMALLINT |  |  |  |
| dialysis | SMALLINT |  |  |  |
| eyes | SMALLINT |  |  |  |
| motor | SMALLINT |  |  |  |
| verbal | SMALLINT |  |  |  |
| meds | SMALLINT |  |  |  |
| urine | DOUBLE |  |  |  |
| wbc | DOUBLE |  |  |  |
| temperature | DOUBLE |  |  |  |
| respiratoryrate | DOUBLE |  |  |  |
| sodium | DOUBLE |  |  |  |
| heartrate | DOUBLE |  |  |  |
| meanbp | DOUBLE |  |  |  |
| ph | DOUBLE |  |  |  |
| hematocrit | DOUBLE |  |  |  |
| creatinine | DOUBLE |  |  |  |
| albumin | DOUBLE |  |  |  |
| pao2 | DOUBLE |  |  |  |
| pco2 | DOUBLE |  |  |  |
| bun | DOUBLE |  |  |  |
| glucose | DOUBLE |  |  |  |
| bilirubin | DOUBLE |  |  |  |
| fio2 | DOUBLE |  |  |  |

### apachepatientresult

**Description:** APACHE patient results and predictions

**Row Count:** 297,064

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| apachepatientresultsid | INTEGER |  |  |  |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| physicianspeciality | VARCHAR | varchar(50) | NULL |  |
| physicianinterventioncategory | VARCHAR | NULL | Physician Intervention Category picklist value |  |
| acutephysiologyscore | INTEGER | int | NULL |  |
| apachescore | INTEGER | int | NULL |  |
| apacheversion | VARCHAR | NOT NULL | The version of the APACHE algorithm used to produce the apacheScore (e.g 3, 4) |  |
| predictedicumortality | VARCHAR | NULL | Predicted ICU Mortality from Apache API |  |
| actualicumortality | VARCHAR | NULL | Actual ICU Mortality |  |
| predictediculos | DOUBLE | float(53)   NULL | Predicted ICU Length of Stay from Apache API |  |
| actualiculos | DOUBLE | float(53)   NULL | Actual ICU Length of Stay |  |
| predictedhospitalmortality | VARCHAR | NULL | Predicted Hospital Mortality from Apache API |  |
| actualhospitalmortality | VARCHAR | varchar(50) | NULL |  |
| predictedhospitallos | DOUBLE | float(53)   NULL | Predicted Hospital Length of Stay from Apache API |  |
| actualhospitallos | DOUBLE | Actual Hospital Length of Stay. Value is 50 when when > 50 days. | S |  |
| preopmi | INTEGER | int | NULL |  |
| preopcardiaccath | INTEGER | int | NULL |  |
| ptcawithin24h | INTEGER | NULL | 0/1. 1- Patient had PTCA with 24 hrs |  |
| unabridgedunitlos | DOUBLE | Actual ICU Length of stay | S |  |
| unabridgedhosplos | DOUBLE | Actual Hospital Length of stay | S |  |
| actualventdays | DOUBLE | Actual Ventilation days. Value is 30 when Actual Ventilation > 30 | S |  |
| predventdays | DOUBLE | float(53)   NULL | Predicted ventilation days from Apache API |  |
| unabridgedactualventdays | DOUBLE | float(53)   NULL | Actual Ventilation days |  |

### apachepredvar

**Description:** APACHE predictor variables

**Row Count:** 171,177

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| apachepredvarid | INTEGER | int | NOT NULL | PK |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| sicuday | SMALLINT | int | NULL |  |
| saps3day1 | SMALLINT | NULL | set to default value 0 |  |
| saps3today | SMALLINT | NULL | set to default value 0 |  |
| saps3yesterday | SMALLINT | NULL | set to default value 0 |  |
| gender | SMALLINT | NULL | Female =1, Male = 0 , Not available =-1 |  |
| teachtype | SMALLINT | NULL | Set to default value of 0 |  |
| region | SMALLINT | NULL | Set to default value of 3 |  |
| bedcount | SMALLINT | int | NULL |  |
| admitsource | SMALLINT | int | NULL |  |
| graftcount | SMALLINT | NULL | Number selected for the patient when a CABG admission diagnosis is selected for the patient in eCare. Default is 3 |  |
| meds | SMALLINT | int | NULL |  |
| verbal | SMALLINT | NULL | GCS verbal score from worst GCS set |  |
| motor | SMALLINT | NULL | GCS motor score from worst GCS set |  |
| eyes | SMALLINT | int | NULL |  |
| age | SMALLINT | int | NULL |  |
| admitdiagnosis | VARCHAR | NULL | Apache admission diagnosis code |  |
| thrombolytics | SMALLINT | NULL | 0/1. 0 – Patient doesn’t has thrombolytics, 1 - Patient has thrombolytics |  |
| diedinhospital | SMALLINT | NULL | 0/1. 1 – Patient died in hospital |  |
| aids | SMALLINT | int | NULL |  |
| hepaticfailure | SMALLINT | NULL | 0/1. 0 – Patient doesn’t has hepaticFailure, 1 - Patient has hepaticFailure |  |
| lymphoma | SMALLINT | int | NULL |  |
| metastaticcancer | SMALLINT | int | NULL |  |
| leukemia | SMALLINT | int | NULL |  |
| immunosuppression | SMALLINT | NULL | 0/1. 0 – Patient doesn’t has immunosuppression, 1 - Patient has immunosuppression |  |
| cirrhosis | SMALLINT | NULL | 0/1. 0 – Patient doesn’t has cirrhosis, 1 - Patient has cirrhosis |  |
| electivesurgery | SMALLINT | int | NULL |  |
| activetx | SMALLINT | int | NULL |  |
| readmit | SMALLINT | int | NULL |  |
| ima | SMALLINT | int | NULL |  |
| midur | SMALLINT | NULL | Indicates if patient had MI within 6 months |  |
| ventday1 | SMALLINT | int | NULL |  |
| oobventday1 | SMALLINT | int | NULL |  |
| oobintubday1 | SMALLINT | int | NULL |  |
| diabetes | SMALLINT | int | NULL |  |
| managementsystem | SMALLINT | int | NULL |  |
| var03hspxlos | DOUBLE | float(53)   NULL | Not used |  |
| pao2 | DOUBLE | float(53)   NULL | paO2 value from the worst ABG data set for the Apache Day |  |
| fio2 | DOUBLE | float(53)   NULL | fiO2 value from the worst ABG data set for the Apache Day |  |
| ejectfx | DOUBLE | float(53)   NULL | S |  |
| creatinine | DOUBLE | Worst creatinine value for the Apache day | S |  |
| dischargelocation | SMALLINT | NULL | Value indicating discharge location for the patient |  |
| visitnumber | SMALLINT | int | NULL |  |
| amilocation | SMALLINT | int | NULL |  |
| day1meds | SMALLINT | int | NULL |  |
| day1verbal | SMALLINT | NULL | GCS verbal score from worst GCS set |  |
| day1motor | SMALLINT | NULL | GCS motor score from worst GCS set |  |
| day1eyes | SMALLINT | int | NULL |  |
| day1pao2 | DOUBLE | float(53)   NULL | paO2 value from the worst ABG data set for the Apache Day |  |
| day1fio2 | DOUBLE | float(53)   NULL | fiO2 value from the worst ABG data set for the Apache Day |  |

### careplancareprovider

**Description:** Care plan provider information

**Row Count:** 502,765

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| cplcareprovderid | INTEGER |  |  |  |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table |  |
| careprovidersaveoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the care provider was entered |  |
| providertype | VARCHAR | varchar(255) | NULL |  |
| specialty | VARCHAR | NULL | the picklist specialty of the care provider e.g.: cardiology unknown obstetrics/gynecology |  |
| interventioncategory | VARCHAR | varchar(255) | NULL |  |
| managingphysician | VARCHAR | NULL | picklist value which denotes whether this care provider is the managing physician: Managing or Consulting |  |
| activeupondischarge | VARCHAR | varchar(10) | NOT NULL |  |

### careplaneol

**Description:** End-of-life care plans

**Row Count:** 1,433

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| cpleolid | INTEGER |  |  |  |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| cpleolsaveoffset | INTEGER | int | NOT NULL |  |
| cpleoldiscussionoffset | INTEGER | NULL | number of minutes from unit admit time that the EOL discussion occurred |  |
| activeupondischarge | VARCHAR | varchar(10) | NULL |  |

### careplangeneral

**Description:** General care plans

**Row Count:** 3,115,018

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| cplgeneralid | INTEGER | int | IDENTITY | PK |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| activeupondischarge | VARCHAR | varchar(10) | NULL |  |
| cplitemoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the care plan general item was entered |  |
| cplgroup | VARCHAR | varchar(255) | NOT NULL |  |
| cplitemvalue | VARCHAR | varchar(1024)   NULL | the picklist value selected / entered into the care plan group e.g.: Very low mortality risk, Non-invasive ventilation, Parenteral - bolus prn |  |

### careplangoal

**Description:** Care plan goals

**Row Count:** 504,139

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| cplgoalid | INTEGER |  |  |  |
| patientunitstayid | INTEGER |  |  |  |
| CPLGOALoffset | INTEGER |  |  |  |
| CPLGOALCATEGORY | VARCHAR |  |  |  |
| CPLGOALVALUE | VARCHAR |  |  |  |
| CPLGOALSTATUS | VARCHAR |  |  |  |
| ACTIVEUPONDISCHARGE | VARCHAR |  |  |  |

### careplaninfectiousdisease

**Description:** Infectious disease care plans

**Row Count:** 8,056

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| cplinfectid | INTEGER | int | IDENTITY |  |
| patientunitstayid | INTEGER | NOT NULL | a globally unique identifier (GUID) used as a foreign key link to the patient table | FK |
| activeupondischarge | VARCHAR | varchar(10) | NOT NULL |  |
| cplinfectdiseaseoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the infectious disease was entered |  |
| infectdiseasesite | VARCHAR | NULL | The picklist site of the infectious disease e.g.: Intra-abdominal, Blood, Catheter related bloodstream, etc. |  |
| infectdiseaseassessment | VARCHAR | varchar(255) | NULL |  |
| responsetotherapy | VARCHAR | NULL | the picklist response to the therapy: Improving, No change, Worsening, Resolved, or BLANK |  |
| treatment | VARCHAR | NULL | the picklist treatment for the infectious disease: Prophylactic, Empiric, Directed, or BLANK |  |

### nurseassessment

**Description:** Nursing assessments

**Row Count:** 15,602,498

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| nurseassessid | INTEGER |  |  |  |
| patientunitstayid | INTEGER |  |  |  |
| NURSEASSESSOFFSET | INTEGER |  |  |  |
| NURSEASSESSENTRYOFFSET | INTEGER |  |  |  |
| CELLATTRIBUTEPATH | VARCHAR |  |  |  |
| CELLLABEL | VARCHAR |  |  |  |
| CELLATTRIBUTE | VARCHAR |  |  |  |
| CELLATTRIBUTEVALUE | VARCHAR |  |  |  |

### nursecare

**Description:** Nursing care documentation

**Row Count:** 8,311,132

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| nursecareid | INTEGER | int | IDENTITY | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| CELLLABEL | VARCHAR | NOT NULL | label of the selected nursing care entry |  |
| NURSECAREOFFSET | INTEGER | int | NOT NULL |  |
| NURSECAREENTRYOFFSET | INTEGER | int | NOT NULL |  |
| CELLATTRIBUTEPATH | VARCHAR | NOT NULL | the full path string of the nursing care entry selected in eCareManager, the sections of the assessment will be separated by a | symbol e.g.: flowsheet | Flowsheet Cell Labels | Nursing Assessment | Scores | Braden Scale | Activity |  |
| CELLATTRIBUTE | VARCHAR | NOT NULL | attribute for the nursing care entry selected in eCareManager |  |
| CELLATTRIBUTEVALUE | VARCHAR | value for the nursing care attribute selected for the nursing care entry in eCareManager | S |  |

### nursecharting

**Description:** Nursing charting entries

**Row Count:** 151,604,232

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| nursingchartid | BIGINT | IDENTITY | surrogate key for the nurse charting | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| NURSINGCHARTOFFSET | INTEGER | NOT NULL | number of minutes from unit admit time that nursing chart column |  |
| NURSINGCHARTENTRYOFFSET | INTEGER | int | NOT NULL |  |
| NURSINGCHARTCELLTYPECAT | VARCHAR | varchar(255) | NOT NULL |  |
| NURSINGCHARTCELLTYPEVALLABEL | VARCHAR | varchar(255) | NOT NULL |  |
| NURSINGCHARTCELLTYPEVALNAME | VARCHAR | varchar(255) | NOT NULL |  |
| NURSINGCHARTVALUE | VARCHAR | NULL | The text that was entered manually or via a interface for the given Cell Type Val Lable e.g.: 100, 4 units, 35%, etc. |  |

### respiratorycare

**Description:** Respiratory care interventions

**Row Count:** 865,381

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| RESPCAREID | INTEGER | IDENTITY | surrogate key for the respiratory data  PK  C |  |
| PATIENTUNITSTAYID | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| RESPCARESTATUSOFFSET | INTEGER | int | NOT NULL |  |
| CURRENTHISTORYSEQNUM | INTEGER | int | NULL |  |
| AIRWAYTYPE | VARCHAR | NULL | the airway picklist type input into the respiratory care status e.g.: Laryngectomy, Tracheostomy, Oral ETT, etc. |  |
| AIRWAYSIZE | VARCHAR | NULL | the picklist airway size input into the respiratory care status e.g.: 35F, 9.5, NULL |  |
| AIRWAYPOSITION | VARCHAR | NULL | picklist airway position for the patient e.g.: 23 @ lip, 26 @ teeth, 20, etc. |  |
| CUFFPRESSURE | DECIMAL(5,1) | decimal(5,1) | NULL |  |
| VENTSTARTOFFSET | INTEGER | int | NULL |  |
| VENTENDOFFSET | INTEGER | NULL | number of minutes from unit admit time that the vent was ended |  |
| PRIORVENTSTARTOFFSET | INTEGER | int | NULL |  |
| PRIORVENTENDOFFSET | INTEGER | NULL | number of minutes from unit admit time that the prior vent was ended |  |
| APNEAPARAMS | VARCHAR | varchar(80) | NULL |  |
| LOWEXHMVLIMIT | DECIMAL(11,4) | the low Ex MV Limit of the vent e.g: 5.0000, 200.0000, 3.0000, etc. | S |  |
| HIEXHMVLIMIT | DECIMAL(11,4) | decimal(11,4)   NULL | the high Ex MV Limit of the vent e.g.: 18.000, 20.0000, 40.0000, etc. |  |
| LOWEXHTVLIMIT | DECIMAL(11,4) | the low Exh TV limit of the vent e.g.: 300.0000, 200.0000, 350.0000, etc. | S |  |
| HIPEAKPRESLIMIT | DECIMAL(11,4) | decimal(11,4)   NULL | the high peak pressure limit of the vent e.g.: 45.0000, 65.0000, 50.0000, etc. |  |
| LOWPEAKPRESLIMIT | DECIMAL(11,4) | decimal(11,4)   NULL | the low peak pressure limit of the vent e.g.: 10.0000, 150.0000, 15.0000, etc. |  |
| HIRESPRATELIMIT | DECIMAL(11,4) | decimal(11,4)   NULL | the high respiration rate limit of the vent e.g.: 40.0000, 32.0000, 24.0000, etc. |  |
| LOWRESPRATELIMIT | DECIMAL(11,4) | decimal(11,4)   NULL | the low respiration rate limit of the vent e.g.: 12.0000, 5.0000, 8.0000, etc. |  |
| SIGHPRESLIMIT | DECIMAL(11,4) | the sigh pressure limit of the vent | S |  |
| LOWIRONOXLIMIT | DECIMAL(11,4) | the low iron ox limit of the vent e.g.: 90.0000, 40.0000, 0.0000, etc. | S |  |
| HIGHIRONOXLIMIT | DECIMAL(11,4) | decimal(11,4)   NULL | the high iron ox limit of the vent e.g.: 100.0000, 120.0000, 90.0000, etc. |  |
| MEANAIRWAYPRESLIMIT | DECIMAL(11,4) | decimal(11,4)   NULL | the mean airway pressure limit of the vent e.g.: 60.0000, 45.0000, 50.0000, etc. |  |
| PEEPLIMIT | DECIMAL(11,4) | the PEEP limit of the vent e.g.: 10.0000, 14.0000, 8.0000, etc. | S |  |
| CPAPLIMIT | DECIMAL(11,4) | the CPAP limit of the vent e.g.: 2.0000, 10.0000, 5.0000, etc. | S |  |
| SETAPNEAINTERVAL | VARCHAR | varchar(80) | NULL |  |
| SETAPNEATV | VARCHAR | NULL | the picklist apnea TV of the vent e.g.: 300, 460, 800, etc. |  |
| SETAPNEAIPPEEPHIGH | VARCHAR | NULL | the picklist apnea IPPEEP high of the vent e.g.: 5, 7.0, 3.0, etc. |  |
| SETAPNEARR | VARCHAR | NULL | the apnea RR of the vent e.g.: 20, 10, 28, etc. |  |
| SETAPNEAPEAKFLOW | VARCHAR | varchar(80) | NULL |  |
| SETAPNEAINSPTIME | VARCHAR | varchar(80) | NULL |  |
| SETAPNEAIE | VARCHAR | NULL | the picklist apnea IE of the vent e.g.: 1:2, 1:5, 1:3, etc. |  |
| SETAPNEAFIO2 | VARCHAR | varchar(80) | NULL |  |

### respiratorycharting

**Description:** Respiratory charting data

**Row Count:** 20,168,176

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| RESPCHARTID | INTEGER | int | IDENTITY |  |
| PATIENTUNITSTAYID | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| RESPCHARTOFFSET | INTEGER | int | NOT NULL |  |
| RESPCHARTENTRYOFFSET | INTEGER | int | NOT NULL |  |
| RESPCHARTTYPECAT | VARCHAR | varchar(255) | NOT NULL |  |
| RESPCHARTVALUELABEL | VARCHAR | varchar(255) | NOT NULL |  |
| RESPCHARTVALUE | VARCHAR | The text that was entered manually or via a interface for the given Cell Type Val Label e.g.: in room, 102, 1:2.0, etc. | S |  |

### treatment

**Description:** Treatment interventions

**Row Count:** 3,688,745

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| treatmentid | INTEGER | int | IDENTITY |  |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| treatmentoffset | INTEGER | int | NOT NULL |  |
| treatmentstring | VARCHAR | varchar(200) | NOT NULL |  |
| activeupondischarge | VARCHAR | varchar(10) | NOT NULL |  |

### physicalexam

**Description:** Physical examination findings

**Row Count:** 9,212,316

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| physicalexamid | INTEGER | IDENTITY | surrogate key for the physical exam item | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| physicalexamoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the physical exam item was entered |  |
| physicalexampath | VARCHAR | varchar(255) | NOT NULL |  |
| physicalexamvalue | VARCHAR | NULL | Structured picklist of available of physical exam items: O2 Sat% Highest, withdraws to pain, HR Current, etc. |  |
| physicalexamtext | VARCHAR | varchar(500) | NOT NULL |  |

### intakeoutput

**Description:** Fluid intake and output records

**Row Count:** 12,030,289

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| intakeoutputid | INTEGER | IDENTITY | surrogate key for the intake output data | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK |  |
| intakeoutputoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the I and O value was observed |  |
| intaketotal | DECIMAL(12,4) | decimal(12,4)   NULL | total intake value up to the current offset, e.g.: 150.0000, 326.0000, 142.0000, etc. |  |
| outputtotal | DECIMAL(12,4) | decimal(12,4)   NULL | total output value up to the current offset, e.g.: 230.0000, 350.0000, 150.0000, etc. |  |
| dialysistotal | DECIMAL(12,4) |  |  |  |
| nettotal | DECIMAL(12,4) | decimal(12,4)   NULL | calculated net value of: intakeTotal – outputTotal + dialysisTotal |  |
| intakeoutputentryoffset | INTEGER | int | NOT NULL |  |
| cellpath | VARCHAR | varchar(500) | NOT NULL |  |
| celllabel | VARCHAR | NOT NULL | The predefined row label text from I and O e.g.: Enteral flush/meds panda, D5 0.45 NS w/20 mEq KCL 1000 ml, Continuous infusion meds, etc. |  |
| cellvaluenumeric | DECIMAL(12,4) | decimal(12,4)   NOT NULL | the value of the current I and O row e.g.: 100.0000, 60.9000, 10.0000, etc. |  |
| cellvaluetext | VARCHAR | NOT NULL | text conversion of the numeric value of the I and O row e.g.: 100, 360, 50 |  |

### microlab

**Description:** Microbiology laboratory results

**Row Count:** 16,996

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| microlabid | INTEGER | IDENTITY | surrogate key for the micro lab | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| culturetakenoffset | INTEGER | NOT NULL | number of minutes from unit admit time that the culture was taken |  |
| culturesite | VARCHAR | varchar(255) | NOT NULL |  |
| organism | VARCHAR | varchar(255) | NOT NULL |  |
| antibiotic | VARCHAR | NULL | picklist antibiotic used e.g.: ceftazidime, aztreonam, other, etc. |  |
| sensitivitylevel | VARCHAR | varchar(255) | NULL |  |

### note

**Description:** Clinical notes

**Row Count:** 2,254,179

| Column Name | Data Type | Null | Description | Key |
|-------------|-----------|------|-------------|-----|
| NOTEID | INTEGER | IDENTITY | surrogate key for the note item | PK |
| patientunitstayid | INTEGER | NOT NULL | foreign key link to the patient table   FK  C |  |
| NOTEOFFSET | INTEGER | NOT NULL | number of minutes from unit admit time for the note item, derived from the note’s date of service |  |
| NOTEENTEREDOFFSET | INTEGER | NOT NULL | number of minutes from unit admit time that the note item was entered |  |
| NOTETYPE | VARCHAR | varchar(50) | NULL |  |
| NOTEPATH | VARCHAR | varchar(255) | NOT NULL |  |
| NOTEVALUE | VARCHAR | NULL | the picklist value name of the note item e.g.: HR Highest, Dx, Verified procedure, etc. |  |
| NOTETEXT | VARCHAR | varchar(255) | NULL |  |
