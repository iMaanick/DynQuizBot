from aiogram import Dispatcher

from app.domain.message import Message
from app.presentation.telegram.handlers.error import setup_handle_error
from app.presentation.telegram.handlers.start import setup_start


def setup_handlers(dp: Dispatcher, messages: list[Message]) -> None:
    setup_start(dp, messages)
    setup_handle_error(dp)
