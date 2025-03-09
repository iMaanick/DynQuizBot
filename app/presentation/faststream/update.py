from adaptix._internal.conversion.facade.func import get_converter
from dishka import FromDishka
from faststream.rabbit import RabbitRouter

from app.application.models.message import Message
from app.application.use_cases.update_messages import UpdateMessagesUseCase, UpdateMessagesIntputDTO
from app.domain import message

update_router = RabbitRouter()


@update_router.subscriber("update",
                          filter=lambda msg: msg.content_type == "application/json", )
async def update(
        message_data: list[Message],
        use_case: FromDishka[UpdateMessagesUseCase],
) -> None:
    converter = get_converter(list[Message], list[message.Message])
    await use_case(
        UpdateMessagesIntputDTO(
            converter(message_data)
        )
    )
