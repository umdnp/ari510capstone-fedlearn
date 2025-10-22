# eICU-CRD Data Dictionary (Enriched)

This data dictionary combines schema information with detailed metadata from the eICU-CRD database.

## Column Legend

- **Nullable**: Indicates if the column can contain NULL values (NULL or NOT NULL)
- **Description**: Detailed description of the column's purpose and content
- **Key**: Indicates if the column is a Primary Key (PK) or Foreign Key (FK)

---

### admissiondrug

**Description:** Drugs administered at admission

**Row Count:** 874,920

**Columns:** 14

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| admissiondrugid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| drugoffset | int4(10) | NOT NULL |  |
| drugenteredoffset | int4(10) | NOT NULL |  |
| drugnotetype | varchar(255) | NULL |  |
| specialtytype | varchar(255) | NULL |  |
| usertype | varchar(255) | NOT NULL |  |
| rxincluded | varchar(5) | NULL |  |
| writtenineicu | varchar(5) | NULL |  |
| drugname | varchar(255) | NOT NULL |  |
| drugdosage | numeric(11,4) | NULL |  |
| drugunit | varchar(1000) | NULL |  |
| drugadmitfrequency | varchar(1000) | NOT NULL |  |
| drughiclseqno | int4(10) | NULL |  |

### admissiondx

**Description:** Admission diagnoses

**Row Count:** 626,858

**Columns:** 6

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| admissiondxid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| admitdxenteredoffset | int4(10) | NOT NULL |  |
| admitdxpath | varchar(500) | NOT NULL |  |
| admitdxname | varchar(255) | NULL |  |
| admitdxtext | varchar(255) | NULL |  |

### allergy

**Description:** Patient allergies

**Row Count:** 251,949

**Columns:** 13

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| allergyid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| allergyoffset | int4(10) | NOT NULL |  |
| allergyenteredoffset | int4(10) | NOT NULL |  |
| allergynotetype | varchar(255) | NULL |  |
| specialtytype | varchar(255) | NULL |  |
| usertype | varchar(255) | NOT NULL |  |
| rxincluded | varchar(5) | NULL |  |
| writtenineicu | varchar(5) | NULL |  |
| drugname | varchar(255) | NOT NULL |  |
| allergytype | varchar(255) | NULL |  |
| allergyname | varchar(255) | NULL |  |
| drughiclseqno | int4(10) | NULL |  |

### apacheapsvar

**Description:** APACHE Acute Physiology Score variables

**Row Count:** 171,177

**Columns:** 26

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| apacheapsvarid | int4(10) | NULL | PK |
| patientunitstayid | int4(10) | NULL | FK |
| intubated | int2(5) | NULL |  |
| vent | int2(5) | NULL |  |
| dialysis | int2(5) | NULL |  |
| eyes | int2(5) | NULL |  |
| motor | int2(5) | NULL |  |
| verbal | int2(5) | NULL |  |
| meds | int2(5) | NULL |  |
| urine | float8(17,17) | NULL |  |
| wbc | float8(17,17) | NULL |  |
| temperature | float8(17,17) | NULL |  |
| respiratoryrate | float8(17,17) | NULL |  |
| sodium | float8(17,17) | NULL |  |
| heartrate | float8(17,17) | NULL |  |
| meanbp | float8(17,17) | NULL |  |
| ph | float8(17,17) | NULL |  |
| hematocrit | float8(17,17) | NULL |  |
| creatinine | float8(17,17) | NULL |  |
| albumin | float8(17,17) | NULL |  |
| pao2 | float8(17,17) | NULL |  |
| pco2 | float8(17,17) | NULL |  |
| bun | float8(17,17) | NULL |  |
| glucose | float8(17,17) | NULL |  |
| bilirubin | float8(17,17) | NULL |  |
| fio2 | float8(17,17) | NULL |  |

### apachepatientresult

**Description:** APACHE patient results and predictions

**Row Count:** 297,064

