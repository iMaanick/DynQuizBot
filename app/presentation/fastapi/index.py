from fastapi import APIRouter, Request

from app.application.models.message import Message

index_router = APIRouter()


@index_router.post("/res")
def index(
        request: Request,
        messages: list[Message],
) -> dict:
    broker = request.state.broker

    broker.publish("update", [message.model_dump() for message in messages])

    return {"status": "messages published"}
