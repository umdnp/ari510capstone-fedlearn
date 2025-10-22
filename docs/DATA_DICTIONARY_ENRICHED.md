# eICU-CRD Data Dictionary (Enriched)

Comprehensive data dictionary for the eICU Collaborative Research Database (eICU-CRD v2.0)

This enriched version includes detailed column metadata including null options, descriptions, key types, and data transformation indicators.

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

## Column Metadata Key

- **PK** = Primary Key
- **FK** = Foreign Key
- **S** = Stored (data stored as entered)
- **C** = Created (system-generated)
- **T** = Transformed (modified before storage)

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

**Purpose:** Contains patient demographics and admission and discharge details for hospital and ICU stays.

**Row Count:** 200,859

**Columns:** 29

**Important Considerations:**
All stays are centered on ICU admission. That is, there is no unitAdmitOffset column: it is 0 for all patientUnitStayID. Note that within a hospital admission, distinct unit stays can be linked by patientHealthSystemStayID. Keep in mind that offsets are still based upon patientUnitStayID, for example:
patientUnitStayID   patientHealthSystemStayID   unitDischargeOffset     hospitalAdmitOffset     hospitalDischargeOffset     Comment
2   800     4320    -5040   10960   The second ICU stay.
10  800     2160    -720    15280   The first ICU stay.

The hospital course for this patient was:

    patient admitted to hospital
    first ICU admission (patientUnitStayID = 10) at 720 minutes after hospital admission (hospitalAdmitOffset = -720)
    first ICU discharge (unitDischargeOffset = 2160) at 720+2160 minutes after hospital admission (unitDischargeOffset - hospitalAdmitOffset = 2160 - (-720) = 2880)
    second ICU admission (patientUnitStayID = 2) at 5040 minutes after hospital admission (hospitalAdmitOffset = -5040)
    second ICU discharge (unitDischargeOffset = 4320) at 9360 minutes after hospital admission (unitDischargeOffset - hospitalAdmitOffset = 4320 - (-5040) = 9360)
    hospital discharge, total length of stay = (10960 - (-5040)) = (15280 - (-720)) = 16000

Note that the first ICU stay has a larger hospitalAdmitOffset, because this stay occurred closer to hospital admission (i.e. it was first). Also note that there is no correlation between patientUnitStayID and the order of patient stays.

There is no systematic method for chronologically ordering patientHealthSystemStayID for the same patient within the same year.
Table columns
Name    Datatype    Null Option     Comment     Is Key  Stored Transformed Created
patientUnitStayID   int     NOT NULL    surrogate key for ICU Stay  PK  C
patientHealthSystemStayID   int     NOT NULL    surrogate key for the patient health system stay (hospital stay)    FK  C
gender  varchar(25)     NULL    gender of the patient: Male, Female, Unknown, Other, NULL       S
age     varchar(10)     NULL    age of the patient in full years. If the patient is over 89 years old specify “> 89” e.g.: 79, 36, 52, “> 89”, etc.         T
ethnicity   varchar(50)     NULL    picklist ethnicity of the patient: Asian, Caucasian, African American, Native American, Hispanic, Other/Unknown, NULL       S
hospitalID  int     NOT NULL    surrogate key for the hospital associated with the patient unit stay        C
wardID  int     NOT NULL    surrogate key for the ward associated with the patient unit stay        C
apacheAdmissionDx   varchar(1000)   NULL    Full path string of admission diagnosis for patients unit stay e.g.: Pulmonary valve surgery, Chest pain, unknown origin, Restrictive lung disease (i.e., Sarcoidosis, pulmonary fibrosis), etc.        S
admissionHeight     decimal(10,2)   NULL    admission height of the patient in cm e.g.: 160.0000, 182.9000, 175.3000, etc.      S
hospitalAdmitTime24     time(0)     NOT NULL    time in 24 hour format of the hospital admit e.g.: “12:45”, “15:30”, “3:45”         T
hospitalAdmitOffset     int     NOT NULL    number of minutes from unit admit time that the patient was admitted to the hospital        C
hospitalAdmitSource     varchar(30)     NULL    location from where the patient was admitted to the hospital e.g.: Direct Admit, Floor, Chest Pain Center. etc.         S
hospitalDischargeYear   smallint    NOT NULL    year of the hospital discharge date         T
hospitalDischargeTime24     time(0)     NOT NULL    time in 24 hour format of when the hospital discharge event occurred e.g.: “12:45”, “15:30”, “3:45”         T
hospitalDischargeOffset     int     NOT NULL    number of minutes from unit admit time that the patient was discharged from the hospital        C
hospitalDischargeLocation   varchar(100)    NULL    Structured list of location where the patient was discharged to from the hospital e.g.: Home, Nursing Home, Death, etc.         S
hospitalDischargeStatus     varchar(10)     NULL    specifies patient’s condition upon leaving the hospital: Alive, Expired, or NULL        S
unitType    varchar(50)     NULL    the picklist unit type of the unit e.g.: MICU,Cardiovascular ICU,SDU/Step down,VICU,Neuro ICU,CCU,Virtual ICU,SICU,ICU,CCU-CTICU,Mobile ICU,CTICU,CSICU,Test ICU,Vent ICU,Burn-Trauma ICU       S
unitAdmitTime24     time(0)     NOT NULL    time in 24 hour format of when the unit admit event occurred e.g.: “12:45”, “15:30”, “3:45”         T
unitAdmitSource     varchar(100)    NULL    picklist location from where the patient was admitted e.g.: Emergency Room, Recovery Room, Direct Admit, etc.       S
unitVisitNumber     int     NOT NULL    identifies the visit number of the patient, i.e. if the patient’s hospital stay has multiple unit stays         C
unitStayType    varchar(15)     NULL    patient’s unit stay type: stepdown/other, readmit for undo, admit, pre-admit, transfer, readmit         S
admissionWeight     decimal(10,2)   NULL    admission weight of the patient in kilograms e.g.: 69.7000, 70.9000, 173.0000, etc.         S
dischargeWeight     decimal(10,2)   NULL    patient weight at time of unit discharge in kilograms e.g.: 69.7000, 70.9000, 173.0000, etc.        S
unitDischargeTime24     time(0)     NOT NULL    time in 24 hour format of when the unit discharge event occurred e.g.: “12:45”, “15:30”, “3:45”         T
unitDischargeOffset     int     NOT NULL    number of minutes from unit admit time that the patient was discharged from the unit        C
unitDischargeLocation   varchar(100)    NULL    Structured list of locations where the patient was discharged to from the unit e.g.: Other ICU (CABG), Other Hospital, Telemetry, Other Internal, Other ICU, Floor, Step-Down Unit (SDU), etc.      S
unitDischargeStatus     varchar(10)     NULL    specifies patient’s condition upon leaving the unit: Alive, Expired, or NULL        S
uniquepid   varchar(10)     NOT NULL    ID for a unique patient.        C


