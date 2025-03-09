from adaptix._internal.conversion.facade.func import get_converter
from aiogram import Bot
from aiogram_dialog import BgManagerFactory, StartMode
from dishka import FromDishka
from faststream.rabbit import RabbitRouter

from app.application.models.message import Message
from app.domain import message
from app.domain.user_set import UserSet
from app.presentation.telegram.states import Dynamic

update_router = RabbitRouter()


@update_router.subscriber("update",
                          filter=lambda msg: msg.content_type == "application/json", )
async def update(
        message_data: list[Message],
        messages: FromDishka[message.Messages],
        user_set: FromDishka[UserSet],
        bot: FromDishka[Bot],
        bg_factory: FromDishka[BgManagerFactory],
) -> None:
    converter = get_converter(list[Message], list[message.Message])
    messages.update(converter(message_data))
    start_message = messages.get_start_message()
    if start_message is None:
        return
    for user in user_set.get_all_users():
        bg = bg_factory.bg(bot, user.id, user.id)
        await bg.start(Dynamic.dyn_state, mode=StartMode.RESET_STACK, data={"id": start_message.message_id})
