from aiogram import Bot
from aiogram.types import TelegramObject, User
from aiogram_dialog import BgManagerFactory
from dishka import Scope, Provider, provide
from fastapi import Request
from faststream.rabbit import RabbitBroker

from app.domain.message import Message, Messages
from app.domain.user_set import UserSet


class DialogDataProvider(Provider):
    def __init__(self, message_data: list[Message], bg_factory: BgManagerFactory, bot: Bot, ) -> None:
        super().__init__()
        self.message_data = message_data
        self.bg_factory = bg_factory
        self.bot = bot

    @provide(scope=Scope.APP)
    async def message_data(self) -> dict[int, Message]:
        message_data: dict[int, Message] = {}
        for message in self.message_data:
            message_data[message.message_id] = message
        return message_data

    @provide(scope=Scope.REQUEST)
    async def get_user(self, obj: TelegramObject) -> User:
        return obj.from_user

    @provide(scope=Scope.APP)
    async def user_set(self) -> UserSet:
        return UserSet()

    @provide(scope=Scope.REQUEST)
    async def get_bg_factory(self) -> BgManagerFactory:
        return self.bg_factory

    @provide(scope=Scope.APP)
    async def get_bot(self) -> Bot:
        return self.bot

    messages = provide(Messages, scope=Scope.APP)


class BrokerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_broker(self, request: Request) -> RabbitBroker:
        return request.state.broker
