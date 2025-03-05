from aiogram import Dispatcher, Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.domain.message import Messages
from app.presentation.telegram.states import Dynamic


@inject
async def start_cmd(
        message: Message,
        dialog_manager: DialogManager,
        messages: FromDishka[Messages]
) -> None:
    target_message = messages.command_to_message.get(message.text, None)
    if target_message is not None:
        await dialog_manager.start(Dynamic.dyn_state, mode=StartMode.RESET_STACK,
                                   data={"id": target_message.message_id})


def setup_start(dp: Dispatcher) -> None:
    router = Router(name=__name__)
    router.message.register(start_cmd, F.func(lambda m: m.text.startswith("/")), F.chat.type.in_({"private"}))
    dp.include_router(router)