https://eicu-crd.mit.edu/eicutables/patient/

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| patientunitstayid | INTEGER | NOT NULL | PK | C | surrogate key for ICU Stay |
| patienthealthsystemstayid | INTEGER | NOT NULL | FK | C | surrogate key for the patient health system stay (hospital stay) |
| gender | VARCHAR | NULL | S |  | gender of the patient: Male, Female, Unknown, Other, NULL |
| age | VARCHAR | NULL | T |  | age of the patient in full years. If the patient is over 89 years old specify “> 89” e.g.: 79, 36, 52, “> 89”, etc. |
| ethnicity | VARCHAR | NULL | S |  | picklist ethnicity of the patient: Asian, Caucasian, African American, Native American, Hispanic, Other/Unknown, NULL |
| hospitalid | INTEGER | NOT NULL | C |  | surrogate key for the hospital associated with the patient unit stay |
| wardid | INTEGER | NOT NULL | C |  | surrogate key for the ward associated with the patient unit stay |
| apacheadmissiondx | VARCHAR | NULL | S |  | Full path string of admission diagnosis for patients unit stay e.g.: Pulmonary valve surgery, Chest pain, unknown origin, Restrictive lung disease (i.e., Sarcoidosis, pulmonary fibrosis), etc. |
| admissionheight | DECIMAL(10,2) | NULL | S |  | admission height of the patient in cm e.g.: 160.0000, 182.9000, 175.3000, etc. |
| hospitaladmittime24 | VARCHAR | NOT NULL | T |  | time in 24 hour format of the hospital admit e.g.: “12:45”, “15:30”, “3:45” |
| hospitaladmitoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the patient was admitted to the hospital |
| hospitaladmitsource | VARCHAR | NULL | S |  | location from where the patient was admitted to the hospital e.g.: Direct Admit, Floor, Chest Pain Center. etc. |
| hospitaldischargeyear | SMALLINT | NOT NULL | T |  | year of the hospital discharge date |
| hospitaldischargetime24 | VARCHAR | NOT NULL | T |  | time in 24 hour format of when the hospital discharge event occurred e.g.: “12:45”, “15:30”, “3:45” |
| hospitaldischargeoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the patient was discharged from the hospital |
| hospitaldischargelocation | VARCHAR | NULL | S |  | Structured list of location where the patient was discharged to from the hospital e.g.: Home, Nursing Home, Death, etc. |
| hospitaldischargestatus | VARCHAR | NULL | S |  | specifies patient’s condition upon leaving the hospital: Alive, Expired, or NULL |
| unittype | VARCHAR | NULL | S |  | the picklist unit type of the unit e.g.: MICU,Cardiovascular ICU,SDU/Step down,VICU,Neuro ICU,CCU,Virtual ICU,SICU,ICU,CCU-CTICU,Mobile ICU,CTICU,CSICU,Test ICU,Vent ICU,Burn-Trauma ICU |
| unitadmittime24 | VARCHAR | NOT NULL | T |  | time in 24 hour format of when the unit admit event occurred e.g.: “12:45”, “15:30”, “3:45” |
| unitadmitsource | VARCHAR | NULL | S |  | picklist location from where the patient was admitted e.g.: Emergency Room, Recovery Room, Direct Admit, etc. |
| unitvisitnumber | INTEGER | NOT NULL | C |  | identifies the visit number of the patient, i.e. if the patient’s hospital stay has multiple unit stays |
| unitstaytype | VARCHAR | NULL | S |  | patient’s unit stay type: stepdown/other, readmit for undo, admit, pre-admit, transfer, readmit |
| admissionweight | DECIMAL(10,2) | NULL | S |  | admission weight of the patient in kilograms e.g.: 69.7000, 70.9000, 173.0000, etc. |
| dischargeweight | DECIMAL(10,2) | NULL | S |  | patient weight at time of unit discharge in kilograms e.g.: 69.7000, 70.9000, 173.0000, etc. |
| unitdischargetime24 | VARCHAR | NOT NULL | T |  | time in 24 hour format of when the unit discharge event occurred e.g.: “12:45”, “15:30”, “3:45” |
| unitdischargeoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the patient was discharged from the unit |
| unitdischargelocation | VARCHAR | NULL | S |  | Structured list of locations where the patient was discharged to from the unit e.g.: Other ICU (CABG), Other Hospital, Telemetry, Other Internal, Other ICU, Floor, Step-Down Unit (SDU), etc. |
| unitdischargestatus | VARCHAR | NULL | S |  | specifies patient’s condition upon leaving the unit: Alive, Expired, or NULL |
| uniquepid | VARCHAR | NOT NULL | C |  | ID for a unique patient. |

### hospital

**Description:** Hospital characteristics and metadata

**Purpose:** The hospital table contains details of hospitals covered by the the eICU telehealth program.

**Row Count:** 208

**Columns:** 4

**Important Considerations:**
The data was collected by self-reported survey.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| hospitalid | INTEGER | NOT NULL | PK | S | surrogate key for the hospital |
| numbedscategory | VARCHAR | number of beds |  |  | S |
| teachingstatus | BOOLEAN | teaching status of hospital |  |  | S |
| region | VARCHAR | region of hospital |  |  | S |

---

## Clinical Measurements

### lab

**Description:** Laboratory test results (~160 standardized measurements)

**Purpose:** Laboratory tests that have have been mapped to a standard set of measurements. Unmapped measurements are recorded in the customLab table.

**Row Count:** 39,132,531

**Columns:** 10

**Important Considerations:**
It is possible some rarely obtained lab measurements are not interfaced into the system and therefore will not be available in the database. Absence of a rare lab measurement, such as serum lidocaine concentrations, would not indicate the lab was not drawn. However, absence of a platelet count would indicate the value was not obtained.
Table columns
Name    Datatype    Null Option     Comment     Is Key  Stored Transformed Created
patientUnitStayID   int     NOT NULL    foreign key link to the patient table   FK  C
labID   int     IDENTITY    surrogate ID for the labs data  PK  C
labResultOffset     int     NOT NULL    number of minutes from unit admit time that the lab value was drawn         C
labTypeID   tinyint     NOT NULL    the type of lab that is represented in the values, 1 for chemistry, 2 for drug level, 3 for hemo, 4 for misc, 5 for non-mapped, 6 for sensitive, 7 for ABG lab      S
labName     varchar(255)    NULL    the picklist name of the lab e.g.: CPK, troponin - I, RBC, HCO3, Total CO2, etc. This is hospital specific.         S
labResult   decimal(11,4)   NULL    the numeric value of the lab e.g.: 7.3230,, 58.0000, 24.8000        S
labResultText   varchar(255)    NULL    the text of the lab value e.g.: 7.257, 58.0 24.8        S
labMeasureNameSystem    varchar(255)    NULL    the measurement name of the lab e.g.: mm Hg, mmol/L, mEq/L, etc.        S
labMeasureNameInterface     varchar(255)    NULL    the measurement name of the lab from interfaces e.g.: mm Hg, mmol/L, mEq/L, etc.        S
labResultRevisedOffset  int     NOT NULL    number of minutes from unit admit time that the revised lab value was entered       C


https://eicu-crd.mit.edu/eicutables/lab/

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| labid | INTEGER | IDENTITY | PK | C | surrogate ID for the labs data |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| labresultoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the lab value was drawn |
| labtypeid | DECIMAL(3,0) | NOT NULL | S |  | the type of lab that is represented in the values, 1 for chemistry, 2 for drug level, 3 for hemo, 4 for misc, 5 for non-mapped, 6 for sensitive, 7 for ABG lab |
| labname | VARCHAR | NULL | S |  | the picklist name of the lab e.g.: CPK, troponin - I, RBC, HCO3, Total CO2, etc. This is hospital specific. |
| labresult | DECIMAL(11,4) | NULL | S |  | the numeric value of the lab e.g.: 7.3230,, 58.0000, 24.8000 |
| labresulttext | VARCHAR | NULL | S |  | the text of the lab value e.g.: 7.257, 58.0 24.8 |
| labmeasurenamesystem | VARCHAR | NULL | S |  | the measurement name of the lab e.g.: mm Hg, mmol/L, mEq/L, etc. |
| labmeasurenameinterface | VARCHAR | NULL | S |  | the measurement name of the lab from interfaces e.g.: mm Hg, mmol/L, mEq/L, etc. |
| labresultrevisedoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the revised lab value was entered |

### customlab

**Description:** Non-standard laboratory measurements

**Purpose:** Standardized labs are included in the ‘lab’ table. Laboratory measurements that are not configured within the standard interface (for example, unmapped tests) are included in the customLab table.

**Row Count:** 1,082

