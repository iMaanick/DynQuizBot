import logging

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, SubManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.domain.message import Messages

logger = logging.getLogger(__name__)


async def on_button_click(
        callback: CallbackQuery,
        button: Button,
        manager: SubManager,
) -> None:
    manager.dialog_data['id'] = int(manager.item_id)


@inject
async def on_input_text(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager,
        messages: FromDishka[Messages],
) -> None:
    current_message_id = manager.dialog_data.get('id')
    current_message = messages.get_message(current_message_id)
    if not current_message.input_handler:
        return
    manager.dialog_data["input_data"][current_message.input_handler.key] = message.text
    manager.dialog_data['id'] = current_message.input_handler.target_message_id
