import asyncio

import pytest
from aiogram_dialog import setup_dialogs
from aiogram_dialog.test_tools import BotClient, MockMessageManager


@pytest.mark.asyncio
async def test_add_timecode_dialog(
        mock_client: BotClient,
) -> None:
    message_manager = MockMessageManager()
    setup_dialogs(mock_client.dp, message_manager=message_manager)
    await mock_client.send('/start')
    await asyncio.sleep(0.03)
    message = message_manager.last_message()
    assert "Welcome to the bot!" in message.text