**Columns:** 7

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| customlabid | INTEGER | not null |  |  | PK |
| patientunitstayid | INTEGER | not null |  |  | FK |
| labotheroffset | INTEGER | not null |  |  |  |
| labothertypeid | INTEGER | not null |  |  |  |
| labothername | VARCHAR |  |  |  |  |
| labotherresult | VARCHAR |  |  |  |  |
| labothervaluetext | VARCHAR |  |  |  |  |

### vitalaperiodic

**Description:** Aperiodic (intermittent) vital signs

**Purpose:** The vitalAperiodic table provides invasive vital sign data which is interfaced into eCareManager at irregular intervals.

**Row Count:** 25,075,074

**Columns:** 13

**Important Considerations:**
The following vital signs are referred to as aperiodic vital signs, as they are not captured by the system on a regular basis (non-invasive BP can be triggered at an unpredictable variety of time intervals):

    Cardiac output
    Cardiac Index
    Pulmonary artery occlusion pressure (“wedge pressure” - PAOP)
    SVR / SVRI
    PVR / PVRI
    Non-invasive blood pressure

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| vitalaperiodicid | INTEGER | IDENTITY | PK | C | surrogate key for the aperiodic value |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| observationoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the aperiodic value was entered |
| noninvasivesystolic | DOUBLE | NULL | S |  | patient’s non invasive systolic value e.g.: 78, 102, 87, etc. |
| noninvasivediastolic | DOUBLE | NULL | S |  | patient’s non invasive diastolic value e.g.: 40, 59, 49, etc. |
| noninvasivemean | DOUBLE | NULL | S |  | patient’s non invasive mean value e.g.: 56, 76, 65, etc. |
| paop | DOUBLE | NULL | S |  | patient’s paop value e.g.: 20, 18, 15, etc. |
| cardiacoutput | DOUBLE | NULL | S |  | patient cardiac output value e.g.: 4.71, 5.81, 5.63, etc. |
| cardiacinput | DOUBLE | NULL | S |  | patient cardiac input value e.g.: |
| svr | DOUBLE | NULL | S |  | patient svr value e.g.: |
| svri | DOUBLE | NULL | S |  | patient svri value e.g.: |
| pvr | DOUBLE | NULL | S |  | patient pvr value e.g.: |
| pvri | DOUBLE | NULL | S |  | patient pvri value e.g.: |

### vitalperiodic

**Description:** Periodic (continuous) vital signs monitoring

**Row Count:** 146,671,642

**Columns:** 19

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| vitalperiodicid | BIGINT |  |  |  |  |
| patientunitstayid | INTEGER |  |  |  |  |
| observationoffset | INTEGER |  |  |  |  |
| temperature | DECIMAL(11,4) |  |  |  |  |
| sao2 | INTEGER |  |  |  |  |
| heartrate | INTEGER |  |  |  |  |
| respiration | INTEGER |  |  |  |  |
| cvp | INTEGER |  |  |  |  |
| etco2 | INTEGER |  |  |  |  |
| systemicsystolic | INTEGER |  |  |  |  |
| systemicdiastolic | INTEGER |  |  |  |  |
| systemicmean | INTEGER |  |  |  |  |
| pasystolic | INTEGER |  |  |  |  |
| padiastolic | INTEGER |  |  |  |  |
| pamean | INTEGER |  |  |  |  |
| st1 | DOUBLE |  |  |  |  |
| st2 | DOUBLE |  |  |  |  |
| st3 | DOUBLE |  |  |  |  |
| icp | INTEGER |  |  |  |  |

---

## Diagnoses and Conditions

### diagnosis

**Description:** Patient diagnoses and conditions

**Purpose:** Patient diagnosis recorded in the active diagnosis table. Sequence does indicate relative severity. diagnosisPriority is not required.

**Row Count:** 2,710,672

**Columns:** 7

**Important Considerations:**
The diagnosis.med table contains diagnoses that were documented in the ICU stay by clinical staff and may or may not be consistent with diagnoses that were coded and used for professional billing or hospital reimbursment purposes. This table does not include diagnoses that may have been documented prior to or after the ICU stay. This table does not indicate which diagnoses were resolved or ruled-out nor does it provide a diagnosis time frame when/if a diagnosis was removed.

    To follow.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| diagnosisid | INTEGER | IDENTITY | PK | C | surrogate key for the diagnosis |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| activeupondischarge | VARCHAR | NULL | S |  | denotes whether the diagnosis was active upon discharge from the unit: True or False |
| diagnosisoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the diagnosis was entered |
| diagnosisstring | VARCHAR | NOT NULL | symbol e.g.: pulmonary | disorders of the airways | the full pathstring of the diagnosis selected in eCareManager, the sections of the diagnosis will be separated by a |
| icd9code | VARCHAR | NOTNULL | S |  | ICD-9 code for the diagnosis e.g.: 518.81, 537.9, 491.20, etc. |
| diagnosispriority | VARCHAR | NOT NULL | S |  | picklist value which denotes whether the diagnosis was marked as: Primary, Major, or Other |

### admissiondx

**Description:** Admission diagnoses

**Purpose:** The admissiondx table contains the primary diagnosis for admission to the ICU per the APACHE scoring criteria. Entered in the patient note forms. After a fixed period from admission has passed, the table cannot be updated by the caregiver.

**Row Count:** 626,858

**Columns:** 6

**Important Considerations:**
Patients admission source (medical, surgical) drives the APACHE diagnosis.
    Present for the majority of patients.
    If a patient does not have an admissiondx entry, they should not have an APACHE score.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| admissiondxid | INTEGER | IDENTITY | PK | C | surrogate key for the admission diagnosis |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| admitdxenteredoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the admission diagnosis was entered |
| admitdxpath | VARCHAR | NOT NULL | All |  | the admission diagnosis' item’s full path e.g.: admission diagnosis |
| admitdxname | VARCHAR | NULL | S |  | admission diagnosis' item’s name e.g.: Angina, stable (asymp or stable pattern of symptoms w/meds) |
| admitdxtext | VARCHAR | NULL | S |  | admission diagnosis amplifying value e.g.: 42, 50 |

### allergy

**Description:** Patient allergies

**Purpose:** The allergy tables contains details of patient allergies. The data is entered in the patient note forms.

**Row Count:** 251,949

**Columns:** 13

**Important Considerations:**
The absence of observation does not indicate an absence of allergy.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| allergyid | INTEGER | IDENTITY | PK | C | surrogate key for the allergy |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| allergyoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the allergy was detected |
| allergyenteredoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the allergy was entered |
| allergynotetype | VARCHAR | NOT NULL | S |  | unique note picklist types e.g.: Comprehensive Progress Admission Intubation |
| specialtytype | VARCHAR | NOT NULL | S |  | physician specialty picklist types e.g.: anesthesiology gastroenterology oncology |
| usertype | VARCHAR | NULL | S |  | eCareManager user picklist types e.g.: eICU Physician Nurse Attending Physician |
| rxincluded | VARCHAR | NOT NULL | S |  | Does the Note have associated Rx data: True or False |
| writtenineicu | VARCHAR | NOT NULL | S |  | Was the Note written in the eICU: True or False |
| drugname | VARCHAR | NULL | S |  | name of the selected admission drug e.g.: POTASSIUM CHLORIDE/D5NS METAXALONE PRAVACHOL |
| allergytype | VARCHAR | NOT NULL | S |  | type of allergy: Drug or Non Drug |
| allergyname | VARCHAR | NOT NULL | S |  | allergy picklist name e.g.: penicillins pollen shellfish |
| drughiclseqno | INTEGER | NULL | S |  | HICL sequence number for the drug if drug allergy e.g.: 2734, 33199, 20492 |

### pasthistory

**Description:** Past medical history

**Purpose:** Provides information related a patient’s relevant past medical history.

**Row Count:** 1,149,180

**Columns:** 8

