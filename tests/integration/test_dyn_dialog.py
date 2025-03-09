import asyncio

import pytest
from aiogram_dialog import setup_dialogs
from aiogram_dialog.test_tools import BotClient, MockMessageManager
from aiogram_dialog.test_tools.keyboard import InlineButtonTextLocator
from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from app.domain.message import Message
from app.main.di import DialogDataProvider, TelegramBotUseCaseProvider
from tests.integration.conftest import MockData


@pytest.mark.asyncio
async def test_dyn_dialog(
        test_data: MockData,
        messages: list[Message],
        message_manager: MockMessageManager,
) -> None:
    container = make_async_container(
        AiogramProvider(),
        DialogDataProvider(messages, test_data.bg_factory, test_data.bot),
        TelegramBotUseCaseProvider(),
    )
    setup_dishka(container=container, router=test_data.dp)

    mock_client = BotClient(test_data.dp, bot=test_data.bot)

    setup_dialogs(mock_client.dp, message_manager=message_manager)

    await mock_client.send('/start')
    await asyncio.sleep(0.03)

    message = message_manager.last_message()
    assert "Welcome to the bot!" in message.text

    await mock_client.send('lul')
    await asyncio.sleep(0.03)
    message = message_manager.last_message()
    assert "Welcome to the bot!" == message.text

    callback_id = await mock_client.click(message, InlineButtonTextLocator('Next'))
    await asyncio.sleep(0.03)
    message_manager.assert_answered(callback_id)
    message = message_manager.last_message()
    assert "This is the second message." == message.text

    callback_id = await mock_client.click(message, InlineButtonTextLocator('Go back'))
    await asyncio.sleep(0.03)
    message_manager.assert_answered(callback_id)
    message = message_manager.last_message()
    assert "Welcome to the bot!" == message.text

    callback_id = await mock_client.click(message, InlineButtonTextLocator('Next'))
    await asyncio.sleep(0.03)
    message_manager.assert_answered(callback_id)
    message = message_manager.last_message()
    assert "This is the second message." == message.text

    callback_id = await mock_client.click(message, InlineButtonTextLocator('Continue'))
    await asyncio.sleep(0.03)
    message_manager.assert_answered(callback_id)
    message = message_manager.last_message()
    assert "Final message." == message.text

    await mock_client.send('MNK)))')
    await asyncio.sleep(0.03)
    message = message_manager.last_message()
    assert "REAL Final message.Your text MNK" in message.text
