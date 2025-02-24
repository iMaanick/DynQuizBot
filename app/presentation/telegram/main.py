import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import SimpleEventIsolation
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka, AiogramProvider
from dotenv import load_dotenv

from app.application.models.config import AiogramSettings
from app.domain.message import Message, Button, TextHandler
from app.infrastructure.logging import setup_logging
from app.main.di import UserProvider, DialogDataProvider
from app.presentation.telegram.commands import setup_commands
from app.presentation.telegram.dialogs import setup_all_dialogs
from app.presentation.telegram.handlers import setup_handlers

messages = [
    Message(
        message_id=1,
        text="Welcome to the bot!",
        command="start",
        buttons=[
            Button(text="Next", target_message_id=2)
        ]
    ),
    Message(
        message_id=2,
        text="This is the second message.",
        buttons=[
            Button(text="Go back", target_message_id=1),
            Button(text="Continue", target_message_id=3)
        ],
        button_width=2,
        command="second",
    ),
    Message(
        message_id=3,
        text="Final message.",
        input_handler=TextHandler(key="user_input", target_message_id=2)
    )
]


async def main() -> None:
    # setup_logging()
    logger = logging.getLogger(__name__)
    load_dotenv()
    token = AiogramSettings().token

    dp = Dispatcher(events_isolation=SimpleEventIsolation())
    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode='HTML')
    )

    logger.info('Setting up handlers, dialogs, and commands.')
    setup_handlers(dp, messages)
    setup_all_dialogs(dp)
    await setup_commands(bot)

    container = make_async_container(AiogramProvider(), UserProvider(), DialogDataProvider(messages))
    setup_dishka(container=container, router=dp)
    logger.info(f'Bot started. {await bot.get_me()}')

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"An error occurred while polling: {e}")
    finally:
        await container.close()
        logger.info('Container closed and bot stopped.')


if __name__ == '__main__':
    asyncio.run(main())