**Important Considerations:**
Providing detailed Past History is not common, but items such as AIDS, Cirrhosis of the Liver, Hepatic Failure, Chronic Renal Failure, Transplant, and Pre-existing Cancers / immunosuppression are more reliable because of their importance in severity outcome scoring.
Table columns
Name    Datatype    Null Option     Comment     Is Key  Stored Transformed Created
pastHistoryID   int     IDENTITY    surrogate key for the past history item     PK  C
patientUnitStayID   int     NOT NULL    foreign key link to the patient table   FK  C
pastHistoryOffset   int     NOT NULL    number of minutes from unit admit time for the past history item        C
pastHistoryEnteredOffset    int     NOT NULL    number of minutes from unit admit time that the past history item was entered       C
pastHistoryNoteType     varchar(20)     NULL    note type for the past history item e.g.: Admission, Initial Consultation/Other, Re-Admission, etc.         S
pastHistoryPath     varchar(255)    NOT NULL    the root path of the past history item e.g.: notes/Progress Notes/Past History/Organ Systems/Hematology/Oncology (A)/Cancer Therapy/Chemotherapy/Cis-platinum, etc.         S
pastHistoryValue    varchar(100)    NULL    Structured picklist of available past history items e.g.: Performed, hypercoagulable condition, COPD - no limitations, etc.         S
pastHistoryValueText    varchar(255)    NULL    the picklist value of the past history item e.g.: COPD - Moderate, CHF, Medication dependent, etc.      S

Detailed description

Data include Past History date/time (as offset), note type, root path (e.g. notes/Progress Notes/Past History/Organ Systems/Hematology/Oncology (A)/Cancer Therapy/Chemotherapy/Cis-platinum, etc.), picklist values (e.g. Performed, Not Performed, Not Obtainable, No Health Problems, etc.) and text (e.g. COPD - Moderate, CHF, Medication dependent). Data entry fields are organized by the following organ systems: • Neurologic • Cardiovascular • Pulmonary • Gastrointestinal • Infectious Disease • Hematology/Oncology • Endocrine • Rheumatic


https://eicu-crd.mit.edu/eicutables/pasthistory/

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| pasthistoryid | INTEGER | IDENTITY | PK | C | surrogate key for the past history item |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| pasthistoryoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time for the past history item |
| pasthistoryenteredoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the past history item was entered |
| pasthistorynotetype | VARCHAR | NULL | S |  | note type for the past history item e.g.: Admission, Initial Consultation/Other, Re-Admission, etc. |
| pasthistorypath | VARCHAR | NOT NULL | S |  | the root path of the past history item e.g.: notes/Progress Notes/Past History/Organ Systems/Hematology/Oncology (A)/Cancer Therapy/Chemotherapy/Cis-platinum, etc. |
| pasthistoryvalue | VARCHAR | NULL | S |  | Structured picklist of available past history items e.g.: Performed, hypercoagulable condition, COPD - no limitations, etc. |
| pasthistoryvaluetext | VARCHAR | NULL | S |  | the picklist value of the past history item e.g.: COPD - Moderate, CHF, Medication dependent, etc. |

---

## Medications

### admissiondrug

**Description:** Drugs administered at admission

**Row Count:** 874,920

**Columns:** 14

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| admissiondrugid | INTEGER |  |  |  |  |
| patientunitstayid | INTEGER |  |  |  |  |
| drugoffset | INTEGER |  |  |  |  |
| drugenteredoffset | INTEGER |  |  |  |  |
| drugnotetype | VARCHAR |  |  |  |  |
| specialtytype | VARCHAR |  |  |  |  |
| usertype | VARCHAR |  |  |  |  |
| rxincluded | VARCHAR |  |  |  |  |
| writtenineicu | VARCHAR |  |  |  |  |
| drugname | VARCHAR |  |  |  |  |
| drugdosage | DECIMAL(11,4) |  |  |  |  |
| drugunit | VARCHAR |  |  |  |  |
| drugadmitfrequency | VARCHAR |  |  |  |  |
| drughiclseqno | INTEGER |  |  |  |  |

### infusiondrug

**Description:** Infusion drug administration records

**Purpose:** Details of drug infusions. Entered from the nursing flowsheet (either manually or interfaced from the hospital electronic health record system).

**Row Count:** 4,803,719

**Columns:** 9

**Important Considerations:**
Infusion drugs entered directly into the source system (eCareManager) by clinicians must include the concentration of the drug being infused. This is done by entering the “drugAmount” and “volumeOfFluid” and this is independent of the amount being infused (drugRate or infusionRate). Interfaced values from source EMRs may not contain the concentration.
    Many EHRs will only interface out the infusion rate so you may only get the mL/hr and it may be difficult to get the actual drug rate unless it’s a standard concentration drug like 10% propofol. The exact drug name and concentration may be present in the medication table to verify concentration.

Let’s take an example row:
infusiondrugid  drugname    drugrate    infusionrate    drugamount  volumeoffluid
2001050     Nitroglycerin (mcg/min)     10  3   50  250

    Concentration will generally be charted in mg and ml. So for this patient with a drugamount = 50 and a volumeoffluid = 250, the administration is from a 50 mg/250 mL bottle of the drug.
    Infusion rate is generally charted as ml/hr. So this patient is receiving 3ml/hr of 50mg/mL of NTG.
    Drug rate units should be specified and should match the calculation obtained from the infusion rate * concentration (which this does once you convert mg to mcg).

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| infusiondrugid | INTEGER | IDENTITY | PK | C | surrogate key for infusion drugs |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| infusionoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that infusion drug column was entered |
| drugname | VARCHAR | NOT NULL | S |  | picklist name of the infusion drug e.g.: Heparin (units/hr), Vasopressin (units/min), Propofol (mcg/kg/min), etc. |
| drugrate | VARCHAR | NULL | S |  | rate of the infusion drug e.g.: 1300, .7, 0.49, etc. |
| infusionrate | VARCHAR | NULL | S |  | infusion rate of the drug e.g.: 13, 1.25, 25000, etc. |
| drugamount | VARCHAR | NULL | S |  | the amount of drug given e.g.: 250, 100, 50, etc. |
| volumeoffluid | VARCHAR | NULL | S |  | volume of fluid for the infusion e.g.: 250, 100, 50, etc. |
| patientweight | VARCHAR | NULL | S |  | the patient weight recorded during the drug infusion in kilograms e.g.: 87.9, 76.3, 65.8, etc. |

### medication

**Description:** Medication administration records

**Purpose:** The medications table reflects the active medication orders for patients. These are orders but do not necessarily reflect administration to the patient. Titration of continuous infusion medications can be obtained in the infusionDrug table.

**Row Count:** 7,301,853

**Columns:** 15

**Important Considerations:**
The majority of hospitals have an HL7 medication interface system in place which automatically synchronizes the orders with eCareManager as they are verified by the pharmacist in the source pharmacy system. For hospitals without a medication interface, the eICU staff may enter a selection of medications to facilitate population management and completeness for reporting purposes.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| medicationid | INTEGER | IDENTITY | PK | C | surrogate key for drugs |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| drugorderoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the drug was ordered |
| drugstartoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the drug was started |
| drugivadmixture | VARCHAR | NOT NULL | S |  | contains “Yes” if an IV admixture, “No” otherwise |
| drugordercancelled | VARCHAR | NOT NULL | S |  | contains “Yes” if drug order was cancelled, “No” otherwise |
| drugname | VARCHAR | NOT NULL | S |  | name of selected drug e.g.: SODIUM CHLORIDE 0.9%, ONDANSETRON HCL, MORPHINE SULFATE, etc. |
| drughiclseqno | INTEGER | NULL | S |  | HICL for the drug e.g.: 8255, 6055, 1694, etc. |
| dosage | VARCHAR | NOT NULL | S |  | the dosage of the drug e.g.: 500 ml, 1 mcg/kg/min, 2.4 units/hour, etc. |
| routeadmin | VARCHAR | NOT NULL | S |  | the picklist route of administration for the drug e.g.: IV (intravenous), IV - continuous infusion (intravenous), PO (oral), etc. |
| frequency | VARCHAR | NOT NULL | S |  | the picklist frequency with which the drug is taken e.g.: Every 6 hour(s), twice a day, four times per day, etc. |
| loadingdose | VARCHAR | NOT NULL | S |  | the loading dose of the drug e.g.: 0 mg, 2 mg, 2 units, etc. |
| prn | VARCHAR | NOT NULL | S |  | denotes whether the medication was PRN or not: Yes, No, or BLANK |
| drugstopoffset | INTEGER | NULL | C |  | number of minutes from unit admit time that the drug was stopped |
| gtc | INTEGER | NULL | S |  | The NDDF GTC code associated with the drug |

