from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import SGDClassifier

# Constants

PROJECT_ROOT = Path(__file__).resolve().parents[2]
META_PATH = PROJECT_ROOT / "configs" / "model_meta.json"

with META_PATH.open("r", encoding="utf-8") as f:
    META = json.load(f)

N_FEATURES: int = int(META["n_features"])
CLASSES: np.ndarray = np.array(META["classes"], dtype=np.int64)
INIT_INTERCEPT: np.ndarray = np.array(META["intercept"], dtype=np.float64)


def get_model(penalty: str, local_epochs: int) -> SGDClassifier:
    """Create the global sklearn model to be trained federatedly.

    Args:
        penalty: Regularization type for SGDClassifier ("l2", "l1", "elasticnet", or "none").
        local_epochs: Number of passes over the LOCAL data per round (max_iter).

    Returns:
        An uninitialized SGDClassifier which will behave like logistic regression
        (because we use loss="log_loss").
    """
    model = SGDClassifier(
        loss="log_loss",  # logistic regression-style
        penalty=penalty,
        max_iter=local_epochs,  # how many epochs each client runs per round
        learning_rate="optimal",
        class_weight="balanced",
        random_state=42,
    )
    return model


def set_initial_params(model: SGDClassifier) -> None:
    """Initialize the model's parameters using model_meta.json.

    Uses:
      - N_FEATURES: preprocessed feature dimension
      - CLASSES:    label set (e.g. [0, 1])
      - INIT_INTERCEPT: initial intercept vector (usually zeros)
    """
    n_classes = len(CLASSES)

    # attributes expected by SGDClassifier
    model.classes_ = CLASSES
    model.coef_ = np.zeros((n_classes, N_FEATURES), dtype=np.float64)
    model.intercept_ = INIT_INTERCEPT.copy()


def get_model_params(model: SGDClassifier) -> list[np.ndarray]:
    """Extract model parameters as a list of NumPy arrays.

    The order and shapes must match what set_model_params() expects.
    """
    return [model.coef_.copy(), model.intercept_.copy()]


def set_model_params(model: SGDClassifier, params: list[np.ndarray]) -> None:
    """Set model parameters from a list of NumPy arrays.

    Args:
        model: The SGDClassifier to modify.
        params: [coef, intercept] as NumPy arrays.
    """
    coef, intercept = params

    model.coef_ = coef.copy()
    model.intercept_ = intercept.copy()
    model.classes_ = CLASSES
