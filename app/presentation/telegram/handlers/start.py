from functools import partial

from aiogram import Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from app.domain import message
from app.presentation.telegram.states import Dynamic


async def start_cmd(
        message_id: int,
        _: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(Dynamic.dyn_state, mode=StartMode.RESET_STACK, data={"id": message_id})


def setup_start(dp: Dispatcher, messages: list[message.Message]) -> None:
    router = Router(name=__name__)
    for message_data in messages:
        if message_data.command:
            print(message_data.command)
            router.message.register(partial(start_cmd, message_data.message_id),
                                    Command(message_data.command),
                                    F.chat.type.in_({"private"}))
    dp.include_router(router)