**Columns:** 23

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| apachepatientresultsid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| physicianspeciality | varchar(50) | NULL |  |
| physicianinterventioncategory | varchar(50) | NULL |  |
| acutephysiologyscore | int4(10) | NULL |  |
| apachescore | int4(10) | NULL |  |
| apacheversion | varchar(5) | NOT NULL |  |
| predictedicumortality | varchar(50) | NULL |  |
| actualicumortality | varchar(50) | NULL |  |
| predictediculos | float8(17,17) | NULL |  |
| actualiculos | float8(17,17) | NULL |  |
| predictedhospitalmortality | varchar(50) | NULL |  |
| actualhospitalmortality | varchar(50) | NULL |  |
| predictedhospitallos | float8(17,17) | NULL |  |
| actualhospitallos | float8(17,17) | NULL |  |
| preopmi | int4(10) | NULL |  |
| preopcardiaccath | int4(10) | NULL |  |
| ptcawithin24h | int4(10) | NULL |  |
| unabridgedunitlos | float8(17,17) | NULL |  |
| unabridgedhosplos | float8(17,17) | NULL |  |
| actualventdays | float8(17,17) | NULL |  |
| predventdays | float8(17,17) | NULL |  |
| unabridgedactualventdays | float8(17,17) | NULL |  |

### apachepredvar

**Description:** APACHE predictor variables

**Row Count:** 171,177

**Columns:** 51

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| apachepredvarid | int4(10) | NULL | PK |
| patientunitstayid | int4(10) | NULL | FK |
| sicuday | int2(5) | NULL |  |
| saps3day1 | int2(5) | NULL |  |
| saps3today | int2(5) | NULL |  |
| saps3yesterday | int2(5) | NULL |  |
| gender | int2(5) | NULL |  |
| teachtype | int2(5) | NULL |  |
| region | int2(5) | NULL |  |
| bedcount | int2(5) | NULL |  |
| admitsource | int2(5) | NULL |  |
| graftcount | int2(5) | NULL |  |
| meds | int2(5) | NULL |  |
| verbal | int2(5) | NULL |  |
| motor | int2(5) | NULL |  |
| eyes | int2(5) | NULL |  |
| age | int2(5) | NULL |  |
| admitdiagnosis | varchar(11) | NULL |  |
| thrombolytics | int2(5) | NULL |  |
| diedinhospital | int2(5) | NULL |  |
| aids | int2(5) | NULL |  |
| hepaticfailure | int2(5) | NULL |  |
| lymphoma | int2(5) | NULL |  |
| metastaticcancer | int2(5) | NULL |  |
| leukemia | int2(5) | NULL |  |
| immunosuppression | int2(5) | NULL |  |
| cirrhosis | int2(5) | NULL |  |
| electivesurgery | int2(5) | NULL |  |
| activetx | int2(5) | NULL |  |
| readmit | int2(5) | NULL |  |
| ima | int2(5) | NULL |  |
| midur | int2(5) | NULL |  |
| ventday1 | int2(5) | NULL |  |
| oobventday1 | int2(5) | NULL |  |
| oobintubday1 | int2(5) | NULL |  |
| diabetes | int2(5) | NULL |  |
| managementsystem | int2(5) | NULL |  |
| var03hspxlos | float8(17,17) | NULL |  |
| pao2 | float8(17,17) | NULL |  |
| fio2 | float8(17,17) | NULL |  |
| ejectfx | float8(17,17) | NULL |  |
| creatinine | float8(17,17) | NULL |  |
| dischargelocation | int2(5) | NULL |  |
| visitnumber | int2(5) | NULL |  |
| amilocation | int2(5) | NULL |  |
| day1meds | int2(5) | NULL |  |
| day1verbal | int2(5) | NULL |  |
| day1motor | int2(5) | NULL |  |
| day1eyes | int2(5) | NULL |  |
| day1pao2 | float8(17,17) | NULL |  |
| day1fio2 | float8(17,17) | NULL |  |

### careplancareprovider

**Description:** Care plan provider information

**Row Count:** 502,765

