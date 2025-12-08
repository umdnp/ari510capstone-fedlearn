from flwr.app import Context
from flwr.clientapp import ClientApp
from flwr.common import RecordDict

app = ClientApp()


@app.main()
def main(context: Context) -> None:
    # This can be basically empty for now
    print("Federated client app started (stub).")


@app.train()
def train(context: Context) -> RecordDict:
    # Minimal no-op implementation so Flower can import it
    return RecordDict()


@app.evaluate()
def evaluate(context: Context) -> RecordDict:
    # Minimal no-op implementation
    return RecordDict()
