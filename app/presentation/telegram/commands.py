from aiogram import Bot
from aiogram.types import BotCommand


async def setup_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="start"),
    ]
    await bot.set_my_commands(commands)
