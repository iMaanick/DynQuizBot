import asyncio

import pytest
from aiogram_dialog import setup_dialogs
from aiogram_dialog.test_tools import BotClient, MockMessageManager
from aiogram_dialog.test_tools.keyboard import InlineButtonTextLocator
from dishka import make_async_container
from dishka.integrations import faststream as faststream_integration
from dishka.integrations.aiogram import AiogramProvider, setup_dishka
from faststream import FastStream
from faststream.rabbit import TestRabbitBroker

from app.domain.message import Message
from app.main.di import DialogDataProvider, TelegramBotUseCaseProvider
from app.presentation.faststream.update import update_router
from tests.integration.conftest import MockData


@pytest.mark.asyncio
async def test_dyn_dialog_with_broker(
        test_data: MockData,
        messages: list[Message],
) -> None:
    container = make_async_container(
        AiogramProvider(),
        DialogDataProvider(messages, test_data.bg_factory, test_data.bot),
        TelegramBotUseCaseProvider(),
    )
    setup_dishka(container=container, router=test_data.dp)
    mock_client = test_data.mock_client
    message_manager = test_data.message_manager

    async with TestRabbitBroker(test_data.broker) as br:
        br.include_router(update_router)
        faststream_app = FastStream(br)
        faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
        await faststream_app.start()

        await mock_client.send('/start')
        await asyncio.sleep(0.03)

        message = message_manager.last_message()
        assert message.text == "Welcome to the bot!"

        await mock_client.send('lul')
        await asyncio.sleep(0.03)
        message = message_manager.last_message()
        assert message.text == "Welcome to the bot!"

        callback_id = await mock_client.click(message, InlineButtonTextLocator('Next'))
        await asyncio.sleep(0.03)
        message_manager.assert_answered(callback_id)
        message = message_manager.last_message()
        assert message.text == "This is the second message."

        callback_id = await mock_client.click(message, InlineButtonTextLocator('Go back'))
        await asyncio.sleep(0.03)
        message_manager.assert_answered(callback_id)
        message = message_manager.last_message()
        assert message.text == "Welcome to the bot!"

        callback_id = await mock_client.click(message, InlineButtonTextLocator('Next'))
        await asyncio.sleep(0.03)
        message_manager.assert_answered(callback_id)
        message = message_manager.last_message()
        assert message.text == "This is the second message."

        callback_id = await mock_client.click(message, InlineButtonTextLocator('Continue'))
        await asyncio.sleep(0.03)
        message_manager.assert_answered(callback_id)
        message = message_manager.last_message()
        assert message.text == "Final message."

        await mock_client.send('MNK)))')
        await asyncio.sleep(0.03)
        message = message_manager.last_message()
        assert message.text == "REAL Final message.Your text MNK)))"

        data = [
            {
                "message_id": 1,
                "text": "New MESSAGE",
                "command": "/start",
            },
        ]
        await br.publish(data, queue="update")

        await mock_client.send('/start')
        await asyncio.sleep(0.03)
        message = message_manager.last_message()
        assert message.text == "New MESSAGE"

        data = [
            {
                "message_id": 1,
                "text": "New MESSAGE222",
                "command": "/start",
            },
        ]
        await br.publish(data, queue="update")

        await mock_client.send('/start')
        await asyncio.sleep(0.03)
        message = message_manager.last_message()
        assert message.text == "New MESSAGE222"
        await container.close()
        message_manager.reset_history()