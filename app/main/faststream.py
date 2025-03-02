from dishka import AsyncContainer
from dishka.integrations import faststream as faststream_integration
from faststream import FastStream
from faststream.rabbit import RabbitBroker


def get_faststream_app(container: AsyncContainer) -> FastStream:
    broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
    faststream_app = FastStream(broker)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    # broker.include_router()
    return faststream_app
