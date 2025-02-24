from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.domain.message import Messages


@inject
async def get_dynamic(dialog_manager: DialogManager, messages: FromDishka[Messages], **kwargs) -> dict[str, Any]:
    current_message_id = dialog_manager.dialog_data.get('id', 1)
    current_message = messages.get_message(current_message_id)
    res = [button.to_dict() for button in current_message.buttons]
    return {
        "buttons": res,
        "buttons_exits": len(res) > 0,
        "text": current_message.text,
        "button_width": current_message.button_width
    }
