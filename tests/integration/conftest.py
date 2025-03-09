from dataclasses import dataclass
from typing import AsyncGenerator

import pytest
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import BgManagerFactory
from aiogram_dialog.api.internal import FakeUser
from aiogram_dialog.test_tools import MockMessageManager
from aiogram_dialog.test_tools.bot_client import FakeBot
from aiogram_dialog.test_tools.memory_storage import JsonMemoryStorage
from asgi_lifespan import LifespanManager
from dishka import make_async_container, Provider, provide, Scope
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker, fastapi, TestRabbitBroker
from faststream.testing.broker import TestBroker
from starlette.testclient import TestClient

from app.application.models.message import TextHandler
from app.domain.button import Button
from app.domain.message import Message
from app.main import create_app
from app.main.di import FastApiUseCaseProvider
from app.main.fastapi import init_routers
from app.presentation.fastapi.root import root_router
from app.presentation.telegram.dialogs import setup_all_dialogs
from app.presentation.telegram.handlers import setup_handlers


@pytest.fixture(scope="function")
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


@pytest.fixture(scope='session')
def fake_user() -> FakeUser:
    return FakeUser(id=321, is_bot=False, first_name='MNK', username='MNK')


@pytest.fixture()
async def test_broker(broker):
    async with TestBroker(broker) as br:
        yield br


@dataclass
class MockData:
    dp: Dispatcher
    bg_factory: BgManagerFactory
    bot: FakeBot
    broker: RabbitBroker


@pytest.fixture(scope="function")
def message_manager() -> MockMessageManager:
    return MockMessageManager()


@pytest.fixture(scope="session")
async def test_data(fake_user: FakeUser, ) -> MockData:
    dp = Dispatcher(
        storage=JsonMemoryStorage(),
    )
    bot = FakeBot()
    setup_handlers(dp)
    bg_factory = setup_all_dialogs(dp)
    broker = RabbitBroker()
    return MockData(dp, bg_factory, bot, broker)


class BrokerProvider(Provider):

    def __init__(self, broker: RabbitBroker):
        self.broker = broker
        super().__init__()

    @provide(scope=Scope.REQUEST)
    async def get_broker(self) -> RabbitBroker:
        return self.broker


@pytest.fixture
async def client_fastapi() -> AsyncGenerator[TestClient, None]:
    router = fastapi.RabbitRouter("amqp://guest:guest@localhost:5672/")
    app = FastAPI()

    app.include_router(router)

    async with TestRabbitBroker(router.broker) as br:
        app.state.broker = br
        app.include_router(root_router)

        container = make_async_container(
            BrokerProvider(br),
            FastapiProvider(),
            FastApiUseCaseProvider(),
        )
        setup_dishka(container, app)
        async with LifespanManager(app):
            yield TestClient(app)
