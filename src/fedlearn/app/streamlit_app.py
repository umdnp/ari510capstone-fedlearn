from __future__ import annotations

from pathlib import Path

import duckdb
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

from fedlearn.common.annotation import annotate_categorical_columns

# Constants

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DUCKDB_PATH = PROJECT_ROOT / "data" / "duckdb" / "fedlearn.duckdb"
VIEW_NAME = "v_features_icu_stay_clean"

CONFIG_DIR = PROJECT_ROOT / "configs"

CENTRAL_MODEL_FILES = {
    "Logistic Regression": CONFIG_DIR / "centralized_logreg.pkl",
    "Random Forest": CONFIG_DIR / "centralized_rf.pkl",
    "Gradient Boosting": CONFIG_DIR / "centralized_gb.pkl",
    "SGD Classifier": CONFIG_DIR / "centralized_sgd.pkl",
}

FED_MODEL_PATH = CONFIG_DIR / "federated_sgd.pkl"

TARGET_COL = "prolonged_stay"
DROP_COLS = ["patientunitstayid", "los_days", "prolonged_stay", "apacheadmissiondx"]


@st.cache_resource
def load_data():
    """
    Load data from DuckDB, annotate categoricals, and create a train/test split.
    """
    conn = duckdb.connect(DUCKDB_PATH, read_only=True)
    try:
        df = conn.execute(f"SELECT * FROM {VIEW_NAME}").df()
    finally:
        conn.close()

    # normalize pandas.NA -> np.nan so sklearn imputers are happy
    df = df.where(df.notna(), np.nan)

    # ensure categorical columns have right categories
    df = annotate_categorical_columns(df)

    if TARGET_COL not in df.columns:
        raise RuntimeError(f"Target column '{TARGET_COL}' not found in dataframe")

    y = df[TARGET_COL]
    X = df.drop(columns=DROP_COLS)

    # 80/20 train/test split for the app
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    return X_train, X_test, y_train, y_test


def compute_metrics(model, X_train, y_train, X_test, y_test) -> dict:
    """
    Compute simple classification metrics for train and test sets.
    Assumes the model is already fit.
    """
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    pr_train, rc_train, f1_train, _ = precision_recall_fscore_support(
        y_train, y_pred_train, average="macro", zero_division=0
    )
    pr_test, rc_test, f1_test, _ = precision_recall_fscore_support(
        y_test, y_pred_test, average="macro", zero_division=0
    )

    return {
        "train_accuracy": train_acc,
        "test_accuracy": test_acc,
        "train_precision": pr_train,
        "train_recall": rc_train,
        "train_f1": f1_train,
        "test_precision": pr_test,
        "test_recall": rc_test,
        "test_f1": f1_test,
    }


@st.cache_resource
def prepare_models():
    """
    Load pre-trained centralized and federated models from disk and compute metrics.
    """
    X_train, X_test, y_train, y_test = load_data()

    models: dict[str, object] = {}
    metrics: dict[str, dict] = {}

    # load centralized models
    for name, path in CENTRAL_MODEL_FILES.items():
        if path.exists():
            try:
                mdl = joblib.load(path)
                models[name] = mdl
                metrics[name] = compute_metrics(mdl, X_train, y_train, X_test, y_test)
            except Exception as e:
                print(f"Failed to load {name} from {path}: {e}")
        else:
            print(f"Model file for {name} not found at {path}")

    # load the federated model (Flower SGD) if present
    if FED_MODEL_PATH.exists():
        try:
            fed_model = joblib.load(FED_MODEL_PATH)
            models["Federated (Flower SGD)"] = fed_model
            metrics["Federated (Flower SGD)"] = compute_metrics(
                fed_model, X_train, y_train, X_test, y_test
            )
        except Exception as e:
            print(f"Failed to load federated model from {FED_MODEL_PATH}: {e}")
    else:
        print(f"No federated model found at {FED_MODEL_PATH}")

    if not models:
        raise RuntimeError(
            "No models were loaded. Make sure you have trained and saved the "
            "centralized and/or federated models into the configs/ directory."
        )

    return models, metrics, X_test, y_test


# Streamlit UI
#
st.set_page_config(
    page_title="ICU Prolonged Stay – Centralized vs Federated",
    layout="wide",
)

st.title("ICU Prolonged Stay Prediction")
st.caption("Centralized vs Federated Learning (Flower) Demo")

st.markdown("""
This app presents the results of our **ICU prolonged stay prediction project**, where we compare
centralized machine-learning models with a **federated learning** approach. It provides an interactive
interface to explore model behavior, evaluate performance, and demonstrate how federated learning can
support privacy-preserving healthcare analytics.

With this UI, you can:

- Compare **centralized vs federated** model performance on the same test set  
- Review **train/test accuracy, precision, recall, and F1** for all models side-by-side  
- Visualize overall performance trends through a **test-accuracy bar chart**  
- Inspect an individual ICU stay and see **true vs predicted outcomes**  
- Explore how each model responds to the same patient case  
""")

with st.spinner("Loading data and models (cached)..."):
    models, metrics, X_test, y_test = prepare_models()

model_names = list(models.keys())

st.sidebar.header("Model selection")
selected_model_name = st.sidebar.selectbox(
    "Choose which model to inspect",
    options=model_names,
)

selected_model = models[selected_model_name]
selected_metrics = metrics[selected_model_name]

