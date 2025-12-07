import duckdb
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

from fedlearn.evaluation import evaluate_model

# load data
conn = duckdb.connect("../data/duckdb/fedlearn.duckdb")
df = conn.execute("select * from v_features_icu_stay_clean").df()

# normalize pandas.NA -> np.nan (so sklearn's SimpleImputer can handle it)
df = df.where(df.notna(), np.nan)


# preprocessing for logistic regression

def build_preprocessor(df) -> ColumnTransformer:
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


# target and feature selection
y = df["prolonged_stay"]
X = df.drop(columns=["patientunitstayid", "los_days", "prolonged_stay", "apacheadmissiondx"])

# logistic regression model
logreg = Pipeline([
    ("preprocessor", build_preprocessor(X)),
    ("classifier", LogisticRegression(
        max_iter=500,
        n_jobs=-1,
        class_weight="balanced",
        solver="lbfgs",
        random_state=42,
    )),
])

# random forest model
RF = Pipeline([
    ("preprocessor", build_preprocessor(X)),
    ("classifier", RandomForestClassifier(
        random_state=42,
    )),
])

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# fit + evaluate
evaluate_model("Logistic Regression", logreg, X_train, y_train, X_test, y_test)
evaluate_model("Random Forest", RF, X_train, y_train, X_test, y_test)