---

## APACHE Scoring

### apacheapsvar

**Description:** APACHE Acute Physiology Score variables

**Purpose:** Contains the variables used to calculate the Acute Physiology Score (APS) III for patients. APS-III is an established method of summarizing patient severity of illness on admission to the ICU, and is a part of the Acute Physiology Age Chronic Health Evaluation (APACHE) system of equations for predicting outcomes for ICU patients.

**Row Count:** 171,177

**Columns:** 26

**Important Considerations:**
Acute Physiology Age Chronic Health Evaluation (APACHE) consists of a groups of equations used for predicting outcomes in critically ill patients.

    APACHE II, III and IV are based on the APS or acute physiology score (which uses 12 physiologic values), age, and chronic health status within one of 56 disease groups. APACHE II is no longer considered valid due to inadequate case mix index adjustments and over estimates mortality because it is based on models from the 1970s-1980s.

    APS points are assigned based upon the “Worst” values (measurement of the degree of physiologic derangement) that a patient exhibits during the APACHE Day. The “Worst” values tend to be those that are furthest away from the APACHE-defined mid-point.

    APACHE III, introduced in 1991, improved the equation by changing the number and weights of the APS and revising the measurement of chronic health status. The APACHE day refers to the time period in which clinical variables can be used in the algorithms.

    APACHE IVa further improved the equations and has been described as having the highest discrimination of any other adult risk adjustment model (SAPS 3, SOFA, MPM III).

    APACHE defines hospital mortality by an admission. discharge, transfer (ADT) hospital disposition as “expired” or “dead”. ICU mortality is defined as a unit dispostion in the ADT system as “expired” or “dead”. Some patients will have more than one ICU admission. For each ICU admission the patient will have a disposition of either dead (expired) or alive.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| apacheapsvarid | INTEGER | IDENTITY | PK | S | surrogate key for APACHE APS (input) variables |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| intubated | SMALLINT | NULL | S |  | set to 0 when not populated; set to 1 when the patient is intubated at the time of the worst ABG result |
| vent | SMALLINT | NULL | S |  | set to 0 when not populated; set to 1 when the patient is ventilated at the time of the worst respiratory rate |
| dialysis | SMALLINT | NULL | S |  | set to 0 when not populated; set to 1 when it is indicated that the patient is on dialysis |
| eyes | SMALLINT | NULL | S |  | set to NULL when not populated; set to 0 when meds field below is 1 (no GCS score); set to the value of the APACHE API’s eyes value in the worst GCS data set when the patient has a valid GCS score; range from 1 to 4 |
| motor | SMALLINT | NULL | S |  | set to NULL when not populated; set to 0 when meds field below is 1 (no GCS score); set to the value of the APACHE API’s motor value in the worst GCS data set when the patient has a valid GCS score; range from 1 to 6 |
| verbal | SMALLINT | NULL | S |  | set to NULL when not populated; set to 0 when meds field below is 1 (no GCS score); set to the value of the APACHE API’s verbal value in the worst GCS data set when the patient has a valid GCS score; range from 1 to 5 |
| meds | SMALLINT | NULL | S |  | set to NULL when not populated; set to 1 when “unable to score due to meds” is selected and no GCS score is available for the APACHE day; set to 0 when “unable to score due to meds” is not selected and a valid GCS score is set |
| urine | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s summed 24 hour urine output value when present |
| wbc | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst WBC (white blood count) lab value when present |
| temperature | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst Celsius temperature value when present |
| respiratoryrate | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst respiratory rate value when present |
| sodium | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst sodium lab value when present |
| heartrate | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst heart rate value when present |
| meanbp | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst mean blood pressure value when present |
| ph | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s pH value for the worst ABG data set when present |
| hematocrit | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst Hct lab value when present |
| creatinine | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst creatinine lab value when present |
| albumin | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst albumin lab value when present |
| pao2 | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s PaO2 value for the worst ABG data set when present |
| pco2 | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s paCO2 value for the worst ABG data set when present |
| bun | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst BUN lab value when present |
| glucose | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst glucose lab value when present |
| bilirubin | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s worst bilirubin lab value when present |
| fio2 | DOUBLE | NULL | S |  | set to NULL when not present; set to the APACHE API’s FiO2 value for the worst ABG data set when present |

### apachepatientresult

**Description:** APACHE patient results and predictions

**Purpose:** Provides predictions made by the APACHE score (versions IV and IVa), including probability of mortality, length of stay, and ventilation days.

**Row Count:** 297,064

**Columns:** 23

**Important Considerations:**
APACHE defines actual hospital mortality by an admission, discharge, transfer (ADT) hospital disposition as “expired” or “dead”. ICU mortality is defined as a unit dispostion in the ADT system as “expired” or “dead”. Some patients will have more than one ICU admission. For each ICU admission the patient will have a disposition of either dead (expired) or alive.
    Predicted mortality is the percent risk of death for an individual patient. This is displayed as decimal. The sum of every patient’s risk of death within the population of interest equals the number of deaths predicted in that population.
    APACHE ICU length of stay refers to the number of days and partial days that a patient was in an ICU. Hospital LOS represents the total number of days and partial days that a patient was in the hospital during a unique hospitalization.
    Patients with an ICU stay less than 4 hours, most transplant patients, burn patients, and patients less than sixteen years of age will be classified as non-predictive.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| apachepatientresultsid | INTEGER |  |  |  |  |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| physicianspeciality | VARCHAR | NULL | S |  | Physician Specialty picklist value |
| physicianinterventioncategory | VARCHAR | NULL | S |  | Physician Intervention Category picklist value |
| acutephysiologyscore | INTEGER | NULL | S |  | Acute Physiology Score from Apache API |
| apachescore | INTEGER | NULL | S |  | Apache Score. Calculated from acutePhysiologyScore |
| apacheversion | VARCHAR | NOT NULL | S |  | The version of the APACHE algorithm used to produce the apacheScore (e.g 3, 4) |
| predictedicumortality | VARCHAR | NULL | S |  | Predicted ICU Mortality from Apache API |
| actualicumortality | VARCHAR | NULL | S |  | Actual ICU Mortality |
| predictediculos | DOUBLE | NULL | S |  | Predicted ICU Length of Stay from Apache API |
| actualiculos | DOUBLE | NULL | S |  | Actual ICU Length of Stay |
| predictedhospitalmortality | VARCHAR | NULL | S |  | Predicted Hospital Mortality from Apache API |
| actualhospitalmortality | VARCHAR | NULL | S |  | Actual Hospital Mortality |
| predictedhospitallos | DOUBLE | NULL | S |  | Predicted Hospital Length of Stay from Apache API |
| actualhospitallos | DOUBLE | NULL | S |  | Actual Hospital Length of Stay. Value is 50 when when > 50 days. |
| preopmi | INTEGER | NULL | S |  | Indicates if patient has pre –Operative Myocardial Infarction |
| preopcardiaccath | INTEGER | NULL | S |  | Indicates if patient has pre –Operative cardiac catheterization |
| ptcawithin24h | INTEGER | NULL | S |  | 0/1. 1- Patient had PTCA with 24 hrs |
| unabridgedunitlos | DOUBLE | NULL | S |  | Actual ICU Length of stay |
| unabridgedhosplos | DOUBLE | NULL | S |  | Actual Hospital Length of stay |
| actualventdays | DOUBLE | NULL | S |  | Actual Ventilation days. Value is 30 when Actual Ventilation > 30 |
| predventdays | DOUBLE | NULL | S |  | Predicted ventilation days from Apache API |
| unabridgedactualventdays | DOUBLE | NULL | S |  | Actual Ventilation days |

