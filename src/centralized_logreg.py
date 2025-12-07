import duckdb
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.linear_model import LogisticRegression

from fedlearn.evaluation import evaluate_model

# load data
conn = duckdb.connect("../data/duckdb/fedlearn.duckdb")
df = conn.execute("select * from v_features_icu_stay_clean").df()

y = df["prolonged_stay"]
X = df.drop(
    columns=["patientunitstayid", "los_days", "prolonged_stay", "apacheadmissiondx"]
)

categorical_features = [
    "gender",
    "ethnicity",
    "unittype",
    "unitadmitsource",
    "hospitaladmitsource",
    "admissiondx_category",
    "numbedscategory",
    "teachingstatus",
    "hospital_region",
    "apache_admitsource_code",
    "age_group",
]

numeric_features = [c for c in X.columns if c not in categorical_features]

# preprocessing for logistic regression

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler()),
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

# logistic regression model

logreg = Pipeline(
    steps=[
        ("preprocess", preprocess),
        (
            "clf",
            LogisticRegression(
                max_iter=500,
                n_jobs=-1,
                class_weight="balanced",
                solver="lbfgs",
                random_state=42,
            ),
        ),
    ]
)

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# fit + evaluate
_ = evaluate_model("Logistic Regression", logreg, X_train, y_train, X_test, y_test)
