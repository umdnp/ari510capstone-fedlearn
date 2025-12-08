from flwr.app import Context
from flwr.clientapp import ClientApp
from flwr.common import Message

app = ClientApp()


@app.train()
def train(message: Message, context: Context) -> Message:
    """
    Temporary stub train function.
    """
    print("Stub train() called")
    print("Incoming message_type:", message)

    # for now, just echo the content back unchanged
    return Message(message.content, reply_to=message)


@app.evaluate()
def evaluate(message: Message, context: Context) -> Message:
    """
    Temporary stub evaluate function.
    """
    print("Stub evaluate() called")
    print("Incoming message_type:", message)

    # echo the content back as well
    return Message(message.content, reply_to=message)
