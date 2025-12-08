from flwr.app import Context
from flwr.clientapp import ClientApp
from flwr.common import Message, ArrayRecord, MetricRecord, RecordDict

app = ClientApp()


@app.train()
def train(message: Message, context: Context) -> Message:
    incoming_arrays: ArrayRecord = message.content["arrays"]

    # for a stub, just echo the same parameters back
    updated_arrays = incoming_arrays

    metrics = MetricRecord({
        "num-examples": 1.0,
        "loss": 0.0,
    })

    # build the reply
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
    Temporary stub evaluate function.
    """
    print("Stub evaluate() called")

    metrics = MetricRecord({
        "num-examples": 1.0,  # again, must be > 0
        "loss": 0.0,
        "accuracy": 0.0,
    })

    reply_content = RecordDict({
        "metrics": metrics,
    })

    return Message(
        content=reply_content,
        reply_to=message,
    )
