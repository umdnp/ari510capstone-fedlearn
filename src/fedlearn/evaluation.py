from __future__ import annotations

from typing import Any, Mapping

from sklearn.metrics import accuracy_score, precision_recall_fscore_support


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
    Fit the model, generate predictions, and compute basic classification metrics.

    Args:
        name: Label used when printing results.
        model: Any scikit-learn style estimator with fit/predict methods.
        X_train: Training features.
        y_train: Training labels.
        X_test: Test features.
        y_test: Test labels.
        average: Averaging mode for precision/recall/F1 (default: "macro").
        zero_division: How to handle zero-division in metrics (default: 0).
        verbose: If True, print metrics to stdout.

    Returns:
        A mapping with accuracy, precision, recall, and f1.
    """
    # train
    model.fit(X_train, y_train)

    # predict
    y_pred = model.predict(X_test)

    # metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average=average, zero_division=zero_division
    )

    metrics = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
    }

    if verbose:
        print(f"{name}")
        print("-" * 40)
        print(f"Accuracy  : {accuracy:.4f}")
        print(f"Precision : {precision:.4f}")
        print(f"Recall    : {recall:.4f}")
        print(f"F1-score  : {f1:.4f}")
        print()

    return metrics
