from dataclasses import dataclass

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from faststream.rabbit import RabbitBroker

from app.application.models.message import Message

index_router = APIRouter()


@dataclass
class UpdateResponse:
    status: str


@index_router.post("/res", response_model=UpdateResponse)
@inject
async def update_messages(
        messages: list[Message],
        broker: FromDishka[RabbitBroker],
) -> UpdateResponse:
    await broker.publish(
        [message.model_dump() for message in messages],
        queue="update"
    )
    return UpdateResponse("messages published")