### apachepredvar

**Description:** APACHE predictor variables

**Purpose:** Provides variables underlying the APACHE predictions. Acute Physiology Age Chronic Health Evaluation (APACHE) consists of a groups of equations used for predicting outcomes in critically ill patients. APACHE II is based on the APS or acute physiology score (which uses 12 physiologic values), age, and chronic health status within one of 56 disease groups. APACHE II is no longer considered valid due to inadequate case mix index adjustments and over estimates mortality because it is based on models from the 1970s-1980s. APACHE III, introduced in 1991, improved the equation by changing the number and weights of the APS and revising the measurement of chronic health status. APACHE IVa further improved the equations and has been described as having the highest discrimination of any other adult risk adjustment model (SAPS 3, SOFA, MPM III).

**Row Count:** 171,177

**Columns:** 51

**Important Considerations:**
oOBVentDay1 and oOBIntubDay1
        if a patient is intubated on day 1 they are mechanically ventilated
        if a patient is ventilated on day 1, but not intubated, they are non-invasively ventilated

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| apachepredvarid | INTEGER | NOT NULL | PK | S | surrogate key for the APACHE Prediction variables |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| sicuday | SMALLINT | NULL | S |  | set to default value 1 |
| saps3day1 | SMALLINT | NULL | S |  | set to default value 0 |
| saps3today | SMALLINT | NULL | S |  | set to default value 0 |
| saps3yesterday | SMALLINT | NULL | S |  | set to default value 0 |
| gender | SMALLINT | NULL | S |  | Female =1, Male = 0 , Not available =-1 |
| teachtype | SMALLINT | NULL | S |  | Set to default value of 0 |
| region | SMALLINT | NULL | S |  | Set to default value of 3 |
| bedcount | SMALLINT | NULL | XxX | XXX | XXX |
| admitsource | SMALLINT | NULL | S |  | Number indicating admit Source for a unit (1 to 8) |
| graftcount | SMALLINT | NULL | S |  | Number selected for the patient when a CABG admission diagnosis is selected for the patient in eCare. Default is 3 |
| meds | SMALLINT | NULL | S |  | 0 when ‘unable to score due to meds’ is not selected in eCare or there are valid GCS values. 1 when ‘unable to score due to meds’ is selected in eCare. -1 when no meds info is available |
| verbal | SMALLINT | NULL | S |  | GCS verbal score from worst GCS set |
| motor | SMALLINT | NULL | S |  | GCS motor score from worst GCS set |
| eyes | SMALLINT | NULL | S |  | GCS eyes score from worst GCS set |
| age | SMALLINT | NULL | S |  | Age in years |
| admitdiagnosis | VARCHAR | NULL | S |  | Apache admission diagnosis code |
| thrombolytics | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has thrombolytics, 1 - Patient has thrombolytics |
| diedinhospital | SMALLINT | NULL | S |  | 0/1. 1 – Patient died in hospital |
| aids | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has aids, 1 - Patient has aids |
| hepaticfailure | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has hepaticFailure, 1 - Patient has hepaticFailure |
| lymphoma | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has lymphoma, 1 - Patient has lymphoma |
| metastaticcancer | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has metastaticCancer, 1 - Patient has metastaticCancer |
| leukemia | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has leukemia, 1 - Patient has leukemia |
| immunosuppression | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has immunosuppression, 1 - Patient has immunosuppression |
| cirrhosis | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has cirrhosis, 1 - Patient has cirrhosis |
| electivesurgery | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has elective Surgery, 1 - Patient has elective Surgery |
| activetx | SMALLINT | NULL | S |  | 0/1. Indicates if the Patient has active Treatment |
| readmit | SMALLINT | NULL | S |  | 0/1. Indicates if the Patient was readmitted |
| ima | SMALLINT | NULL | S |  | Indicates if ‘Internal Mammary Artery Graft’ field was selected in eCare or not for the patient |
| midur | SMALLINT | NULL | S |  | Indicates if patient had MI within 6 months |
| ventday1 | SMALLINT | NULL | S |  | Indicates if patient was ventilated for the worst respiratory rate |
| oobventday1 | SMALLINT | NULL | S |  | Indicates if patient was ventilated at anytime for the apache day |
| oobintubday1 | SMALLINT | NULL | S |  | Indicates if patient was intubated at anytime for the apache day |
| diabetes | SMALLINT | NULL | S |  | 0/1. 0 – Patient doesn’t has diabetes, 1 - Patient has diabetes |
| managementsystem | SMALLINT | NULL | S |  | Not used |
| var03hspxlos | DOUBLE | NULL | S |  | Not used |
| pao2 | DOUBLE | NULL | S |  | paO2 value from the worst ABG data set for the Apache Day |
| fio2 | DOUBLE | NULL | S |  | fiO2 value from the worst ABG data set for the Apache Day |
| ejectfx | DOUBLE | NULL |  |  | S |
| creatinine | DOUBLE | NULL | S |  | Worst creatinine value for the Apache day |
| dischargelocation | SMALLINT | NULL | S |  | Value indicating discharge location for the patient |
| visitnumber | SMALLINT | NULL | S |  | value indicating number of unit admission |
| amilocation | SMALLINT | NULL | S |  | 1 to 7. Value indicating AMI Location |
| day1meds | SMALLINT | NULL | S |  | 0 when ‘unable to score due to meds’ is not selected in eCare or there are valid GCS values. 1 when ‘unable to score due to meds’ is selected in eCare. -1 when no meds info is available |
| day1verbal | SMALLINT | NULL | S |  | GCS verbal score from worst GCS set |
| day1motor | SMALLINT | NULL | S |  | GCS motor score from worst GCS set |
| day1eyes | SMALLINT | NULL | S |  | GCS eyes score from worst GCS set |
| day1pao2 | DOUBLE | NULL | S |  | paO2 value from the worst ABG data set for the Apache Day |
| day1fio2 | DOUBLE | NULL | S |  | fiO2 value from the worst ABG data set for the Apache Day |

---

## Care Planning

### careplancareprovider

**Description:** Care plan provider information

**Purpose:** Details relating to the managing or consulting physician, including specialty and intervention category.

**Row Count:** 502,765

**Columns:** 8

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| cplcareprovderid | INTEGER |  |  |  |  |
| patientunitstayid | INTEGER | NOT NULL | Fk | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| careprovidersaveoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the care provider was entered |
| providertype | VARCHAR | NULL | S |  | the picklist type of the care provider: Admitting Consultant Referring Primary |
| specialty | VARCHAR | NULL | S |  | the picklist specialty of the care provider e.g.: cardiology unknown obstetrics/gynecology |
| interventioncategory | VARCHAR | NULL | S |  | The eICU intervention category of the care provider: I, II, III, IV, Unknown, or NULL. This data denotes the level of oversight and intervention authorized for eICU clinicians for this patient by the managing physician (MP). Category I – Ermercency interaction only, Cat II – Emergency and Best Practices intervention only, Cat III – Full interaction, Cat IV - Full interaction (redundant). |
| managingphysician | VARCHAR | NULL | S |  | picklist value which denotes whether this care provider is the managing physician: Managing or Consulting |
| activeupondischarge | VARCHAR | NOT NULL | S |  | denotes if this physician was active upon patient discharge: True or False |

