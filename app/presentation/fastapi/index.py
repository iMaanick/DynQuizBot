from dataclasses import dataclass

from adaptix._internal.conversion.facade.func import get_converter
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.application.models.message import Message
from app.application.use_cases.update_messages import UpdateMessagesUseCase, UpdateMessagesIntputDTO
from app.domain import message

index_router = APIRouter()


@dataclass
class UpdateResponse:
    status: str


@index_router.post("/res", response_model=UpdateResponse)
@inject
async def update_messages(
        messages: list[Message],
        use_case: FromDishka[UpdateMessagesUseCase],
) -> UpdateResponse:
    converter = get_converter(list[Message], list[message.Message])
    await use_case(
        UpdateMessagesIntputDTO(
            converter(messages)
        )
    )
    return UpdateResponse("messages published")
