from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
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
    model: SGDClassifier = pipeline.named_steps["classifier"]
    n_classes = len(CLASSES)

    # attributes expected by SGDClassifier
    model.classes_ = CLASSES
    model.coef_ = np.zeros((n_classes, N_FEATURES), dtype=np.float64)
    model.intercept_ = INIT_INTERCEPT.copy()


def get_model_params(pipeline: Pipeline) -> list[np.ndarray]:
    """
    Extract model parameters as a list of NumPy arrays.

    The order and shapes must match what set_model_params() expects.
    """
    model: SGDClassifier = pipeline.named_steps["classifier"]

    if not hasattr(model, "coef_"):
        raise RuntimeError("Classifier has no coef_. Did you call set_initial_params?")

    return [model.coef_.copy(), model.intercept_.copy()]


def set_model_params(pipeline: Pipeline, params: list[np.ndarray]) -> None:
    """
    Set model parameters from a list of NumPy arrays.

    Args:
        pipeline: The Pipeline whose classifier will be modified.
        params: [coef, intercept] as NumPy arrays.
    """
    model: SGDClassifier = pipeline.named_steps["classifier"]
    coef, intercept = params

    model.coef_ = coef.copy()
    model.intercept_ = intercept.copy()
    model.classes_ = CLASSES
