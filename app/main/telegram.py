import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import SimpleEventIsolation
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka, AiogramProvider
from dotenv import load_dotenv
from faststream import FastStream

from app.application.models.config import AiogramSettings
from app.domain.message import Message
from app.domain.text_handler import TextHandler
from app.domain.button import Button
from app.main.di import DialogDataProvider
from app.main.faststream import create_faststream_app
from app.presentation.telegram.commands import setup_commands
from app.presentation.telegram.dialogs import setup_all_dialogs
from app.presentation.telegram.handlers import setup_handlers

messages = [
    Message(
        message_id=1,
        text="Welcome to the bot!",
        command="/start",
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
        command="/second",
    ),
    Message(
        message_id=3,
        text="Final message.",
        input_handler=TextHandler(key="user_input", target_message_id=4)
    ),
    Message(
        message_id=4,
        text="REAL Final message.Your text {user_input}",
    )
]


async def on_startup(app: FastStream) -> None:
    await app.run()


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
    bg_factory = setup_all_dialogs(dp)
    await setup_commands(bot)

    container = make_async_container(AiogramProvider(), DialogDataProvider(messages, bg_factory, bot))
    setup_dishka(container=container, router=dp)
    faststream = create_faststream_app(container)
    logger.info(f'Bot started. {await bot.get_me()}')

    try:
        async with faststream.broker:
            await faststream.start()
            await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"An error occurred while polling: {e}")
    finally:
        await container.close()
        await faststream.stop()
        logger.info('Container closed and bot stopped.')


if __name__ == '__main__':
    asyncio.run(main())
