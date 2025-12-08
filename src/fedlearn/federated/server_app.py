from __future__ import annotations

from pathlib import Path

import joblib
from flwr.app import ArrayRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg

from fedlearn.federated.utils import (
    get_model,
    get_model_params,
    set_initial_params,
    set_model_params,
)

app = ServerApp()

# Constants

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = PROJECT_ROOT / "configs"
MODEL_PATH = CONFIG_DIR / "final_model.pkl"


@app.main()
def main(grid: Grid, context: Context) -> None:
    # make sure configs dir exists
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # read run config from pyproject.toml or cli
    num_rounds: int = context.run_config["num-server-rounds"]
    penalty: str = context.run_config["penalty"]
    local_epochs: int = context.run_config["local-epochs"]

    fraction_train: float = context.run_config.get("fraction-train", 1.0)
    fraction_evaluate: float = context.run_config.get("fraction-evaluate", 1.0)

    # create and initialize model
    model = get_model(penalty=penalty, local_epochs=local_epochs)
    set_initial_params(model)

    arrays = ArrayRecord(get_model_params(model))

    # initialize FedAvg strategy
    strategy = FedAvg(
        fraction_train=fraction_train,
        fraction_evaluate=fraction_evaluate,
    )

    # run federated training
    result = strategy.start(
        grid=grid,
        initial_arrays=arrays,
        num_rounds=num_rounds,
    )

    # get final global params and save model
    final_params = result.arrays.to_numpy_ndarrays()
    set_model_params(model, final_params)

    print(f"Saving final model to {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)
