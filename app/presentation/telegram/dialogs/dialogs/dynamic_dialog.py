from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ListGroup, Button
from aiogram_dialog.widgets.text import Format

from app.application.widgets.dynamic_group import DynamicGroup
from app.application.dialogs.dynamic.getters import get_dynamic
from app.application.dialogs.dynamic.handlers import on_button_click, on_input_text
from app.presentation.telegram.states import Dynamic

dynamic_dialog = Dialog(
    Window(
        Format(
            '{text}'
        ),
        DynamicGroup(
            ListGroup(
                Button(Format('{item[text]}'),
                       id='some_id',
                       on_click=on_button_click),
                id='button',
                items='buttons',
                item_id_getter=lambda item: item['target_message_id'],
                when=F["buttons"].len() > 0
            ),
            width=F.func(lambda data: data["button_width"])
        ),
        MessageInput(on_input_text, content_types=[ContentType.TEXT]),
        getter=get_dynamic,
        state=Dynamic.dyn_state
    ),
)


def setup_dynamic_dialog(router: Router) -> None:
    router.include_router(dynamic_dialog)
