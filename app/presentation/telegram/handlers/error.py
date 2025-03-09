import logging

from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

logger = logging.getLogger(__name__)


async def handle_error(
        event,
        dialog_manager: DialogManager
) -> None:
    logger.error(event.exception)


def setup_handle_error(dp: Dispatcher) -> None:
    dp.errors.register(
        handle_error,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        handle_error,
        ExceptionTypeFilter(UnknownState),
    )
