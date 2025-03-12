from aiogram import Dispatcher

from app.presentation.telegram.handlers.error import setup_handle_error
from app.presentation.telegram.handlers.start import setup_start


def setup_handlers(dp: Dispatcher) -> None:
    setup_start(dp)
    setup_handle_error(dp)
