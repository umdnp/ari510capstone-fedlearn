# Notebooks

This directory contains Jupyter notebooks for exploratory data analysis and model development for the ICU prolonged stay prediction project.

## Structure

- `exploratory/` - Exploratory Data Analysis (EDA) and model development notebooks

## Notebooks

### Exploratory Analysis

#### 01_database_exploration.ipynb
Initial exploration of the eICU Collaborative Research Database structure, tables, and relationships. Understanding the raw data schema and available features.

#### 02_icu_length_of_stay_analysis.ipynb
Analysis of ICU length of stay patterns, distribution, and definition of the target variable (prolonged stay > 3 days). Examines class balance and statistical properties.

#### 03_feature_exploration.ipynb
Deep dive into clinical features including demographics, vital signs, lab values, and APACHE scores. Explores feature distributions, correlations, and missing value patterns.

#### 04_partitioning_analysis.ipynb
Analysis of data partitioning strategies for federated learning. Explores different ways to split data across simulated hospital sites while maintaining statistical properties.

#### 05_feature_extraction_and_imputation.ipynb
Feature engineering from raw eICU tables and evaluation of different imputation strategies for handling missing clinical data (median, KNN, iterative imputation).

#### 06_model_comparison.ipynb
Initial comparison of machine learning models (Logistic Regression, Random Forest, Gradient Boosting, SGD) on the ICU prolonged stay prediction task.

#### 07_data_preprocessing_analysis.ipynb
Analysis of preprocessing pipeline components including standardization, one-hot encoding, and feature selection. Evaluates impact on model performance.

#### 08_comprehensive_model_comparison.ipynb
Extended model comparison with additional algorithms and evaluation metrics. Includes detailed performance analysis across different model families.

#### 09_feature_importance_analysis.ipynb
Analysis of feature importance using various methods (tree-based importance, permutation importance, SHAP values). Identifies most predictive clinical features for prolonged ICU stays.

#### 10_hyperparameter_tuning.ipynb
Systematic hyperparameter tuning for best performing models. Uses grid search and cross-validation to optimize model configurations.

## Running Notebooks

### Prerequisites

```bash
# Activate virtual environment
source .venv/bin/activate

# Install Jupyter (if not already installed)
pip install jupyter ipykernel

# Start Jupyter
jupyter notebook
```

### Data Requirements

Notebooks require access to:
- eICU Collaborative Research Database (full dataset for notebooks 01-10)
- DuckDB database: `data/duckdb/fedlearn.duckdb`
- Preprocessed features and labels

See main project README for data setup instructions.

## Naming Convention

Notebooks use numbered prefixes for sequential ordering:
- `01_` through `10_` - Sequential exploratory analysis
- Descriptive names indicate the notebook's focus

## Notes

- Notebooks are for exploratory analysis and prototyping
- Production code should be in `src/fedlearn/` modules
- Checkpoint files (`.ipynb_checkpoints/`) are git-ignored
