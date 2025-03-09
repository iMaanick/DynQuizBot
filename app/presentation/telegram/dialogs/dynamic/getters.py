from typing import Any

from aiogram.types import User
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.domain.message import Messages
from app.domain.user_set import UserSet


@inject
async def get_dynamic(
        dialog_manager: DialogManager,
        messages: FromDishka[Messages],
        user_set: FromDishka[UserSet],
        user: FromDishka[User],
        **kwargs
) -> dict[str, Any]:
    if "id" not in dialog_manager.dialog_data:
        user_set.add(user)
        dialog_manager.dialog_data["id"] = dialog_manager.start_data["id"]
        dialog_manager.dialog_data["input_data"] = {}
    current_message_id = dialog_manager.dialog_data["id"]
    current_message = messages.get_message(current_message_id)
    res = [button.to_dict() for button in current_message.buttons]
    return {
        "buttons": res,
        "text": current_message.text.format_map(dialog_manager.dialog_data["input_data"]),
        # можно перехватывать ошибку, но мне пока лень
        "button_width": current_message.button_width
    }
