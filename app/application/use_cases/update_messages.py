from dataclasses import dataclass

from aiogram import Bot
from aiogram_dialog import BgManagerFactory, StartMode

from app.domain.message import Message, Messages
from app.domain.user_set import UserSet
from app.presentation.telegram.states import Dynamic


@dataclass
class UpdateMessagesIntputDTO:
    messages: list[Message]


class UpdateMessagesUseCase:
    def __init__(
            self,
            messages: Messages,
            user_set: UserSet,
            bot: Bot,
            bg_factory: BgManagerFactory,
    ) -> None:
        self.messages = messages
        self.user_set = user_set
        self.bot = bot
        self.bg_factory = bg_factory

    async def __call__(self, data: UpdateMessagesIntputDTO) -> None:
        self.messages.update(data.messages)
        start_message = self.messages.get_start_message()
        if start_message is None:
            return
        for user in self.user_set.get_all_users():
            bg = self.bg_factory.bg(self.bot, user.id, user.id)
            await bg.start(Dynamic.dyn_state, mode=StartMode.RESET_STACK, data={"id": start_message.message_id})
