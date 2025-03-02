from faststream.rabbit import RabbitRouter
from faststream.rabbit.annotations import RabbitBroker

from app.application.models.message import Message

route = RabbitRouter()


@route.subscriber("update")
async def start_mailing(
        messages: list[Message],
        broker: RabbitBroker,
) -> None:
    print(messages)