**Columns:** 8

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| cplcareprovderid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| careprovidersaveoffset | int4(10) | NOT NULL |  |
| providertype | varchar(255) | NULL |  |
| specialty | varchar(255) | NULL |  |
| interventioncategory | varchar(255) | NULL |  |
| managingphysician | varchar(50) | NULL |  |
| activeupondischarge | varchar(10) | NOT NULL |  |

### careplaneol

**Description:** End-of-life care plans

**Row Count:** 1,433

**Columns:** 5

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| cpleolid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| cpleolsaveoffset | int4(10) | NOT NULL |  |
| cpleoldiscussionoffset | int4(10) | NULL |  |
| activeupondischarge | varchar(10) | NULL |  |

### careplangeneral

**Description:** General care plans

**Row Count:** 3,115,018

**Columns:** 6

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| cplgeneralid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| activeupondischarge | varchar(10) | NOT NULL |  |
| cplitemoffset | int4(10) | NOT NULL |  |
| cplgroup | varchar(255) | NOT NULL |  |
| cplitemvalue | varchar(1024) | NULL |  |

### careplangoal

**Description:** Care plan goals

**Row Count:** 504,139

**Columns:** 7

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| cplgoalid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| cplgoaloffset | int4(10) | NOT NULL |  |
| cplgoalcategory | varchar(255) | NULL |  |
| cplgoalvalue | varchar(1000) | NULL |  |
| cplgoalstatus | varchar(255) | NULL |  |
| activeupondischarge | varchar(10) | NOT NULL |  |

### careplaninfectiousdisease

**Description:** Infectious disease care plans

**Row Count:** 8,056

**Columns:** 8

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| cplinfectid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| activeupondischarge | varchar(10) | NOT NULL |  |
| cplinfectdiseaseoffset | int4(10) | NOT NULL |  |
| infectdiseasesite | varchar(64) | NULL |  |
| infectdiseaseassessment | varchar(64) | NULL |  |
| responsetotherapy | varchar(32) | NULL |  |
| treatment | varchar(32) | NULL |  |

### customlab

**Description:** Non-standard laboratory measurements

**Row Count:** 1,082

**Columns:** 7

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| customlabid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| labotheroffset | int4(10) | NOT NULL |  |
| labothertypeid | int4(10) | NOT NULL |  |
| labothername | varchar(64) | NULL |  |
| labotherresult | varchar(64) | NULL |  |
| labothervaluetext | varchar(128) | NULL |  |

### diagnosis

**Description:** Patient diagnoses and conditions

**Row Count:** 2,710,672

**Columns:** 12

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| diagnosisid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| activeupondischarge | varchar(64) | NULL |  |
| diagnosisoffset | int4(10) | NOT NULL |  |
| diagnosisstring | varchar(200) | NOT NULL |  |
| icd9code | varchar(100) | NULL |  |
| diagnosispriority | varchar(10) | NOT NULL |  |
| able eicu.eicu_crd.hospital |  | NOT NULL |  |
| hospitalid | int4(10) | NOT NULL |  |
| numbedscategory | varchar(32) | NULL |  |
| teachingstatus | bool(1) | NULL |  |
| region | varchar(64) | NULL |  |

### infusiondrug

**Description:** Infusion drug administration records

**Row Count:** 4,803,719

**Columns:** 9

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| infusiondrugid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| infusionoffset | int4(10) | NOT NULL |  |
| drugname | varchar(255) | NOT NULL |  |
| drugrate | varchar(255) | NULL |  |
| infusionrate | varchar(255) | NULL |  |
| drugamount | varchar(255) | NULL |  |
| volumeoffluid | varchar(255) | NULL |  |
| patientweight | varchar(255) | NULL |  |

### intakeoutput

**Description:** Fluid intake and output records

**Row Count:** 12,030,289

