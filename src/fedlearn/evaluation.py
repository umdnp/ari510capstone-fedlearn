from __future__ import annotations

from time import perf_counter
from typing import Any, Mapping, Dict

from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def _compute_metrics(
        y_true,
        y_pred,
        average: str = "macro",
        zero_division: int = 0,
) -> Dict[str, float]:
    """
    Helper to avoid duplicating metric code.
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average=average, zero_division=zero_division
    )
    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
    }


def evaluate_model(
        name: str,
        model: Any,
        X_train,
        y_train,
        X_test,
        y_test,
        average: str = "macro",
        zero_division: int = 0,
        verbose: bool = True,
) -> Mapping[str, float]:
    """
    Fit the model, generate predictions, and compute basic classification
    metrics for both training and test sets.

    Returns:
        A mapping with train_* and test_* metrics.
    """
    # train
    t0 = perf_counter()
    model.fit(X_train, y_train)
    train_time = perf_counter() - t0

    model.fit(X_train, y_train)

    # predict on train and test
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # metrics
    train_metrics = _compute_metrics(
        y_train, y_pred_train, average=average, zero_division=zero_division
    )
    test_metrics = _compute_metrics(
        y_test, y_pred_test, average=average, zero_division=zero_division
    )

    # combine in a single dict
    metrics: Dict[str, float] = {
        "train_time": float(train_time),
        **{f"train_{k}": v for k, v in train_metrics.items()},
        **{f"test_{k}": v for k, v in test_metrics.items()},
    }


    if verbose:
        print(f"{name}")
        print("-" * 40)
        print(f"Train time: {train_time:.3f}s")
        print("Train set:")
        print(f"  Accuracy  : {train_metrics['accuracy']:.4f}")
        print(f"  Precision : {train_metrics['precision']:.4f}")
        print(f"  Recall    : {train_metrics['recall']:.4f}")
        print(f"  F1-score  : {train_metrics['f1']:.4f}")
        print()
        print("Test set:")
        print(f"  Accuracy  : {test_metrics['accuracy']:.4f}")
        print(f"  Precision : {test_metrics['precision']:.4f}")
        print(f"  Recall    : {test_metrics['recall']:.4f}")
        print(f"  F1-score  : {test_metrics['f1']:.4f}")
        print()

    return metrics