### careplaneol

**Description:** End-of-life care plans

**Purpose:** Documentation relating to end of life care and discussions.

**Row Count:** 1,433

**Columns:** 5

**Important Considerations:**
The Care Plan in eCareManager is used primarily as an intraprofessional communication tool. Variables related to care provider type and specialty, code status, prognosis, family/healthcare proxy, end-of-life discussions, and various therapies (sedation and analgesia therpaies, airway and ventilation status, and stress ulcer and deep vein thrombosis) can be documented on the Care Plan.

    The End-of-Life Discussion section of the Care Plan allows for the care provider who had the discussion, the date/time of the discussion as well as free text comments describing the discussion to be documented.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| cpleolid | INTEGER |  |  |  |  |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| cpleolsaveoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the EOL discussion was entered |
| cpleoldiscussionoffset | INTEGER | NULL | C |  | number of minutes from unit admit time that the EOL discussion occurred |
| activeupondischarge | VARCHAR | NULL | S |  | denotes if the EOL discussion was active upon discharge: True or False |

### careplangeneral

**Description:** General care plans

**Purpose:** Documentation relating to care planning, continuously updated over a patient stay.

**Row Count:** 3,115,018

**Columns:** 6

**Important Considerations:**
The Care Plan in eCareManager is used primarily as an intraprofessional communication tool. Variables related to care provider type and specialty, code status, prognosis, family/healthcare proxy, end-of-life discussions, and various therapies (sedation and analgesia therpaies, airway and ventilation status, and stress ulcer and deep vein thrombosis) can be documented on the Care Plan.

    The Care Plan primarily consists of structured picklist items.

    When determining whether a patient recieved a particular therapy other fields within the database are generally used first, and if missing then variables documented on the Care Plan will be used. For example if the fields in the respiratory flowsheet are blank but mechanical ventilation is chosen as an Active Therapy on the Care Plan then the variable of mechanical ventialtion is determined to be true.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| cplgeneralid | INTEGER | IDENTITY | PK | C | surrogate key for care plan general items |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| activeupondischarge | VARCHAR | NOT NULL | S |  | denotes if the item was active upon discharge: True or False |
| cplitemoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the care plan general item was entered |
| cplgroup | VARCHAR | NOT NULL | S |  | the picklist group type in care plan where the value was selected / entered e.g.: Activity, Critical Care Discharge/Transfer Planning, Daily Goals/Safety Risks/Discharge Requirements, Safety/Restraints, Acuity, etc. |
| cplitemvalue | VARCHAR | NULL | S |  | the picklist value selected / entered into the care plan group e.g.: Very low mortality risk, Non-invasive ventilation, Parenteral - bolus prn |

### careplangoal

**Description:** Care plan goals

**Row Count:** 504,139

**Columns:** 7

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| cplgoalid | INTEGER |  |  |  |  |
| patientunitstayid | INTEGER |  |  |  |  |
| CPLGOALoffset | INTEGER |  |  |  |  |
| CPLGOALCATEGORY | VARCHAR |  |  |  |  |
| CPLGOALVALUE | VARCHAR |  |  |  |  |
| CPLGOALSTATUS | VARCHAR |  |  |  |  |
| ACTIVEUPONDISCHARGE | VARCHAR |  |  |  |  |

### careplaninfectiousdisease

**Description:** Infectious disease care plans

**Purpose:** High level record of infectious diseases added as part of the care plan form.

**Row Count:** 8,056

**Columns:** 8

**Important Considerations:**
The Care Plan in eCareManager is used primarily as an intraprofessional communication tool. Variables related to care provider type and specialty, code status, prognosis, family/healthcare proxy, end-of-life discussions, and various therapies (sedation and analgesia therpaies, airway and ventilation status, and stress ulcer and deep vein thrombosis) can be documented on the Care Plan.

    If infectious disease data are present for a hospital, then this it is likely used to communicate site or source of infectious process and infection control precautions between bedside providers and may be widely used at that particular hospital. This section is rarely completed.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| cplinfectid | INTEGER | IDENTITY | PK | C | surrogate key for care plan infectious diseases |
| patientunitstayid | INTEGER | NOT NULL | FK | C | a globally unique identifier (GUID) used as a foreign key link to the patient table |
| activeupondischarge | VARCHAR | NOT NULL | S |  | denotes whether the infectious disease was active upon discharge: True or False |
| cplinfectdiseaseoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the infectious disease was entered |
| infectdiseasesite | VARCHAR | NULL | S |  | The picklist site of the infectious disease e.g.: Intra-abdominal, Blood, Catheter related bloodstream, etc. |
| infectdiseaseassessment | VARCHAR | NULL | S |  | the picklist assessment of the infectious disease: Definite infection, Probable infection or Possible infection |
| responsetotherapy | VARCHAR | NULL | S |  | the picklist response to the therapy: Improving, No change, Worsening, Resolved, or BLANK |
| treatment | VARCHAR | NULL | S |  | the picklist treatment for the infectious disease: Prophylactic, Empiric, Directed, or BLANK |

---

## Nursing Documentation

---

## Respiratory Care

---

## Other Clinical Data

### treatment

**Description:** Treatment interventions

**Purpose:** The treatment table allows users to document, in a structured format, specific active treatments for the patient.

**Row Count:** 3,688,745

**Columns:** 5

**Important Considerations:**
The treatment table can only be populated directly into eCareManager as structured text. Absence of a treatment documented in this table should not be used as evidence a specific treatment was not administered. Data includes patient treatment information including date/time, whether the treatment was active upon patient discharge, and the path of the treatment e.g.: neurologic | ICH/ cerebral infarct|thrombolytics | tenecteplase, cardiovascular | arrhythmias | antiarrhythmics | atropine, etc.
Table columns
Name    Datatype    Null Option     Comment     Is Key  Stored Transformed Created
patientUnitStayID   int     NOT NULL    foreign key link to the patient table   FK  C
treatmentID     int     IDENTITY    surrogate key for the treatment     PK  C
treatmentOffset     int     NOT NULL    number of minutes from unit admit time that the treatment was entered       C
treatmentString     varchar(200)    NOT NULL    the path of the treatment e.g.: neurologic  ICH/ cerebral infarct   thrombolytics
activeUponDischarge     varchar(10)     NOT NULL    denotes whether the treatment was active upon discharge from the unit: True or False        S

https://eicu-crd.mit.edu/eicutables/treatment/

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| treatmentid | INTEGER | IDENTITY | PK | C | surrogate key for the treatment |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| treatmentoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the treatment was entered |
| treatmentstring | VARCHAR | NOT NULL | ICH/ cerebral infarct | thrombolytics | the path of the treatment e.g.: neurologic |
| activeupondischarge | VARCHAR | NOT NULL | S |  | denotes whether the treatment was active upon discharge from the unit: True or False |

### physicalexam

**Description:** Physical examination findings

**Purpose:** The physical exam section allows users to document results of a physical exam.

**Row Count:** 9,212,316

**Columns:** 6

**Important Considerations:**
Data for physical exam are entered directly into eCareManager. The choices for the physical exam include Not Performed, Performed-Free Text, and Performed-Structured, however the free text sections are not included in the research database. The Structured option allows a large variety of pick list selections and specific text entry boxes to create a structured physical exam.

