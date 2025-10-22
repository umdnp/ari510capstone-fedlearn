# eICU-CRD Data Dictionary

Data dictionary for the eICU Collaborative Research Database (eICU-CRD v2.0)

## Overview

The eICU-CRD is built from the Philips eICU telehealth program, covering patient admissions from 2014-2015 across continental U.S. critical care units.

**Database Statistics:**
- Total Tables: 31
- Total Rows: 457,325,320

## Key Identifiers

- **hospitalid** - Unique hospital identifier
- **uniquepid** - Patient identifier (consistent across hospital stays)
- **patienthealthsystemstayid** - Hospital stay identifier
- **patientunitstayid** - ICU unit stay identifier (primary key for most tables)

## Time Representation

Event timestamps are stored as **offsets from ICU admission time, in minutes**:
- Positive values = events after ICU admission
- Negative values = events before ICU admission (e.g., emergency department)

---

## Table of Contents

- [Core Tables](#core-tables)
- [Clinical Measurements](#clinical-measurements)
- [Diagnoses and Conditions](#diagnoses-and-conditions)
- [Medications](#medications)
- [APACHE Scoring](#apache-scoring)
- [Care Planning](#care-planning)
- [Nursing Documentation](#nursing-documentation)
- [Respiratory Care](#respiratory-care)
- [Other Clinical Data](#other-clinical-data)

---

## Core Tables

### patient

**Description:** Core patient demographics and ICU stay information

**Row Count:** 200,859

**Columns:** 29

| Column Name | Data Type |
|-------------|-----------|
| patientunitstayid | INTEGER |
| patienthealthsystemstayid | INTEGER |
| gender | VARCHAR |
| age | VARCHAR |
| ethnicity | VARCHAR |
| hospitalid | INTEGER |
| wardid | INTEGER |
| apacheadmissiondx | VARCHAR |
| admissionheight | DECIMAL(10,2) |
| hospitaladmittime24 | VARCHAR |
| hospitaladmitoffset | INTEGER |
| hospitaladmitsource | VARCHAR |
| hospitaldischargeyear | SMALLINT |
| hospitaldischargetime24 | VARCHAR |
| hospitaldischargeoffset | INTEGER |
| hospitaldischargelocation | VARCHAR |
| hospitaldischargestatus | VARCHAR |
| unittype | VARCHAR |
| unitadmittime24 | VARCHAR |
| unitadmitsource | VARCHAR |
| unitvisitnumber | INTEGER |
| unitstaytype | VARCHAR |
| admissionweight | DECIMAL(10,2) |
| dischargeweight | DECIMAL(10,2) |
| unitdischargetime24 | VARCHAR |
| unitdischargeoffset | INTEGER |
| unitdischargelocation | VARCHAR |
| unitdischargestatus | VARCHAR |
| uniquepid | VARCHAR |

### hospital

**Description:** Hospital characteristics and metadata

**Row Count:** 208

**Columns:** 4

| Column Name | Data Type |
|-------------|-----------|
| hospitalid | INTEGER |
| numbedscategory | VARCHAR |
| teachingstatus | BOOLEAN |
| region | VARCHAR |

---

## Clinical Measurements

### lab

**Description:** Laboratory test results (~160 standardized measurements)

**Row Count:** 39,132,531

**Columns:** 10

| Column Name | Data Type |
|-------------|-----------|
| labid | INTEGER |
| patientunitstayid | INTEGER |
| labresultoffset | INTEGER |
| labtypeid | DECIMAL(3,0) |
| labname | VARCHAR |
| labresult | DECIMAL(11,4) |
| labresulttext | VARCHAR |
| labmeasurenamesystem | VARCHAR |
| labmeasurenameinterface | VARCHAR |
| labresultrevisedoffset | INTEGER |

### customlab

**Description:** Non-standard laboratory measurements

**Row Count:** 1,082

**Columns:** 7

| Column Name | Data Type |
|-------------|-----------|
| customlabid | INTEGER |
| patientunitstayid | INTEGER |
| labotheroffset | INTEGER |
| labothertypeid | INTEGER |
| labothername | VARCHAR |
| labotherresult | VARCHAR |
| labothervaluetext | VARCHAR |

### vitalaperiodic

**Description:** Aperiodic (intermittent) vital signs

**Row Count:** 25,075,074

**Columns:** 13

| Column Name | Data Type |
|-------------|-----------|
| vitalaperiodicid | INTEGER |
| patientunitstayid | INTEGER |
| observationoffset | INTEGER |
| noninvasivesystolic | DOUBLE |
| noninvasivediastolic | DOUBLE |
| noninvasivemean | DOUBLE |
| paop | DOUBLE |
| cardiacoutput | DOUBLE |
| cardiacinput | DOUBLE |
| svr | DOUBLE |
| svri | DOUBLE |
| pvr | DOUBLE |
| pvri | DOUBLE |

### vitalperiodic

**Description:** Periodic (continuous) vital signs monitoring

**Row Count:** 146,671,642

**Columns:** 19

| Column Name | Data Type |
|-------------|-----------|
| vitalperiodicid | BIGINT |
| patientunitstayid | INTEGER |
| observationoffset | INTEGER |
| temperature | DECIMAL(11,4) |
| sao2 | INTEGER |
| heartrate | INTEGER |
| respiration | INTEGER |
| cvp | INTEGER |
| etco2 | INTEGER |
| systemicsystolic | INTEGER |
| systemicdiastolic | INTEGER |
| systemicmean | INTEGER |
| pasystolic | INTEGER |
| padiastolic | INTEGER |
| pamean | INTEGER |
| st1 | DOUBLE |
| st2 | DOUBLE |
| st3 | DOUBLE |
| icp | INTEGER |

---

## Diagnoses and Conditions

### diagnosis

**Description:** Patient diagnoses and conditions

**Row Count:** 2,710,672

**Columns:** 7

| Column Name | Data Type |
|-------------|-----------|
| diagnosisid | INTEGER |
| patientunitstayid | INTEGER |
| activeupondischarge | VARCHAR |
| diagnosisoffset | INTEGER |
| diagnosisstring | VARCHAR |
| icd9code | VARCHAR |
| diagnosispriority | VARCHAR |

### admissiondx

**Description:** Admission diagnoses

**Row Count:** 626,858

**Columns:** 6

| Column Name | Data Type |
|-------------|-----------|
| admissiondxid | INTEGER |
| patientunitstayid | INTEGER |
| admitdxenteredoffset | INTEGER |
| admitdxpath | VARCHAR |
| admitdxname | VARCHAR |
| admitdxtext | VARCHAR |

### allergy

**Description:** Patient allergies

**Row Count:** 251,949

**Columns:** 13

| Column Name | Data Type |
|-------------|-----------|
| allergyid | INTEGER |
| patientunitstayid | INTEGER |
| allergyoffset | INTEGER |
| allergyenteredoffset | INTEGER |
| allergynotetype | VARCHAR |
| specialtytype | VARCHAR |
| usertype | VARCHAR |
| rxincluded | VARCHAR |
| writtenineicu | VARCHAR |
| drugname | VARCHAR |
| allergytype | VARCHAR |
| allergyname | VARCHAR |
| drughiclseqno | INTEGER |

### pasthistory

**Description:** Past medical history

**Row Count:** 1,149,180

**Columns:** 8

| Column Name | Data Type |
|-------------|-----------|
| pasthistoryid | INTEGER |
| patientunitstayid | INTEGER |
| pasthistoryoffset | INTEGER |
| pasthistoryenteredoffset | INTEGER |
| pasthistorynotetype | VARCHAR |
| pasthistorypath | VARCHAR |
| pasthistoryvalue | VARCHAR |
| pasthistoryvaluetext | VARCHAR |

---

## Medications

### admissiondrug

**Description:** Drugs administered at admission

**Row Count:** 874,920

**Columns:** 14

| Column Name | Data Type |
|-------------|-----------|
| admissiondrugid | INTEGER |
| patientunitstayid | INTEGER |
| drugoffset | INTEGER |
| drugenteredoffset | INTEGER |
| drugnotetype | VARCHAR |
| specialtytype | VARCHAR |
| usertype | VARCHAR |
| rxincluded | VARCHAR |
| writtenineicu | VARCHAR |
| drugname | VARCHAR |
| drugdosage | DECIMAL(11,4) |
| drugunit | VARCHAR |
| drugadmitfrequency | VARCHAR |
| drughiclseqno | INTEGER |

### infusiondrug

**Description:** Infusion drug administration records

**Row Count:** 4,803,719

**Columns:** 9

| Column Name | Data Type |
|-------------|-----------|
| infusiondrugid | INTEGER |
| patientunitstayid | INTEGER |
| infusionoffset | INTEGER |
| drugname | VARCHAR |
| drugrate | VARCHAR |
| infusionrate | VARCHAR |
| drugamount | VARCHAR |
| volumeoffluid | VARCHAR |
| patientweight | VARCHAR |

### medication

**Description:** Medication administration records

**Row Count:** 7,301,853

**Columns:** 15

| Column Name | Data Type |
|-------------|-----------|
| medicationid | INTEGER |
| patientunitstayid | INTEGER |
| drugorderoffset | INTEGER |
| drugstartoffset | INTEGER |
| drugivadmixture | VARCHAR |
| drugordercancelled | VARCHAR |
| drugname | VARCHAR |
| drughiclseqno | INTEGER |
| dosage | VARCHAR |
| routeadmin | VARCHAR |
| frequency | VARCHAR |
| loadingdose | VARCHAR |
| prn | VARCHAR |
| drugstopoffset | INTEGER |
| gtc | INTEGER |

---

## APACHE Scoring

### apacheapsvar

**Description:** APACHE Acute Physiology Score variables

**Row Count:** 171,177

**Columns:** 26

| Column Name | Data Type |
|-------------|-----------|
| apacheapsvarid | INTEGER |
| patientunitstayid | INTEGER |
| intubated | SMALLINT |
| vent | SMALLINT |
| dialysis | SMALLINT |
| eyes | SMALLINT |
| motor | SMALLINT |
| verbal | SMALLINT |
| meds | SMALLINT |
| urine | DOUBLE |
| wbc | DOUBLE |
| temperature | DOUBLE |
| respiratoryrate | DOUBLE |
| sodium | DOUBLE |
| heartrate | DOUBLE |
| meanbp | DOUBLE |
| ph | DOUBLE |
| hematocrit | DOUBLE |
| creatinine | DOUBLE |
| albumin | DOUBLE |
| pao2 | DOUBLE |
| pco2 | DOUBLE |
| bun | DOUBLE |
| glucose | DOUBLE |
| bilirubin | DOUBLE |
| fio2 | DOUBLE |

### apachepatientresult

**Description:** APACHE patient results and predictions

**Row Count:** 297,064

**Columns:** 23

| Column Name | Data Type |
|-------------|-----------|
| apachepatientresultsid | INTEGER |
| patientunitstayid | INTEGER |
| physicianspeciality | VARCHAR |
| physicianinterventioncategory | VARCHAR |
| acutephysiologyscore | INTEGER |
| apachescore | INTEGER |
| apacheversion | VARCHAR |
| predictedicumortality | VARCHAR |
| actualicumortality | VARCHAR |
| predictediculos | DOUBLE |
| actualiculos | DOUBLE |
| predictedhospitalmortality | VARCHAR |
| actualhospitalmortality | VARCHAR |
| predictedhospitallos | DOUBLE |
| actualhospitallos | DOUBLE |
| preopmi | INTEGER |
| preopcardiaccath | INTEGER |
| ptcawithin24h | INTEGER |
| unabridgedunitlos | DOUBLE |
| unabridgedhosplos | DOUBLE |
| actualventdays | DOUBLE |
| predventdays | DOUBLE |
| unabridgedactualventdays | DOUBLE |

### apachepredvar

**Description:** APACHE predictor variables

**Row Count:** 171,177

**Columns:** 51

| Column Name | Data Type |
|-------------|-----------|
| apachepredvarid | INTEGER |
| patientunitstayid | INTEGER |
| sicuday | SMALLINT |
| saps3day1 | SMALLINT |
| saps3today | SMALLINT |
| saps3yesterday | SMALLINT |
| gender | SMALLINT |
| teachtype | SMALLINT |
| region | SMALLINT |
| bedcount | SMALLINT |
| admitsource | SMALLINT |
| graftcount | SMALLINT |
| meds | SMALLINT |
| verbal | SMALLINT |
| motor | SMALLINT |
| eyes | SMALLINT |
| age | SMALLINT |
| admitdiagnosis | VARCHAR |
| thrombolytics | SMALLINT |
| diedinhospital | SMALLINT |
| aids | SMALLINT |
| hepaticfailure | SMALLINT |
| lymphoma | SMALLINT |
| metastaticcancer | SMALLINT |
| leukemia | SMALLINT |
| immunosuppression | SMALLINT |
| cirrhosis | SMALLINT |
| electivesurgery | SMALLINT |
| activetx | SMALLINT |
| readmit | SMALLINT |
| ima | SMALLINT |
| midur | SMALLINT |
| ventday1 | SMALLINT |
| oobventday1 | SMALLINT |
| oobintubday1 | SMALLINT |
| diabetes | SMALLINT |
| managementsystem | SMALLINT |
| var03hspxlos | DOUBLE |
| pao2 | DOUBLE |
| fio2 | DOUBLE |
| ejectfx | DOUBLE |
| creatinine | DOUBLE |
| dischargelocation | SMALLINT |
| visitnumber | SMALLINT |
| amilocation | SMALLINT |
| day1meds | SMALLINT |
| day1verbal | SMALLINT |
| day1motor | SMALLINT |
| day1eyes | SMALLINT |
| day1pao2 | DOUBLE |
| day1fio2 | DOUBLE |

---

## Care Planning

### careplancareprovider

**Description:** Care plan provider information

**Row Count:** 502,765

**Columns:** 8

| Column Name | Data Type |
|-------------|-----------|
| cplcareprovderid | INTEGER |
| patientunitstayid | INTEGER |
| careprovidersaveoffset | INTEGER |
| providertype | VARCHAR |
| specialty | VARCHAR |
| interventioncategory | VARCHAR |
| managingphysician | VARCHAR |
| activeupondischarge | VARCHAR |

### careplaneol

**Description:** End-of-life care plans

**Row Count:** 1,433

**Columns:** 5

| Column Name | Data Type |
|-------------|-----------|
| cpleolid | INTEGER |
| patientunitstayid | INTEGER |
| cpleolsaveoffset | INTEGER |
| cpleoldiscussionoffset | INTEGER |
| activeupondischarge | VARCHAR |

### careplangeneral

**Description:** General care plans

**Row Count:** 3,115,018

**Columns:** 6

| Column Name | Data Type |
|-------------|-----------|
| cplgeneralid | INTEGER |
| patientunitstayid | INTEGER |
| activeupondischarge | VARCHAR |
| cplitemoffset | INTEGER |
| cplgroup | VARCHAR |
| cplitemvalue | VARCHAR |

### careplangoal

**Description:** Care plan goals

**Row Count:** 504,139

**Columns:** 7

| Column Name | Data Type |
|-------------|-----------|
| cplgoalid | INTEGER |
| patientunitstayid | INTEGER |
| CPLGOALoffset | INTEGER |
| CPLGOALCATEGORY | VARCHAR |
| CPLGOALVALUE | VARCHAR |
| CPLGOALSTATUS | VARCHAR |
| ACTIVEUPONDISCHARGE | VARCHAR |

### careplaninfectiousdisease

**Description:** Infectious disease care plans

**Row Count:** 8,056

**Columns:** 8

| Column Name | Data Type |
|-------------|-----------|
| cplinfectid | INTEGER |
| patientunitstayid | INTEGER |
| activeupondischarge | VARCHAR |
| cplinfectdiseaseoffset | INTEGER |
| infectdiseasesite | VARCHAR |
| infectdiseaseassessment | VARCHAR |
| responsetotherapy | VARCHAR |
| treatment | VARCHAR |

---

## Nursing Documentation

### NURSEASSESSMENT

**Description:** Nursing assessments

**Row Count:** 15,602,498

**Columns:** 8

| Column Name | Data Type |
|-------------|-----------|
| nurseassessid | INTEGER |
| patientunitstayid | INTEGER |
| NURSEASSESSOFFSET | INTEGER |
| NURSEASSESSENTRYOFFSET | INTEGER |
| CELLATTRIBUTEPATH | VARCHAR |
| CELLLABEL | VARCHAR |
| CELLATTRIBUTE | VARCHAR |
| CELLATTRIBUTEVALUE | VARCHAR |

### NURSECARE

**Description:** Nursing care documentation

**Row Count:** 8,311,132

**Columns:** 8

| Column Name | Data Type |
|-------------|-----------|
| nursecareid | INTEGER |
| patientunitstayid | INTEGER |
| CELLLABEL | VARCHAR |
| NURSECAREOFFSET | INTEGER |
| NURSECAREENTRYOFFSET | INTEGER |
| CELLATTRIBUTEPATH | VARCHAR |
| CELLATTRIBUTE | VARCHAR |
| CELLATTRIBUTEVALUE | VARCHAR |

### NURSECHARTING

**Description:** Nursing charting entries

**Row Count:** 151,604,232

**Columns:** 8

| Column Name | Data Type |
|-------------|-----------|
| nursingchartid | BIGINT |
| patientunitstayid | INTEGER |
| NURSINGCHARTOFFSET | INTEGER |
| NURSINGCHARTENTRYOFFSET | INTEGER |
| NURSINGCHARTCELLTYPECAT | VARCHAR |
| NURSINGCHARTCELLTYPEVALLABEL | VARCHAR |
| NURSINGCHARTCELLTYPEVALNAME | VARCHAR |
| NURSINGCHARTVALUE | VARCHAR |

---

## Respiratory Care

### RESPIRATORYCARE

**Description:** Respiratory care interventions

**Row Count:** 865,381

**Columns:** 34

| Column Name | Data Type |
|-------------|-----------|
| RESPCAREID | INTEGER |
| PATIENTUNITSTAYID | INTEGER |
| RESPCARESTATUSOFFSET | INTEGER |
| CURRENTHISTORYSEQNUM | INTEGER |
| AIRWAYTYPE | VARCHAR |
| AIRWAYSIZE | VARCHAR |
| AIRWAYPOSITION | VARCHAR |
| CUFFPRESSURE | DECIMAL(5,1) |
| VENTSTARTOFFSET | INTEGER |
| VENTENDOFFSET | INTEGER |
| PRIORVENTSTARTOFFSET | INTEGER |
| PRIORVENTENDOFFSET | INTEGER |
| APNEAPARAMS | VARCHAR |
| LOWEXHMVLIMIT | DECIMAL(11,4) |
| HIEXHMVLIMIT | DECIMAL(11,4) |
| LOWEXHTVLIMIT | DECIMAL(11,4) |
| HIPEAKPRESLIMIT | DECIMAL(11,4) |
| LOWPEAKPRESLIMIT | DECIMAL(11,4) |
| HIRESPRATELIMIT | DECIMAL(11,4) |
| LOWRESPRATELIMIT | DECIMAL(11,4) |
| SIGHPRESLIMIT | DECIMAL(11,4) |
| LOWIRONOXLIMIT | DECIMAL(11,4) |
| HIGHIRONOXLIMIT | DECIMAL(11,4) |
| MEANAIRWAYPRESLIMIT | DECIMAL(11,4) |
| PEEPLIMIT | DECIMAL(11,4) |
| CPAPLIMIT | DECIMAL(11,4) |
| SETAPNEAINTERVAL | VARCHAR |
| SETAPNEATV | VARCHAR |
| SETAPNEAIPPEEPHIGH | VARCHAR |
| SETAPNEARR | VARCHAR |
| SETAPNEAPEAKFLOW | VARCHAR |
| SETAPNEAINSPTIME | VARCHAR |
| SETAPNEAIE | VARCHAR |
| SETAPNEAFIO2 | VARCHAR |

### RESPIRATORYCHARTING

**Description:** Respiratory charting data

**Row Count:** 20,168,176

**Columns:** 7

| Column Name | Data Type |
|-------------|-----------|
| RESPCHARTID | INTEGER |
| PATIENTUNITSTAYID | INTEGER |
| RESPCHARTOFFSET | INTEGER |
| RESPCHARTENTRYOFFSET | INTEGER |
| RESPCHARTTYPECAT | VARCHAR |
| RESPCHARTVALUELABEL | VARCHAR |
| RESPCHARTVALUE | VARCHAR |

---

## Other Clinical Data

### treatment

**Description:** Treatment interventions

**Row Count:** 3,688,745

**Columns:** 5

| Column Name | Data Type |
|-------------|-----------|
| treatmentid | INTEGER |
| patientunitstayid | INTEGER |
| treatmentoffset | INTEGER |
| treatmentstring | VARCHAR |
| activeupondischarge | VARCHAR |

### physicalexam

**Description:** Physical examination findings

**Row Count:** 9,212,316

**Columns:** 6

| Column Name | Data Type |
|-------------|-----------|
| physicalexamid | INTEGER |
| patientunitstayid | INTEGER |
| physicalexamoffset | INTEGER |
| physicalexampath | VARCHAR |
| physicalexamvalue | VARCHAR |
| physicalexamtext | VARCHAR |

### intakeoutput

**Description:** Fluid intake and output records

**Row Count:** 12,030,289

**Columns:** 12

| Column Name | Data Type |
|-------------|-----------|
| intakeoutputid | INTEGER |
| patientunitstayid | INTEGER |
| intakeoutputoffset | INTEGER |
| intaketotal | DECIMAL(12,4) |
| outputtotal | DECIMAL(12,4) |
| dialysistotal | DECIMAL(12,4) |
| nettotal | DECIMAL(12,4) |
| intakeoutputentryoffset | INTEGER |
| cellpath | VARCHAR |
| celllabel | VARCHAR |
| cellvaluenumeric | DECIMAL(12,4) |
| cellvaluetext | VARCHAR |

### microlab

**Description:** Microbiology laboratory results

**Row Count:** 16,996

**Columns:** 7

| Column Name | Data Type |
|-------------|-----------|
| microlabid | INTEGER |
| patientunitstayid | INTEGER |
| culturetakenoffset | INTEGER |
| culturesite | VARCHAR |
| organism | VARCHAR |
| antibiotic | VARCHAR |
| sensitivitylevel | VARCHAR |

### note

**Description:** Clinical notes

**Row Count:** 2,254,179

**Columns:** 8

| Column Name | Data Type |
|-------------|-----------|
| NOTEID | INTEGER |
| patientunitstayid | INTEGER |
| NOTEOFFSET | INTEGER |
| NOTEENTEREDOFFSET | INTEGER |
| NOTETYPE | VARCHAR |
| NOTEPATH | VARCHAR |
| NOTEVALUE | VARCHAR |
| NOTETEXT | VARCHAR |

---