**Columns:** 12

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| intakeoutputid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| intakeoutputoffset | int4(10) | NOT NULL |  |
| intaketotal | numeric(12,4) | NULL |  |
| outputtotal | numeric(12,4) | NULL |  |
| dialysistotal | numeric(12,4) | NULL |  |
| nettotal | numeric(12,4) | NULL |  |
| intakeoutputentryoffset | int4(10) | NOT NULL |  |
| cellpath | varchar(500) | NULL |  |
| celllabel | varchar(255) | NULL |  |
| cellvaluenumeric | numeric(12,4) | NOT NULL |  |
| cellvaluetext | varchar(255) | NOT NULL |  |

### lab

**Description:** Laboratory test results (~160 standardized measurements)

**Row Count:** 39,132,531

**Columns:** 10

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| labid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| labresultoffset | int4(10) | NOT NULL |  |
| labtypeid | numeric(3) | NOT NULL |  |
| labname | varchar(256) | NULL |  |
| labresult | numeric(11,4) | NULL |  |
| labresulttext | varchar(255) | NULL |  |
| labmeasurenamesystem | varchar(255) | NULL |  |
| labmeasurenameinterface | varchar(255) | NULL |  |
| labresultrevisedoffset | int4(10) | NULL |  |

### medication

**Description:** Medication administration records

**Row Count:** 7,301,853

**Columns:** 15

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| medicationid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| drugorderoffset | int4(10) | NOT NULL |  |
| drugstartoffset | int4(10) | NOT NULL |  |
| drugivadmixture | varchar(6) | NOT NULL |  |
| drugordercancelled | varchar(6) | NOT NULL |  |
| drugname | varchar(220) | NULL |  |
| drughiclseqno | int4(10) | NULL |  |
| dosage | varchar(60) | NULL |  |
| routeadmin | varchar(120) | NULL |  |
| frequency | varchar(255) | NULL |  |
| loadingdose | varchar(120) | NOT NULL |  |
| prn | varchar(6) | NOT NULL |  |
| drugstopoffset | int4(10) | NOT NULL |  |
| gtc | int4(10) | NOT NULL |  |

### microlab

**Description:** Microbiology laboratory results

**Row Count:** 16,996

**Columns:** 7

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| microlabid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| culturetakenoffset | int4(10) | NOT NULL |  |
| culturesite | varchar(255) | NOT NULL |  |
| organism | varchar(255) | NOT NULL |  |
| antibiotic | varchar(255) | NULL |  |
| sensitivitylevel | varchar(255) | NULL |  |

### note

**Description:** Clinical notes

**Row Count:** 2,254,179

**Columns:** 8

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| noteid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| noteoffset | int4(10) | NOT NULL |  |
| noteenteredoffset | int4(10) | NOT NULL |  |
| notetype | varchar(50) | NOT NULL |  |
| notepath | varchar(255) | NOT NULL |  |
| notevalue | varchar(150) | NULL |  |
| notetext | varchar(500) | NULL |  |

### nurseassessment

**Description:** Nursing assessments

**Row Count:** 15,602,498

**Columns:** 8

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| nurseassessid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| nurseassessoffset | int4(10) | NOT NULL |  |
| nurseassessentryoffset | int4(10) | NOT NULL |  |
| cellattributepath | varchar(255) | NOT NULL |  |
| celllabel | varchar(255) | NOT NULL |  |
| cellattribute | varchar(255) | NOT NULL |  |
| cellattributevalue | varchar(4000) | NULL |  |

### nursecare

**Description:** Nursing care documentation

**Row Count:** 8,311,132

**Columns:** 8

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| nursecareid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| celllabel | varchar(255) | NOT NULL |  |
| nursecareoffset | int4(10) | NOT NULL |  |
| nursecareentryoffset | int4(10) | NOT NULL |  |
| cellattributepath | varchar(255) | NOT NULL |  |
| cellattribute | varchar(255) | NOT NULL |  |
| cellattributevalue | varchar(4000) | NULL |  |

### nursecharting

**Description:** Nursing charting entries

**Row Count:** 151,604,232

**Columns:** 8

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| nursingchartid | int8(19) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| nursingchartoffset | int4(10) | NOT NULL |  |
| nursingchartentryoffset | int4(10) | NOT NULL |  |
| nursingchartcelltypecat | varchar(255) | NOT NULL |  |
| nursingchartcelltypevallabel | varchar(255) | NULL |  |
| nursingchartcelltypevalname | varchar(255) | NULL |  |
| nursingchartvalue | varchar(255) | NULL |  |

