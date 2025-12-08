from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

# Constants

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = PROJECT_ROOT / "configs"

META_PATH = PROJECT_ROOT / "configs" / "model_meta.json"
PREPROC_PATH = CONFIG_DIR / "preprocessor.pkl"

with META_PATH.open("r", encoding="utf-8") as f:
    META = json.load(f)

N_FEATURES: int = int(META["n_features"])
CLASSES: np.ndarray = np.array(META["classes"], dtype=np.int64)
INIT_INTERCEPT: np.ndarray = np.array(META["intercept"], dtype=np.float64)


def _load_preprocessor():
    """
    Load the pre-fitted preprocessing pipeline.
    """
    return joblib.load(PREPROC_PATH)


def get_preprocessor_feature_names() -> np.ndarray:
    """
    Return the feature column names in order that the preprocessor expects.
    """
    preprocessor = _load_preprocessor()

    if isinstance(preprocessor, Pipeline):
        for name, step in preprocessor.named_steps.items():
            if isinstance(step, ColumnTransformer):
                preprocessor = step
                break

    if not isinstance(preprocessor, ColumnTransformer):
        raise TypeError(
            f"Expected a ColumnTransformer, got {type(preprocessor)}. "
            "Check what you are storing in preprocessor.pkl."
        )

    feature_names: list[str] = []

    for name, transformer, columns in preprocessor.transformers:
        if name == "remainder":
            continue

        if isinstance(columns, (list, tuple, np.ndarray, pd.Index)):
            feature_names.extend([str(c) for c in columns])
        else:
            # single column
            feature_names.append(str(columns))

    return np.array(feature_names, dtype=object)


def get_model(penalty: str, local_epochs: int) -> Pipeline:
    """
    Create the global sklearn model to be trained federatedly.

    Args:
        penalty: Regularization type for SGDClassifier ("l2", "l1", "elasticnet", or "none").
        local_epochs: Number of passes over the LOCAL data per round (max_iter).

    Returns:
        A Pipeline(preprocessor -> SGDClassifier).
    """
    preprocessor = _load_preprocessor()

    model = SGDClassifier(
        loss="log_loss",  # logistic regression-style
        penalty=penalty,
        max_iter=local_epochs,  # how many epochs each client runs per round
        learning_rate="optimal",
        class_weight="balanced",
        n_jobs=-1,
        random_state=42,
        warm_start=True,
    )

    model.classes_ = CLASSES

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model),
        ]
    )


def set_initial_params(pipeline: Pipeline) -> None:
    """
    Initialize the model's parameters using model_meta.json.

    Uses:
      - N_FEATURES: preprocessed feature dimension
      - CLASSES:    label set (e.g. [0, 1])
      - INIT_INTERCEPT: initial intercept vector (usually zeros)
    """
    clf: SGDClassifier = pipeline.named_steps["classifier"]
    n_classes = len(CLASSES)

    clf.classes_ = CLASSES

    if n_classes <= 2:
        # binary case: SGDClassifier stores coef_ as (n_features,)
        # and intercept_ as a single bias term of shape (1,)
        clf.coef_ = np.zeros(N_FEATURES, dtype=np.float64)

        if INIT_INTERCEPT.size > 0:
            b0 = float(INIT_INTERCEPT.ravel()[0])
        else:
            b0 = 0.0

        clf.intercept_ = np.array([b0], dtype=np.float64)
    else:
        # multiclass case: shape (n_classes, n_features) and (n_classes,)
        clf.coef_ = np.zeros((n_classes, N_FEATURES), dtype=np.float64)

        if INIT_INTERCEPT.shape == (n_classes,):
            clf.intercept_ = INIT_INTERCEPT.astype(np.float64).copy()
        else:
            raise RuntimeError(
                f"INIT_INTERCEPT shape {INIT_INTERCEPT.shape} does not match number of classes {n_classes}"
            )


def get_model_params(pipeline: Pipeline) -> list[np.ndarray]:
    """
    Extract model parameters as a list of NumPy arrays.

    The order and shapes must match what set_model_params() expects.
    """
    clf: SGDClassifier = pipeline.named_steps["classifier"]

    if not hasattr(clf, "coef_"):
        raise RuntimeError("Classifier has no coef_. Did you call set_initial_params?")

    return [clf.coef_.copy(), clf.intercept_.copy()]


def set_model_params(pipeline: Pipeline, params: list[np.ndarray]) -> None:
    """
    Set model parameters from a list of NumPy arrays.

    Args:
        pipeline: The Pipeline whose classifier will be modified.
        params: [coef, intercept] as NumPy arrays.
    """
    clf: SGDClassifier = pipeline.named_steps["classifier"]
    coef, intercept = params
    clf.coef_ = coef.copy()
    clf.intercept_ = intercept.copy()
    clf.classes_ = CLASSES
