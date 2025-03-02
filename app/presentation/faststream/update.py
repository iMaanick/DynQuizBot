from dishka import FromDishka
from faststream.rabbit import RabbitRouter
from faststream.rabbit.annotations import RabbitBroker
from app. domain import message
from app.application.models.message import Message

update_router = RabbitRouter()


@update_router.subscriber("update",
                          filter=lambda msg: msg.content_type == "application/json", )
async def update(
        message_data: list[Message],
        messages: FromDishka[message.Messages],
        broker: RabbitBroker,

) -> None:
    messages.update(message_data)