### pasthistory

**Description:** Past medical history

**Row Count:** 1,149,180

**Columns:** 8

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| pasthistoryid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| pasthistoryoffset | int4(10) | NOT NULL |  |
| pasthistoryenteredoffset | int4(10) | NOT NULL |  |
| pasthistorynotetype | varchar(40) | NULL |  |
| pasthistorypath | varchar(255) | NOT NULL |  |
| pasthistoryvalue | varchar(100) | NULL |  |
| pasthistoryvaluetext | varchar(255) | NULL |  |

### patient

**Description:** Core patient demographics and ICU stay information

**Row Count:** 200,859

**Columns:** 29

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| patientunitstayid | int4(10) | NOT NULL | PK |
| patienthealthsystemstayid | int4(10) | NULL |  |
| gender | varchar(25) | NULL |  |
| age | varchar(10) | NULL |  |
| ethnicity | varchar(50) | NULL |  |
| hospitalid | int4(10) | NULL |  |
| wardid | int4(10) | NULL |  |
| apacheadmissiondx | varchar(1000) | NULL |  |
| admissionheight | numeric(10,2) | NULL |  |
| hospitaladmittime24 | varchar(8) | NULL |  |
| hospitaladmitoffset | int4(10) | NULL |  |
| hospitaladmitsource | varchar(30) | NULL |  |
| hospitaldischargeyear | int2(5) | NULL |  |
| hospitaldischargetime24 | varchar(8) | NULL |  |
| hospitaldischargeoffset | int4(10) | NULL |  |
| hospitaldischargelocation | varchar(100) | NULL |  |
| hospitaldischargestatus | varchar(10) | NULL |  |
| unittype | varchar(50) | NULL |  |
| unitadmittime24 | varchar(8) | NULL |  |
| unitadmitsource | varchar(100) | NULL |  |
| unitvisitnumber | int4(10) | NULL |  |
| unitstaytype | varchar(15) | NULL |  |
| admissionweight | numeric(10,2) | NULL |  |
| dischargeweight | numeric(10,2) | NULL |  |
| unitdischargetime24 | varchar(8) | NULL |  |
| unitdischargeoffset | int4(10) | NULL |  |
| unitdischargelocation | varchar(100) | NULL |  |
| unitdischargestatus | varchar(10) | NULL |  |
| uniquepid | varchar(10) | NULL |  |

### physicalexam

**Description:** Physical examination findings

**Row Count:** 9,212,316

**Columns:** 6

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| physicalexamid | int4(10) | NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| physicalexamoffset | int4(10) | NOT NULL |  |
| physicalexampath | varchar(255) | NOT NULL |  |
| physicalexamvalue | varchar(100) | NULL |  |
| physicalexamtext | varchar(500) | NULL |  |

### respiratorycare

**Description:** Respiratory care interventions

**Row Count:** 865,381