Physical Exam: The table below lists the data displayed in the Constitutional Data field and the selection criteria for this data (e.g., most recent 15 minute mean value). The values for heart rate, blood pressure, temperature, respiratory rate and O2 sat include the 24 hour range as well as the current values.
Table columns
Name    Datatype    Null Option     Comment     Is Key  Stored Transformed Created
physicalExamID  int     IDENTITY    surrogate key for the physical exam item    PK  C
patientUnitStayID   int     NOT NULL    foreign key link to the patient table   FK  C
physicalExamOffset  int     NOT NULL    number of minutes from unit admit time that the physical exam item was entered      C
physicalExamPath    varchar(255)    NOT NULL    the root path of the physical exam item e.g.: notes/Progress Notes/Physical Exam/Physical Exam/Constitutional/Vital Sign and Physiological Data/Resp Rate/Resp Current, notes/Progress Notes/Physical Exam/Physical Exam/Neurologic/GCS/Verbal Score/5, etc.        S
physicalExamValue   varchar(100)    NULL    Structured picklist of available of physical exam items: O2 Sat% Highest, withdraws to pain, HR Current, etc.       S
physicalExamText    varchar(500)    NOT NULL    The string builder value of the physical exam item e.g.: manual entry, 85, no wheezing, etc.        S


https://eicu-crd.mit.edu/eicutables/physicalexam/

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| physicalexamid | INTEGER | IDENTITY | PK | C | surrogate key for the physical exam item |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| physicalexamoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the physical exam item was entered |
| physicalexampath | VARCHAR | NOT NULL | S |  | the root path of the physical exam item e.g.: notes/Progress Notes/Physical Exam/Physical Exam/Constitutional/Vital Sign and Physiological Data/Resp Rate/Resp Current, notes/Progress Notes/Physical Exam/Physical Exam/Neurologic/GCS/Verbal Score/5, etc. |
| physicalexamvalue | VARCHAR | NULL | S |  | Structured picklist of available of physical exam items: O2 Sat% Highest, withdraws to pain, HR Current, etc. |
| physicalexamtext | VARCHAR | NOT NULL | S |  | The string builder value of the physical exam item e.g.: manual entry, 85, no wheezing, etc. |

### intakeoutput

**Description:** Fluid intake and output records

**Purpose:** Intake and output recorded for patients. Entered from the nursing flowsheet (either manually or interfaced into the hospital system).

**Row Count:** 12,030,289

**Columns:** 12

**Important Considerations:**
Absence of measurement does not indicate absence of intake or output.
    The intakeTotal, outputTotal, diaslysisTotal, and netTotal are cumulative measurements up to the current offset. The value measured for the given row is stored in cellValueNumeric and cellValueText
    When several entries are recorded at the same time for a patient, the values in intaketotal, outputtotal, dialysistotal and nettotal are duplicated!
    outputtotal does not only corrspond to urine output, but also output from drains, blood loss, etc.
    cellvaluenumeric is always POSITIVE, while dialysistotal is NEGATIVE for fluid removal and POSITIVE when fluid is administered to the patient via the dialysis machine.
    With each new entry in intakeoutput, the current daily net total is reported. If several entries happen at the same time, the daily net total will be repeated multiple times. So if you are trying to compute the daily fluid balance, you need to first isolate unique instances of daily net total (select distinct patientunitstayid, intakeoutputoffset, nettotal) and then sum these unique values. Failure to do so will result in a grossly overestimated daily fluid balance.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| intakeoutputid | INTEGER | IDENTITY | PK |  | surrogate key for the intake output data |
| patientunitstayid | INTEGER | NOT NULL | FK |  | foreign key link to the patient table |
| intakeoutputoffset | INTEGER | NOT NULL |  |  | number of minutes from unit admit time that the I and O value was observed |
| intaketotal | DECIMAL(12,4) | NULL |  |  | total intake value up to the current offset, e.g.: 150.0000, 326.0000, 142.0000, etc. |
| outputtotal | DECIMAL(12,4) | NULL |  |  | total output value up to the current offset, e.g.: 230.0000, 350.0000, 150.0000, etc. |
| dialysistotal | DECIMAL(12,4) | NULL |  |  | total dialysis value up to the current offset, e.g.: -96.0000, -2300.0000, 0.0000, etc. |
| nettotal | DECIMAL(12,4) | NULL |  |  | calculated net value of: intakeTotal – outputTotal + dialysisTotal |
| intakeoutputentryoffset | INTEGER | NOT NULL |  |  | number of minutes from unit admit time that the I and O value was entered |
| cellpath | VARCHAR | NOT NULL | Flowsheet Cell Labels |  | the root path of info from the label in I and O e.g.: flowsheet |
| celllabel | VARCHAR | NOT NULL |  |  | The predefined row label text from I and O e.g.: Enteral flush/meds panda, D5 0.45 NS w/20 mEq KCL 1000 ml, Continuous infusion meds, etc. |
| cellvaluenumeric | DECIMAL(12,4) | NOT NULL |  |  | the value of the current I and O row e.g.: 100.0000, 60.9000, 10.0000, etc. |
| cellvaluetext | VARCHAR | NOT NULL |  |  | text conversion of the numeric value of the I and O row e.g.: 100, 360, 50 |

### microlab

**Description:** Microbiology laboratory results

**Purpose:** Microbiology data.

**Row Count:** 16,996

**Columns:** 7

**Important Considerations:**
The dataset is not well populated due to limited availability of microbiology interfaces.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| microlabid | INTEGER | IDENTITY | PK | C | surrogate key for the micro lab |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| culturetakenoffset | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the culture was taken |
| culturesite | VARCHAR | NOT NULL | S |  | picklist site name from where the culture was taken e.g.: Wound, Drainage Fluid, Sputum, Expectorated, Nasopharynx, etc. |
| organism | VARCHAR | NOT NULL | S |  | picklist organism found e.g.: Staphylococcus aureus, Pseudomonas aeruginosa, no growth, etc. |
| antibiotic | VARCHAR | NULL | S |  | picklist antibiotic used e.g.: ceftazidime, aztreonam, other, etc. |
| sensitivitylevel | VARCHAR | NULL | S |  | picklist sensitivity level of antibiotic: Intermediate, Resistant, or Sensitive |

### note

**Description:** Clinical notes

**Purpose:** There are several types of notes which can be entered in the system. The detailed description provides a list of the possible Note types and their intended use. Notes are generally entered by the physician or physician extender primarily responsible for the documentation of the patient’s unit care.

**Row Count:** 2,254,179

**Columns:** 8

**Important Considerations:**
The majority of data entered in notes is done in a structured format and available in the database. Any notes or section of notes which are primarily narrative text format have been removed and are not available for research at this time in order to minimize risk of including PHI.

| Column Name | Data Type | Null | Key | S/T/C | Description |
|-------------|-----------|------|-----|-------|-------------|
| NOTEID | INTEGER | IDENTITY | PK | C | surrogate key for the note item |
| patientunitstayid | INTEGER | NOT NULL | FK | C | foreign key link to the patient table |
| NOTEOFFSET | INTEGER | NOT NULL | C |  | number of minutes from unit admit time for the note item, derived from the note’s date of service |
| NOTEENTEREDOFFSET | INTEGER | NOT NULL | C |  | number of minutes from unit admit time that the note item was entered |
| NOTETYPE | VARCHAR | NULL | S |  | type of note e.g.: Admission, Comprehensive Progress, Brief Progress, etc. |
| NOTEPATH | VARCHAR | NOT NULL | S |  | the root path of the note item e.g.: notes/Progress Notes/Assessment and Plan/Organ System dx(s) and rx(s)/Gastrointestinal/Dx/Dx, notes/Progress Notes/Assessment and Plan/Organ System dx(s) and rx(s)/Gastrointestinal/Dx/Dx, etc. |
| NOTEVALUE | VARCHAR | NULL | S |  | the picklist value name of the note item e.g.: HR Highest, Dx, Verified procedure, etc. |
| NOTETEXT | VARCHAR | NULL | S |  | the picklist value text of the note item e.g.: ABDOMINAL PAIN / TENDERNESS, nausea-with vomiting, +1358, respiratory arrest, etc. |

---
