# ARI 510 HW3 - Data Annotation Package

This repository contains all materials for HW3, supporting data annotation for the eICU ICU stay prediction project.

## Files Included
- **annotations.xlsx** - The annotation interface used to label categorical features and document numeric feature meanings.
- **annotation_guidelines.docx** - Complete annotation instructions for annotators.
- **annotation_guidelines.docx** - Annotation guidelines in PDF format.
- **LICENSE.txt** - An Open Database License (ODbL) v1.0 is included with the demo data.

## Dataset
Due to restrictions on the full eICU dataset, this assignment uses the public demo subset:

https://physionet.org/content/eicu-crd-demo/2.0.1

This dataset contains the same schema as the full eICU-CRD, allowing accurate annotation work.

## Annotation Workflow
1. Open `annotations.xlsx`.
2. Use the Categorical Features sheet to expand each feature and inspect the raw -> canonical mappings.
3. Use the Numeric Features sheet to understand and validate descriptions and binary meanings.
4. Refer to `annotation_guidelines.docx` for full instructions.

## Purpose
Clean, human-defined annotations improve:
- Model interpretability  
- Category consistency  
- Downstream machine learning performance  

These annotations are used by the model's preprocessing pipeline to normalize data and ensure stable behavior across training/evaluation.
