from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request
from faststream.rabbit import RabbitBroker

from app.application.models.message import Message

index_router = APIRouter()


@index_router.post("/res")
@inject
async def index(
        request: Request,
        messages: list[Message],
        broker: FromDishka[RabbitBroker],
) -> dict:
    await broker.publish(
        [message.model_dump() for message in messages],
        queue="update"
    )
    return {"status": "messages published"}
