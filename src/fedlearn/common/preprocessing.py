from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder

from fedlearn.common.annotation import ANNOTATION_CONFIG

CATEGORICAL_FEATURES: list[str] = list(ANNOTATION_CONFIG.keys())

NUMERIC_FEATURES: list[str] = [
    "admissionheight",
    "admissionweight",
    "age_numeric",
    "any_pressor_24h",
    "apache_admitsource_code",
    "apache_admitsource_code_missing",
    "apache_aids",
    "apache_albumin",
    "apache_albumin_missing",
    "apache_bedcount",
    "apache_bedcount_missing",
    "apache_bilirubin",
    "apache_bilirubin_missing",
    "apache_bun",
    "apache_bun_missing",
    "apache_cirrhosis",
    "apache_creatinine",
    "apache_creatinine_missing",
    "apache_diabetes",
    "apache_dialysis",
    "apache_electivesurgery",
    "apache_electivesurgery_missing",
    "apache_gcs_eyes",
    "apache_gcs_motor",
    "apache_gcs_total",
    "apache_gcs_verbal",
    "apache_glucose",
    "apache_glucose_missing",
    "apache_hct",
    "apache_hct_missing",
    "apache_hepaticfailure",
    "apache_hr",
    "apache_immunosuppression",
    "apache_intubated",
    "apache_leukemia",
    "apache_lymphoma",
    "apache_meanbp",
    "apache_metastaticcancer",
    "apache_oobintubday1",
    "apache_oobventday1",
    "apache_readmit",
    "apache_rr",
    "apache_sodium",
    "apache_sodium_missing",
    "apache_temp",
    "apache_temp_missing",
    "apache_urine_24h",
    "apache_urine_24h_missing",
    "apache_vent",
    "apache_ventday1",
    "apache_wbc",
    "apache_wbc_missing",
    "avg_hr_24h",
    "avg_rr_24h",
    "avg_sao2_24h",
    "bmi",
    "creatinine_change_24h",
    "creatinine_max_24h",
    "creatinine_mean_24h",
    "emergency_admit",
    "glucose_mean_24h",
    "had_bradycardia_24h",
    "had_hypoxemia_24h",
    "had_tachycardia_24h",
    "has_aki_24h",
    "hr_range_24h",
    "is_missing_gcs_eyes",
    "is_missing_gcs_motor",
    "is_missing_gcs_verbal",
    "max_hr_24h",
    "max_rr_24h",
    "max_sao2_24h",
    "min_hr_24h",
    "min_rr_24h",
    "min_sao2_24h",
    "pressor_epi_24h",
    "pressor_epi_24h_missing",
    "pressor_norepi_24h",
    "pressor_norepi_24h_missing",
    "pressor_vaso_24h",
    "pressor_vaso_24h_missing",
    "rr_range_24h",
    "sao2_range_24h",
    "sedative_propofol_24h",
    "sedative_propofol_24h_missing",
    "unitvisitnumber",
    "vent_started_24h",
    "vent_started_24h_missing",
    "wbc_mean_24h",
]

ALL_FEATURES: list[str] = (NUMERIC_FEATURES + CATEGORICAL_FEATURES)


def build_preprocessor() -> ColumnTransformer:
    """
    Build a preprocessing pipeline with a fixed, annotation-aware schema.
    """
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler()),
    ])

    categories_per_feature = [
        ANNOTATION_CONFIG[col]["categories"] for col in CATEGORICAL_FEATURES
    ]

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(categories=categories_per_feature, handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", numeric_transformer, NUMERIC_FEATURES),
            ("categorical", categorical_transformer, CATEGORICAL_FEATURES),
        ],
    )

    return preprocessor


# No longer used - kept for reference
def build_preprocessor_dynamically(df) -> ColumnTransformer:
    """
    Build a preprocessing pipeline dynamically, based on dataset
    """
    numeric_features = df.select_dtypes(include=["number"]).columns
    categorical_features = df.select_dtypes(exclude=["number"]).columns

    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler()),
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", numeric_transformer, numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ],
    )

    return preprocessor
