from __future__ import annotations

from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from flwr.app import Context
from flwr.clientapp import ClientApp
from flwr.common import Message, RecordDict, ArrayRecord, MetricRecord
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split

from fedlearn.federated.utils import (
    get_model,
    get_model_params,
    set_model_params,
)

app = ClientApp()

# Constants

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DUCKDB_PATH = PROJECT_ROOT / "data" / "duckdb" / "fedlearn.duckdb"
VIEW_NAME = "v_features_icu_stay_clean"

TARGET_COL = "prolonged_stay"
DROP_COLS = ["patientunitstayid", "los_days", "prolonged_stay", "apacheadmissiondx"]
REGION_COL = "hospital_region"

CLIENT_REGION_MAP = {
    "client_midwest": ["Midwest"],
    "client_south": ["South"],
    "client_other": ["West", "Northeast", "Unknown"],
}

# Partitioning scheme
# partition-id = 0 -> client_midwest
# partition-id = 1 -> client_south
# partition-id = 2 -> client_other
CLIENT_KEYS = ["client_midwest", "client_south", "client_other"]


def _get_client_key(context: Context) -> str:
    """
    Map Flower's partition-id to our logical client bucket name.
    """
    partition_id = int(context.node_config["partition-id"])
    try:
        return CLIENT_KEYS[partition_id]
    except IndexError:
        raise RuntimeError(
            f"partition-id={partition_id} out of range for CLIENT_KEYS={CLIENT_KEYS}"
        )


def _load_client_data(context: Context) -> pd.DataFrame:
    """
    Load only this client's partition from DuckDB.

    The mapping is:
      partition-id -> client bucket -> list of raw regions.

    Example:
      partition-id=0 -> "client_midwest" -> ["Midwest"]
      partition-id=1 -> "client_south"   -> ["South"]
      partition-id=2 -> "client_other"   -> ["West", "Northeast", "Unknown"]
    """
    client_key = _get_client_key(context)
    regions = CLIENT_REGION_MAP[client_key]

    conn = duckdb.connect(DUCKDB_PATH, read_only=True)
    try:
        placeholders = ", ".join(["?"] * len(regions))
        query = f"""
            SELECT *
            FROM {VIEW_NAME}
            WHERE {REGION_COL} IN ({placeholders})
        """
        df = conn.execute(query, regions).df()
    finally:
        conn.close()

    # normalize pandas.NA -> np.nan so sklearn imputers are happy
    df = df.where(df.notna(), np.nan)
    return df


def _get_train_eval_data(
        context: Context,
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Load this client's local data and split into train/eval sets.
    """
    df = _load_client_data(context)

    if df.empty:
        raise RuntimeError("No rows found for this client's partition")

    y = df[TARGET_COL]
    X = df.drop(columns=DROP_COLS, errors="ignore")

    X_train, X_eval, y_train, y_eval = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() > 1 else None
    )

    return X_train, y_train, X_eval, y_eval


@app.train()
def train(message: Message, context: Context) -> Message:
    """
    Perform one round of local training for this client.

    Steps:
      1) Load global model parameters from the server.
      2) Initialize the local model with those parameters.
      3) Load this client's local train/eval data.
      4) Train for `local-epochs` on the local training data.
      5) Compute metrics on the local eval data.
      6) Return updated parameters and metrics to the server.
    """
    incoming_arrays = message.content["arrays"]
    penalty = context.run_config["penalty"]
    local_epochs = context.run_config["local-epochs"]

    # create model using shared run_config
    model = get_model(penalty=penalty, local_epochs=local_epochs)
    set_model_params(model, incoming_arrays.to_numpy_ndarrays())

    # load local train/eval data for this client
    X_train, y_train, X_eval, y_eval = _get_train_eval_data(context)

    # local training
    for _ in range(local_epochs):
        model.fit(X_train, y_train)

    # compute metrics on eval split
    y_pred = model.predict(X_eval)
    acc = float(accuracy_score(y_eval, y_pred))

    try:
        y_proba = model.predict_proba(X_eval)
        loss = float(log_loss(y_eval, y_proba))
    except Exception:
        loss = 0.0

    num_examples = float(len(X_train))

    metrics = MetricRecord({
        "num-examples": num_examples,
        "loss": loss,
        "accuracy": acc,
    })

    # extract updated model params
    updated_arrays = ArrayRecord(get_model_params(model))

    reply_content = RecordDict({
        "arrays": updated_arrays,
        "metrics": metrics,
    })

    reply_message = Message(
        content=reply_content,
        reply_to=message,
    )

    return reply_message


@app.evaluate()
def evaluate(message: Message, context: Context) -> Message:
    """
    Local evaluation using current global parameters.

    This uses the same partitioning logic and eval split as `train`,
    but does not perform any further training.
    """
    incoming_arrays = message.content["arrays"]
    penalty = context.run_config["penalty"]
    local_epochs = context.run_config["local-epochs"]

    # recreate model and load parameters
    model = get_model(penalty=penalty, local_epochs=local_epochs)
    set_model_params(model, incoming_arrays.to_numpy_ndarrays())

    # load local eval data
    _, _, X_eval, y_eval = _get_train_eval_data(context)

    # compute metrics
    y_pred = model.predict(X_eval)
    acc = float(accuracy_score(y_eval, y_pred))

    try:
        y_proba = model.predict_proba(X_eval)
        loss = float(log_loss(y_eval, y_proba))
    except Exception:
        loss = 0.0

    num_examples = float(len(X_eval))

    metrics = MetricRecord({
        "num-examples": num_examples,
        "loss": loss,
        "accuracy": acc,
    })

    reply_content = RecordDict({
        "metrics": metrics,
    })

    return Message(
        content=reply_content,
        reply_to=message,
    )
