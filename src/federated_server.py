import flwr as fl

# Constants

NUM_ROUNDS = 5
NUM_CLIENTS = 3  # must match the number of clients you actually run


def weighted_average(metrics: list[tuple[int, dict[str, float]]]) -> dict[str, float]:
    """
    Weighted average of client metrics by number of examples.
    """
    if not metrics:
        return {}

    total_examples = sum(num_examples for num_examples, _ in metrics)

    def avg(key: str) -> float:
        return sum(num_examples * m[key] for num_examples, m in metrics) / total_examples

    return {
        "accuracy": avg("accuracy"),
        "precision": avg("precision"),
        "recall": avg("recall"),
        "f1": avg("f1"),
    }


def main() -> None:
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0,  # use all clients for training
        fraction_evaluate=1.0,  # use all clients for evaluation
        min_fit_clients=NUM_CLIENTS,
        min_evaluate_clients=NUM_CLIENTS,
        min_available_clients=NUM_CLIENTS,
        evaluate_metrics_aggregation_fn=weighted_average,
    )

    print(f"Starting server for {NUM_ROUNDS} rounds, expecting {NUM_CLIENTS} clients ...")

    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=NUM_ROUNDS),
        strategy=strategy,
    )


if __name__ == "__main__":
    main()
