import duckdb
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from fedlearn.evaluation import evaluate_model
from src.fedlearn.preprocessing import build_preprocessor

# load data
conn = duckdb.connect("../data/duckdb/fedlearn.duckdb")
df = conn.execute("select * from v_features_icu_stay_clean").df()

# normalize pandas.NA -> np.nan (so sklearn's SimpleImputer can handle it)
df = df.where(df.notna(), np.nan)

# target and feature selection
y = df["prolonged_stay"]
X = df.drop(columns=["patientunitstayid", "los_days", "prolonged_stay", "apacheadmissiondx"])

# logistic regression model
logreg = Pipeline([
    ("preprocessor", build_preprocessor(X)),
    ("classifier", LogisticRegression(
        max_iter=1000,
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
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )),
])

# gradient boosting model
GB = Pipeline([
    ("preprocessor", build_preprocessor(X)),
    ("classifier", GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
    )),
])

# sgd classifier (supports partial_fit for federated learning)
SGD = Pipeline([
    ("preprocessor", build_preprocessor(X)),
    ("classifier", SGDClassifier(
        loss="log_loss",
        penalty="l2",
        alpha=0.0001,
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )),
])

# train/val/test split (60/20/20)
# first split: 80/20 (train+val / test)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# second split: 75/25 of remaining (60/20 of total)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)

print("Dataset split sizes:")
print(f"  Training:   {len(X_train):,} samples ({len(X_train) / len(X) * 100:.1f}%)")
print(f"  Validation: {len(X_val):,} samples ({len(X_val) / len(X) * 100:.1f}%)")
print(f"  Test:       {len(X_test):,} samples ({len(X_test) / len(X) * 100:.1f}%)")
print()

# fit + evaluate on validation set (for hyperparameter tuning)
print("=" * 80)
print("VALIDATION SET PERFORMANCE (for hyperparameter tuning)")
print("=" * 80)
print()
evaluate_model("Logistic Regression", logreg, X_train, y_train, X_val, y_val)
evaluate_model("Random Forest", RF, X_train, y_train, X_val, y_val)
evaluate_model("Gradient Boosting", GB, X_train, y_train, X_val, y_val)
evaluate_model("SGD Classifier", SGD, X_train, y_train, X_val, y_val)

# fit + evaluate on test set (final held-out performance)
print("=" * 80)
print("FINAL TEST SET PERFORMANCE (held-out)")
print("=" * 80)
print()
evaluate_model("Logistic Regression", logreg, X_train, y_train, X_test, y_test)
evaluate_model("Random Forest", RF, X_train, y_train, X_test, y_test)
evaluate_model("Gradient Boosting", GB, X_train, y_train, X_test, y_test)
evaluate_model("SGD Classifier", SGD, X_train, y_train, X_test, y_test)
