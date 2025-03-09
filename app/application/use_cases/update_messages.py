from dataclasses import dataclass

from adaptix import Retort
from faststream.rabbit import RabbitBroker

from app.domain.message import Message


@dataclass
class UpdateMessagesIntputDTO:
    messages: list[Message]


class UpdateMessagesUseCase:
    def __init__(
            self,
            broker: RabbitBroker,
    ) -> None:
        self.broker = broker
        self.retort = Retort()

    async def __call__(self, data: UpdateMessagesIntputDTO) -> None:
        await self.broker.publish(
            self.retort.dump(data.messages, list[Message]),
            queue="update"
        )
