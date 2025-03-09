from aiogram import Dispatcher, Router
from aiogram_dialog import setup_dialogs, BgManagerFactory

from app.presentation.telegram.dialogs.dialogs.dynamic_dialog import setup_dynamic_dialog


def setup_all_dialogs(dp: Dispatcher) -> BgManagerFactory:
    dialog_router = Router()
    setup_dynamic_dialog(dialog_router)
    dp.include_router(dialog_router)
    bg_factory = setup_dialogs(dp)
    return bg_factory
