import json
from pathlib import Path

# Read the notebook
notebook_path = Path("../notebooks/exploratory/07_data_preprocessing_analysis.ipynb")
with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Export cells to add
export_cells = [
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create output directory\n",
            "output_dir = Path(\"data_samples\")\n",
            "output_dir.mkdir(exist_ok=True)\n",
            "\n",
            "print(\"Output directory:\", output_dir.absolute())\n",
            "print(\"\\nExporting CSV samples for manual review...\\n\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# EXPORT 1: Categorical Features - Show distribution of top categorical features\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT 1: Categorical Features Sample\")\n",
            "print(\"=\" * 80)\n",
            "\n",
            "# Get 15 random samples with their categorical features\n",
            "sample_cols = ['patientunitstayid'] + current_categorical\n",
            "export1 = df[sample_cols].sample(n=15, random_state=42)\n",
            "\n",
            "export1_path = output_dir / \"01_categorical_features_sample.csv\"\n",
            "export1.to_csv(export1_path, index=False)\n",
            "\n",
            "print(f\"Exported {len(export1)} records\")\n",
            "print(f\"File: {export1_path}\")\n",
            "print(f\"\\nSample preview:\")\n",
            "print(export1.head().to_string(index=False))\n",
            "print(\"\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# EXPORT 2: Miscategorized Features - Binary/low-cardinality features treated as numeric\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT 2: Potential Miscategorized Features Sample\")\n",
            "print(\"=\" * 80)\n",
            "\n",
            "# Show 20 records with binary APACHE flags and other low-cardinality features\n",
            "misc_features = ['patientunitstayid', 'apache_intubated', 'apache_vent', 'apache_dialysis',\n",
            "                'apache_diabetes', 'apache_admitsource_code', 'apache_gcs_eyes', \n",
            "                'apache_gcs_verbal', 'apache_gcs_motor', 'vent_started_24h', \n",
            "                'pressor_norepi_24h', 'pressor_epi_24h']\n",
            "\n",
            "misc_features = [f for f in misc_features if f in df.columns]\n",
            "export2 = df[misc_features].sample(n=20, random_state=42)\n",
            "\n",
            "export2_path = output_dir / \"02_miscategorized_features_sample.csv\"\n",
            "export2.to_csv(export2_path, index=False)\n",
            "\n",
            "print(f\"Exported {len(export2)} records\")\n",
            "print(f\"File: {export2_path}\")\n",
            "print(f\"Features included: {len(misc_features)-1} potential categorical features\")\n",
            "print(f\"\\nSample preview:\")\n",
            "print(export2.head(10).to_string(index=False))\n",
            "print(\"\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# EXPORT 3: APACHE -1.0 Values - Records with missing indicators\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT 3: APACHE -1.0 Values Sample\")\n",
            "print(\"=\" * 80)\n",
            "\n",
            "# Get records with -1.0 values in high-frequency features\n",
            "high_neg_one_features = ['apache_pao2', 'apache_ph', 'apache_fio2', 'apache_pco2', \n",
            "                         'apache_bilirubin', 'apache_albumin']\n",
            "\n",
            "# Find records with at least one -1.0 value\n",
            "mask = (df[high_neg_one_features] == -1.0).any(axis=1)\n",
            "export3_cols = ['patientunitstayid'] + high_neg_one_features\n",
            "export3 = df[mask][export3_cols].sample(n=min(20, mask.sum()), random_state=42)\n",
            "\n",
            "export3_path = output_dir / \"03_apache_neg_one_values_sample.csv\"\n",
            "export3.to_csv(export3_path, index=False)\n",
            "\n",
            "print(f\"Exported {len(export3)} records with -1.0 values\")\n",
            "print(f\"File: {export3_path}\")\n",
            "print(f\"\\nSample preview (showing -1.0 missing indicators):\")\n",
            "print(export3.head(10).to_string(index=False))\n",
            "print(\"\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# EXPORT 4: Outliers - Records with outlier values\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT 4: Outlier Records Sample\")\n",
            "print(\"=\" * 80)\n",
            "\n",
            "# Focus on creatinine_mean_24h (12% outliers)\n",
            "feat_info = outlier_df[outlier_df['feature'] == 'creatinine_mean_24h'].iloc[0]\n",
            "lower = feat_info['lower_bound']\n",
            "upper = feat_info['upper_bound']\n",
            "\n",
            "# Get outlier records\n",
            "outlier_mask = (df['creatinine_mean_24h'] < lower) | (df['creatinine_mean_24h'] > upper)\n",
            "outlier_cols = ['patientunitstayid', 'creatinine_mean_24h', 'creatinine_max_24h',\n",
            "                'apache_creatinine', 'admissionweight', 'age_numeric']\n",
            "\n",
            "export4 = df[outlier_mask][outlier_cols].sample(n=min(25, outlier_mask.sum()), random_state=42)\n",
            "\n",
            "export4_path = output_dir / \"04_outlier_records_sample.csv\"\n",
            "export4.to_csv(export4_path, index=False)\n",
            "\n",
            "print(f\"Exported {len(export4)} records with outlier creatinine values\")\n",
            "print(f\"File: {export4_path}\")\n",
            "print(f\"IQR bounds: [{lower:.2f}, {upper:.2f}]\")\n",
            "print(f\"\\nSample preview:\")\n",
            "print(export4.head(10).to_string(index=False))\n",
            "print(\"\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# EXPORT 5: High Missing Data - Records from features with >30% missing\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT 5: High Missing Data Sample\")\n",
            "print(\"=\" * 80)\n",
            "\n",
            "# Features with >30% missing\n",
            "high_miss_features = high_missing['feature'].tolist()\n",
            "export5_cols = ['patientunitstayid'] + high_miss_features\n",
            "\n",
            "export5 = df[export5_cols].sample(n=20, random_state=42)\n",
            "\n",
            "export5_path = output_dir / \"05_high_missing_data_sample.csv\"\n",
            "export5.to_csv(export5_path, index=False)\n",
            "\n",
            "print(f\"Exported {len(export5)} records\")\n",
            "print(f\"File: {export5_path}\")\n",
            "print(f\"Features with >30% missing: {len(high_miss_features)}\")\n",
            "print(f\"\\nSample preview:\")\n",
            "print(export5.head(10).to_string(index=False))\n",
            "print(\"\\nNote: NaN values represent actual missing data\")\n",
            "print(\"\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# EXPORT 6: Feature Engineering Candidates - Records where we can create new features\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT 6: Feature Engineering Candidates Sample\")\n",
            "print(\"=\" * 80)\n",
            "\n",
            "# Get records where we can create BMI, total GCS, and vital ranges\n",
            "has_bmi_data = df['admissionheight'].notna() & df['admissionweight'].notna()\n",
            "has_gcs_data = (df['apache_gcs_eyes'].notna() & \n",
            "                df['apache_gcs_verbal'].notna() & \n",
            "                df['apache_gcs_motor'].notna())\n",
            "has_vitals = df['min_hr_24h'].notna() & df['max_hr_24h'].notna()\n",
            "\n",
            "# Get records with all engineerable features\n",
            "mask = has_bmi_data & has_gcs_data & has_vitals\n",
            "\n",
            "eng_cols = ['patientunitstayid', 'admissionheight', 'admissionweight',\n",
            "            'apache_gcs_eyes', 'apache_gcs_verbal', 'apache_gcs_motor',\n",
            "            'min_hr_24h', 'max_hr_24h', 'min_rr_24h', 'max_rr_24h',\n",
            "            'min_sao2_24h', 'max_sao2_24h']\n",
            "\n",
            "export6 = df[mask][eng_cols].sample(n=min(20, mask.sum()), random_state=42)\n",
            "\n",
            "# Calculate the engineered features for demonstration\n",
            "export6 = export6.copy()\n",
            "export6['BMI'] = export6['admissionweight'] / ((export6['admissionheight']/100) ** 2)\n",
            "export6['total_GCS'] = (export6['apache_gcs_eyes'] + \n",
            "                        export6['apache_gcs_verbal'] + \n",
            "                        export6['apache_gcs_motor'])\n",
            "export6['HR_range'] = export6['max_hr_24h'] - export6['min_hr_24h']\n",
            "\n",
            "export6_path = output_dir / \"06_feature_engineering_sample.csv\"\n",
            "export6.to_csv(export6_path, index=False)\n",
            "\n",
            "print(f\"Exported {len(export6)} records with engineerable features\")\n",
            "print(f\"File: {export6_path}\")\n",
            "print(f\"\\nNew features demonstrated: BMI, total_GCS, HR_range\")\n",
            "print(f\"\\nSample preview:\")\n",
            "print(export6[['patientunitstayid', 'admissionheight', 'admissionweight', 'BMI', \n",
            "               'apache_gcs_eyes', 'apache_gcs_verbal', 'apache_gcs_motor', 'total_GCS']].head(10).to_string(index=False))\n",
            "print(\"\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# EXPORT 7: Multicollinearity - Show highly correlated feature pairs\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT 7: Multicollinearity Sample\")\n",
            "print(\"=\" * 80)\n",
            "\n",
            "# Create a dataframe showing the correlated pairs\n",
            "corr_data = []\n",
            "for feat1, feat2, corr_val in high_corr_pairs:\n",
            "    # Get sample values for both features\n",
            "    sample_records = df[[feat1, feat2]].dropna().sample(n=min(5, len(df)), random_state=42)\n",
            "    for idx, row in sample_records.iterrows():\n",
            "        corr_data.append({\n",
            "            'feature_1': feat1,\n",
            "            'feature_2': feat2,\n",
            "            'correlation': corr_val,\n",
            "            'value_1': row[feat1],\n",
            "            'value_2': row[feat2]\n",
            "        })\n",
            "\n",
            "export7 = pd.DataFrame(corr_data)\n",
            "\n",
            "export7_path = output_dir / \"07_multicollinearity_sample.csv\"\n",
            "export7.to_csv(export7_path, index=False)\n",
            "\n",
            "print(f\"Exported {len(export7)} sample records showing correlated pairs\")\n",
            "print(f\"File: {export7_path}\")\n",
            "print(f\"\\nHighly correlated pairs (correlation > 0.9):\")\n",
            "for feat1, feat2, corr_val in sorted(high_corr_pairs, key=lambda x: x[2], reverse=True):\n",
            "    print(f\"  {feat1} ↔ {feat2}: {corr_val:.4f}\")\n",
            "print(f\"\\nSample preview:\")\n",
            "print(export7.head(15).to_string(index=False))\n",
            "print(\"\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Summary of all exports\n",
            "print(\"=\" * 80)\n",
            "print(\"EXPORT SUMMARY\")\n",
            "print(\"=\" * 80)\n",
            "print(f\"\\nAll CSV files saved to: {output_dir.absolute()}\")\n",
            "print(f\"\\nExported files:\")\n",
            "for csv_file in sorted(output_dir.glob(\"*.csv\")):\n",
            "    size_kb = csv_file.stat().st_size / 1024\n",
            "    print(f\"  - {csv_file.name} ({size_kb:.1f} KB)\")\n",
            "print(f\"\\n✅ All exports completed successfully!\")\n",
            "print(\"=\" * 80)"
        ]
    }
]

# Add the export cells to the notebook
for cell in export_cells:
    nb['cells'].append(cell)

# Write the updated notebook
with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Added {len(export_cells)} export cells to {notebook_path}")
