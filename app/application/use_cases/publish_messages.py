from dataclasses import dataclass

from adaptix import Retort
from faststream.rabbit import RabbitBroker

from app.domain.message import Message


@dataclass
class PublishMessagesIntputDTO:
    messages: list[Message]


class PublishMessagesUseCase:
    def __init__(
            self,
            broker: RabbitBroker,
    ) -> None:
        self.broker = broker
        self.retort = Retort()

    async def __call__(self, data: PublishMessagesIntputDTO) -> None:
        await self.broker.publish(
            self.retort.dump(data.messages, list[Message]),
            queue="update"
        )