st.sidebar.markdown("---")
st.sidebar.markdown("**About this app**")
st.sidebar.markdown("""
- Data: `v_features_icu_stay_clean` (DuckDB)  
- Target: `prolonged_stay`  
- Centralized: LogReg / RF / GB / SGD pipelines saved as `.pkl`  
- Federated: SGDClassifier trained with Flower (`federated_sgd.pkl`)
""")

# Overall performance for selected model
#
st.subheader("1. Held-out test performance (selected model)")

cols = st.columns(4)
cols[0].metric("Train accuracy", f"{selected_metrics['train_accuracy']:.3f}")
cols[1].metric("Test accuracy", f"{selected_metrics['test_accuracy']:.3f}")
cols[2].metric("Test F1 (macro)", f"{selected_metrics['test_f1']:.3f}")
cols[3].metric("Test recall (macro)", f"{selected_metrics['test_recall']:.3f}")

st.markdown("""
Use the dropdown in the sidebar to switch between the centralized models (LogReg / RF / GB / SGD)
and the federated model. All models are evaluated on the **same** test split.
""")

metrics_df = pd.DataFrame({
    "train": {
        "accuracy": selected_metrics["train_accuracy"],
        "precision": selected_metrics["train_precision"],
        "recall": selected_metrics["train_recall"],
        "f1": selected_metrics["train_f1"],
    },
    "test": {
        "accuracy": selected_metrics["test_accuracy"],
        "precision": selected_metrics["test_precision"],
        "recall": selected_metrics["test_recall"],
        "f1": selected_metrics["test_f1"],
    },
})
st.dataframe(metrics_df.style.format("{:.3f}"), use_container_width=True)

# Model comparison overview (all models side-by-side)
#
st.subheader("1a. Model comparison overview (all models)")

base_order = [
    "Logistic Regression",
    "Random Forest",
    "Gradient Boosting",
    "SGD Classifier",
]
ordered_names = [m for m in base_order if m in metrics] + [
    m for m in metrics.keys() if m not in base_order
]

rows = []
for name in ordered_names:
    m = metrics[name]
    rows.append({
        "model": name,
        "train_accuracy": m["train_accuracy"],
        "test_accuracy": m["test_accuracy"],
        "train_precision": m["train_precision"],
        "train_recall": m["train_recall"],
        "train_f1": m["train_f1"],
        "test_precision": m["test_precision"],
        "test_recall": m["test_recall"],
        "test_f1": m["test_f1"],
    })

all_metrics_df = pd.DataFrame(rows).set_index("model")

st.dataframe(
    all_metrics_df.style.format("{:.3f}"),
    use_container_width=True,
)

# Test accuracy by model (bar chart)
#
st.subheader("1b. Test accuracy by model (bar chart)")

chart_df = all_metrics_df[["test_accuracy"]].sort_values(
    "test_accuracy", ascending=False
)
st.bar_chart(chart_df)

# Sample patient inspection
#
st.subheader("2. Inspect a sample ICU stay from the test set")

sample_idx = st.slider(
    "Choose a test sample index",
    min_value=0,
    max_value=len(X_test) - 1,
    value=0,
    help="Pick a row from the held-out test set to inspect.",
)

x_row = X_test.iloc[[sample_idx]]  # keep as DataFrame
true_label = y_test.iloc[sample_idx]

st.markdown("**Raw feature values for this patient:**")
st.dataframe(x_row.T, use_container_width=True)

# predict with the selected model
pred_label = selected_model.predict(x_row)[0]

prob_msg = None
if hasattr(selected_model, "predict_proba"):
    try:
        proba = selected_model.predict_proba(x_row)[0]
        classes = list(selected_model.classes_)
        if 1 in classes:
            prob_prolonged = float(proba[classes.index(1)])
            prob_msg = f"P(prolonged stay = 1) = {prob_prolonged:.3f}"
    except Exception:
        prob_msg = None

st.markdown("**Model output:**")
c1, c2, c3 = st.columns(3)
c1.write(f"True label: `{true_label}`")
c2.write(f"Predicted label: `{pred_label}`")
if prob_msg:
    c3.write(prob_msg)

st.markdown("""
To make the most of this app, you can:

1. Use the slider to select an individual ICU stay and explore that patient’s feature values  
2. View the **true** `prolonged_stay` label, which indicates the actual outcome in the dataset  
3. Compare it to the model’s **predicted** label — the model’s final decision for that patient  
4. Examine the probability shown as `P(prolonged stay = 1)`, which represents the model’s estimated likelihood of a prolonged stay  
   - Probabilities ≥ 0.5 result in a predicted label of **1**  
   - Probabilities < 0.5 result in a predicted label of **0**  
5. Switch between different models in the sidebar (LogReg / RF / GB / SGD / Federated) to see how each one performs on the same patient  
6. Identify cases where a model is confident, uncertain, or incorrect  
   - Example: *True label = 1*, *Predicted label = 0*, *P = 0.313* indicates the model underestimated the risk  
7. Use these comparisons to better understand strengths, weaknesses, and performance differences between centralized and federated learning approaches  
""")

# Federated model status
#
st.subheader("3. Federated model status")

if "Federated (Flower SGD)" in models:
    st.success(
        f"Federated model loaded from `{FED_MODEL_PATH}`. "
        "These parameters were learned via Flower's FedAvg across the regional clients."
    )
else:
    st.warning(
        f"No federated model found at `{FED_MODEL_PATH}`.\n\n"
        "To enable the federated comparison:\n"
        "1. Run your Flower training (`flwr run` using `server_app.py` / `client_app.py`).\n"
        f"2. Make sure it finishes and saves `federated_sgd.pkl` into the `configs/` directory.\n"
        "3. Restart this Streamlit app."
    )
