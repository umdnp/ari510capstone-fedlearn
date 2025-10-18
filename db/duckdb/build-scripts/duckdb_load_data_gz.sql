PRAGMA threads=8;

INSERT INTO admissiondrug SELECT * FROM read_csv_auto('admissionDrug.csv.gz', header=true, quote='"', escape='"');
INSERT INTO admissiondx   SELECT * FROM read_csv_auto('admissionDx.csv.gz',   header=true, quote='"', escape='"');
INSERT INTO allergy       SELECT * FROM read_csv_auto('allergy.csv.gz',       header=true, quote='"', escape='"');
INSERT INTO apacheapsvar  SELECT * FROM read_csv_auto('apacheApsVar.csv.gz',  header=true, quote='"', escape='"');
INSERT INTO apachepatientresult SELECT * FROM read_csv_auto('apachePatientResult.csv.gz', header=true, quote='"', escape='"');
INSERT INTO apachepredvar SELECT * FROM read_csv_auto('apachePredVar.csv.gz', header=true, quote='"', escape='"');
INSERT INTO careplancareprovider SELECT * FROM read_csv_auto('carePlanCareProvider.csv.gz', header=true, quote='"', escape='"');
INSERT INTO careplaneol   SELECT * FROM read_csv_auto('carePlanEOL.csv.gz',   header=true, quote='"', escape='"');
INSERT INTO careplangeneral SELECT * FROM read_csv_auto('carePlanGeneral.csv.gz', header=true, quote='"', escape='"');
INSERT INTO careplangoal  SELECT * FROM read_csv_auto('carePlanGoal.csv.gz',  header=true, quote='"', escape='"');
INSERT INTO careplaninfectiousdisease SELECT * FROM read_csv_auto('carePlanInfectiousDisease.csv.gz', header=true, quote='"', escape='"');
INSERT INTO customlab     SELECT * FROM read_csv_auto('customLab.csv.gz',     header=true, quote='"', escape='"');
INSERT INTO diagnosis     SELECT * FROM read_csv_auto('diagnosis.csv.gz',     header=true, quote='"', escape='"');
INSERT INTO hospital      SELECT * FROM read_csv_auto('hospital.csv.gz',      header=true, quote='"', escape='"');
INSERT INTO infusiondrug  SELECT * FROM read_csv_auto('infusionDrug.csv.gz',  header=true, quote='"', escape='"');
INSERT INTO intakeoutput  SELECT * FROM read_csv_auto('intakeOutput.csv.gz',  header=true, quote='"', escape='"');
INSERT INTO lab           SELECT * FROM read_csv_auto('lab.csv.gz',           header=true, quote='"', escape='"');
INSERT INTO medication    SELECT * FROM read_csv_auto('medication.csv.gz',    header=true, quote='"', escape='"');
INSERT INTO microlab      SELECT * FROM read_csv_auto('microLab.csv.gz',      header=true, quote='"', escape='"');
INSERT INTO note          SELECT * FROM read_csv_auto('note.csv.gz',          header=true, quote='"', escape='"');
INSERT INTO nurseassessment SELECT * FROM read_csv_auto('nurseAssessment.csv.gz', header=true, quote='"', escape='"');
INSERT INTO nursecare     SELECT * FROM read_csv_auto('nurseCare.csv.gz',     header=true, quote='"', escape='"');
INSERT INTO nursecharting SELECT * FROM read_csv_auto('nurseCharting.csv.gz', header=true, quote='"', escape='"');
INSERT INTO pasthistory   SELECT * FROM read_csv_auto('pastHistory.csv.gz',   header=true, quote='"', escape='"');
INSERT INTO patient       SELECT * FROM read_csv_auto('patient.csv.gz',       header=true, quote='"', escape='"');
INSERT INTO physicalexam  SELECT * FROM read_csv_auto('physicalExam.csv.gz',  header=true, quote='"', escape='"');
INSERT INTO respiratorycare SELECT * FROM read_csv_auto('respiratoryCare.csv.gz', header=true, quote='"', escape='"');
INSERT INTO respiratorycharting SELECT * FROM read_csv_auto('respiratoryCharting.csv.gz', header=true, quote='"', escape='"');
INSERT INTO treatment     SELECT * FROM read_csv_auto('treatment.csv.gz',     header=true, quote='"', escape='"');
INSERT INTO vitalaperiodic SELECT * FROM read_csv_auto('vitalAperiodic.csv.gz', header=true, quote='"', escape='"');
INSERT INTO vitalperiodic SELECT * FROM read_csv_auto('vitalPeriodic.csv.gz', header=true, quote='"', escape='"');

CHECKPOINT;

