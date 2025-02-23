from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.presentation.telegram.states import Dynamic


async def start_cmd(
        message: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(Dynamic.dyn_state, mode=StartMode.RESET_STACK)


def setup_start(dp: Dispatcher) -> None:
    router = Router(name=__name__)
    router.message.register(start_cmd, Command("start"), F.chat.type.in_({"private"}))
    dp.include_router(router)