**Columns:** 34

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| respcareid | int4(10) | NULL | PK |
| patientunitstayid | int4(10) | NULL | FK |
| respcarestatusoffset | int4(10) | NULL |  |
| currenthistoryseqnum | int4(10) | NULL |  |
| airwaytype | varchar(30) | NULL |  |
| airwaysize | varchar(10) | NULL |  |
| airwayposition | varchar(32) | NULL |  |
| cuffpressure | numeric(5,1) | NULL |  |
| ventstartoffset | int4(10) | NULL |  |
| ventendoffset | int4(10) | NULL |  |
| priorventstartoffset | int4(10) | NULL |  |
| priorventendoffset | int4(10) | NULL |  |
| apneaparams | varchar(80) | NULL |  |
| lowexhmvlimit | numeric(11,4) | NULL |  |
| hiexhmvlimit | numeric(11,4) | NULL |  |
| lowexhtvlimit | numeric(11,4) | NULL |  |
| hipeakpreslimit | numeric(11,4) | NULL |  |
| lowpeakpreslimit | numeric(11,4) | NULL |  |
| hirespratelimit | numeric(11,4) | NULL |  |
| lowrespratelimit | numeric(11,4) | NULL |  |
| sighpreslimit | numeric(11,4) | NULL |  |
| lowironoxlimit | numeric(11,4) | NULL |  |
| highironoxlimit | numeric(11,4) | NULL |  |
| meanairwaypreslimit | numeric(11,4) | NULL |  |
| peeplimit | numeric(11,4) | NULL |  |
| cpaplimit | numeric(11,4) | NULL |  |
| setapneainterval | varchar(80) | NULL |  |
| setapneatv | varchar(80) | NULL |  |
| setapneaippeephigh | varchar(80) | NULL |  |
| setapnearr | varchar(80) | NULL |  |
| setapneapeakflow | varchar(80) | NULL |  |
| setapneainsptime | varchar(80) | NULL |  |
| setapneaie | varchar(80) | NULL |  |
| setapneafio2 | varchar(80) | NULL |  |

### respiratorycharting

**Description:** Respiratory charting data

**Row Count:** 20,168,176

**Columns:** 7

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| respchartid | int4(10) | NULL | PK |
| patientunitstayid | int4(10) | NULL | FK |
| respchartoffset | int4(10) | NULL |  |
| respchartentryoffset | int4(10) | NULL |  |
| respcharttypecat | varchar(255) | NULL |  |
| respchartvaluelabel | varchar(255) | NULL |  |
| respchartvalue | varchar(1000) | NULL |  |

### treatment

**Description:** Treatment interventions

**Row Count:** 3,688,745

**Columns:** 5

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| treatmentid | int4(10) | NULL | PK |
| patientunitstayid | int4(10) | NULL | FK |
| treatmentoffset | int4(10) | NULL |  |
| treatmentstring | varchar(200) | NULL |  |
| activeupondischarge | varchar(10) | NULL |  |

### vitalaperiodic

**Description:** Aperiodic (intermittent) vital signs

**Row Count:** 25,075,074

**Columns:** 13

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| vitalaperiodicid | int4(10) | NOT NULL | PK |
| patientunitstayid | int4(10) | NOT NULL | FK |
| observationoffset | int4(10) | NOT NULL |  |
| noninvasivesystolic | float8(17,17) | NULL |  |
| noninvasivediastolic | float8(17,17) | NULL |  |
| noninvasivemean | float8(17,17) | NULL |  |
| paop | float8(17,17) | NULL |  |
| cardiacoutput | float8(17,17) | NULL |  |
| cardiacinput | float8(17,17) | NULL |  |
| svr | float8(17,17) | NULL |  |
| svri | float8(17,17) | NULL |  |
| pvr | float8(17,17) | NULL |  |
| pvri | float8(17,17) | NULL |  |

### vitalperiodic

**Description:** Periodic (continuous) vital signs monitoring

**Row Count:** 146,671,642

**Columns:** 19

| Column Name | Data Type | Nullable | Key |
|-------------|-----------|----------|-----|
| vitalperiodicid | int8(19) | NULL | PK |
| patientunitstayid | int4(10) | NULL | FK |
| observationoffset | int4(10) | NULL |  |
| temperature | numeric(11,4) | NULL |  |
| sao2 | int4(10) | NULL |  |
| heartrate | int4(10) | NULL |  |
| respiration | int4(10) | NULL |  |
| cvp | int4(10) | NULL |  |
| etco2 | int4(10) | NULL |  |
| systemicsystolic | int4(10) | NULL |  |
| systemicdiastolic | int4(10) | NULL |  |
| systemicmean | int4(10) | NULL |  |
| pasystolic | int4(10) | NULL |  |
| padiastolic | int4(10) | NULL |  |
| pamean | int4(10) | NULL |  |
| st1 | float8(17,17) | NULL |  |
| st2 | float8(17,17) | NULL |  |
| st3 | float8(17,17) | NULL |  |
| icp | int4(10) | NULL |  |
