from aiogram.types import TelegramObject, User
from dishka import Scope, Provider, provide
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.domain.message import Message, Messages


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user(self, obj: TelegramObject) -> User:
        return obj.from_user


class DialogDataProvider(Provider):

    def __init__(self, message_data: list[Message]):
        super().__init__()
        self.message_data = message_data

    @provide(scope=Scope.APP)
    async def message_data(self) -> dict[int, Message]:
        message_data: dict[int, Message] = {}
        for message in self.message_data:
            message_data[message.message_id] = message
        return message_data

    messages = provide(Messages, scope=Scope.REQUEST)
