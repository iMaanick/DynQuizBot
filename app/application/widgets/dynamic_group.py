from itertools import chain
from typing import Optional, Union, Iterable

from aiogram import MagicFilter
from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import RawKeyboard, ButtonVariant
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Keyboard, Group


class DynamicGroup(Group):
    def __init__(
            self,
            *buttons: Keyboard,
            id: Optional[str] = None,
            width: Optional[Union[int, MagicFilter]] = None,
            when: WhenCondition = None,
    ):
        super().__init__(id=id, when=when)
        self.buttons = buttons
        self.width = width

    async def _render_keyboard(
            self,
            data: dict,
            manager: DialogManager,
    ) -> RawKeyboard:
        kbd: RawKeyboard = []
        actual_width = self.width

        if isinstance(self.width, MagicFilter):
            actual_width = self.width.resolve(data)

        if actual_width is not None and not isinstance(actual_width, int):
            raise ValueError(f"Resolved width must be an integer or None, got {type(actual_width)}")

        for b in self.buttons:
            b_kbd = await b.render_keyboard(data, manager)
            if actual_width is None:
                kbd += b_kbd
            else:
                if not kbd:
                    kbd.append([])
                kbd[0].extend(chain.from_iterable(b_kbd))

        if actual_width and kbd:
            kbd = self._dyn_wrap_kbd(kbd[0], actual_width)
        return kbd

    def _dyn_wrap_kbd(
            self,
            kbd: Iterable[InlineKeyboardButton],
            width: int,
    ) -> RawKeyboard:
        res: RawKeyboard = []
        row: list[ButtonVariant] = []
        for b in kbd:
            row.append(b)
            if len(row) >= width:
                res.append(row)
                row = []
        if row:
            res.append(row)
        return res
