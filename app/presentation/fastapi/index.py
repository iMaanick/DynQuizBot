from fastapi import APIRouter, Request
from faststream.rabbit import RabbitBroker

from app.application.models.message import Message

index_router = APIRouter()


@index_router.post("/res")
async def index(
        request: Request,
        messages: list[Message],
) -> dict:
    broker: RabbitBroker = request.state.broker

    await broker.publish(
        [message.model_dump() for message in messages],
        queue="update"
    )
    return {"status": "messages published"}
