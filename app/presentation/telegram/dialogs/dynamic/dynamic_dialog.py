from aiogram import Router
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, ListGroup, Button
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import inject

from app.presentation.telegram.dialogs.dynamic.getters import get_dynamic
from app.presentation.telegram.dialogs.dynamic.handlers import on_button_click, on_input_text
from app.presentation.telegram.states import Dynamic


dynamic_dialog = Dialog(
    Window(
        Format(
            '{text}'
        ),
        ListGroup(
            Button(Format('{item[text]}'),
                   id='some_id',
                   on_click=on_button_click),
            id='button',
            items='buttons',
            item_id_getter=lambda item: item['target_message_id'],
            when='buttons_exits'
        ),
        MessageInput(on_input_text, content_types=[ContentType.TEXT]),
        getter=get_dynamic,
        state=Dynamic.dyn_state
    ),
)


def setup_dynamic_dialog(router: Router) -> None:
    router.include_router(dynamic_dialog)
