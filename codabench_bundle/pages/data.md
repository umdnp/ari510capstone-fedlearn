# Dataset Information

## Data Source

This competition uses the **eICU Collaborative Research Database (Demo Version)**.

- **Official Source**: [PhysioNet - eICU-CRD Demo v2.0.1](https://physionet.org/content/eicu-crd-demo/2.0.1/)
- **Publisher**: MIT Laboratory for Computational Physiology
- **License**: Open Data Commons Open Database License v1.0
- **Access**: Publicly available, no credentials required

## Original Dataset

The eICU Collaborative Research Database contains de-identified health data from ICU patients across multiple hospitals in the United States. The demo version is a subset designed for educational and research purposes.

### Citation

If you use this dataset in your research, please cite:

```
Pollard, T. J., Johnson, A. E. W., Raffa, J. D., Celi, L. A., Mark, R. G.,
& Badawi, O. (2018). The eICU Collaborative Research Database, a freely
available multi-center database for critical care research. Scientific Data,
5, 180178. https://doi.org/10.1038/sdata.2018.178
```

## Competition Dataset

### Source Data
- **Total ICU Stays**: 2,520 patient records from the demo dataset
- **Time Period**: 2014-2015
- **Hospitals**: Multiple ICUs across the United States

### Feature Engineering

The raw eICU demo data was processed to create machine learning-ready features:

1. **Demographics**: Age, gender, ethnicity, admission weight
2. **Vital Signs**: Aggregated statistics (mean, std, min, max) for:
   - Heart rate
   - Blood pressure (systolic, diastolic, mean arterial)
   - Temperature
   - Oxygen saturation
   - Respiratory rate

3. **Laboratory Values**: Aggregated statistics for:
   - WBC, creatinine, BUN, glucose
   - Electrolytes (sodium, potassium, bicarbonate)
   - Hematology (Hct, Hgb, platelets)
   - Liver function (total bilirubin)

4. **Clinical Scores**: APACHE IV scores and mortality predictions

### Target Variable

**Prolonged ICU Stay**: Binary classification
- **0**: Length of stay ≤ 3 days
- **1**: Length of stay > 3 days

Calculated as: `prolonged_stay = 1 if (unitdischargeoffset / 1440) > 3 else 0`

### Train/Test Split

- **Training Set**: 1,512 samples (60%)
- **Test Set**: 1,008 samples (40%)
- **Split Method**: Stratified random split (random_state=42)
- **Class Distribution**: 78.2% not prolonged, 21.8% prolonged (maintained in both splits)

### Data Quality

- **Missing Values**: Various features have missing data (clinical reality)
- **Data Leakage Prevention**: `los_days` excluded from features
- **Text Fields Removed**: `apacheadmissiondx` excluded (free text)

## Processing Pipeline

The data was processed using the following pipeline:

1. Load raw CSV files from eICU demo (patient, vitalPeriodic, lab, apachePatientResult)
2. Calculate prolonged stay target from `unitdischargeoffset`
3. Aggregate time-series vital signs (mean, std, min, max per patient)
4. Aggregate laboratory values (mean, std, min, max per patient)
5. Extract APACHE scores and predictions
6. Merge all features into single dataset
7. Handle age encoding ("> 89" → 90)
8. Create stratified 60/40 train/test split

## Data Usage Terms

By participating in this competition, you agree to:

1. Use the data only for the purposes of this competition
2. Not attempt to re-identify any patients
3. Cite the original eICU-CRD publication if using this data in publications
4. Comply with the Open Data Commons Open Database License v1.0

## Acknowledgments

We thank the MIT Laboratory for Computational Physiology and all contributing hospitals for making the eICU Collaborative Research Database publicly available for research and education.

## Questions?

For questions about the original dataset, please refer to:
- [eICU-CRD Demo Documentation](https://physionet.org/content/eicu-crd-demo/2.0.1/)
- [eICU-CRD Full Database](https://eicu-crd.mit.edu/)
