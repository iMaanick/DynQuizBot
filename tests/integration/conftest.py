from unittest.mock import AsyncMock

import pytest
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import TelegramObject, User
from aiogram_dialog import BgManagerFactory
from aiogram_dialog.api.internal import FakeUser
from aiogram_dialog.test_tools import BotClient
from aiogram_dialog.test_tools.bot_client import FakeBot
from dishka import Provider, provide, Scope, make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from app.application.models.message import TextHandler
from app.domain.message import Message, Messages
from app.domain.button import Button
from app.domain.user_set import UserSet
from app.presentation.telegram.dialogs import setup_all_dialogs
from app.presentation.telegram.handlers import setup_handlers


class FakeProvider(Provider):
    def __init__(
            self,
            message_data: list[Message],
            bg_factory: BgManagerFactory,
            bot: Bot,
    ) -> None:
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


@pytest.fixture(scope='package')
def messages() -> list[Message]:
    return [
        Message(
            message_id=1,
            text="Welcome to the bot!",
            command="/start",
            buttons=[
                Button(text="Next", target_message_id=2)
            ]
        ),
        Message(
            message_id=2,
            text="This is the second message.",
            buttons=[
                Button(text="Go back", target_message_id=1),
                Button(text="Continue", target_message_id=3)
            ],
            button_width=2,
            command="/second",
        ),
        Message(
            message_id=3,
            text="Final message.",
            input_handler=TextHandler(key="user_input", target_message_id=4)
        ),
        Message(
            message_id=4,
            text="REAL Final message.Your text {user_input}",
        )
    ]


@pytest.fixture(scope='package')
def fake_user() -> FakeUser:
    return FakeUser(id=321, is_bot=False, first_name='MNK', username='MNK')


@pytest.fixture(scope='package')
def mock_client(messages: list[Message], fake_user: FakeUser) -> BotClient:
    dp = Dispatcher(
        storage=MemoryStorage(),
    )
    bot = FakeBot()
    setup_handlers(dp, messages)
    bg_factory = setup_all_dialogs(dp)
    container = make_async_container(AiogramProvider(), FakeProvider(messages, bg_factory, bot))
    setup_dishka(container=container, router=dp)
    return BotClient(dp, bot=bot)
