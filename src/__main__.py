import asyncio
import os.path

from aiogram import Bot
from aiogram import Dispatcher

from src.bot import setup_bot
from src.bot import setup_dispatcher
from src.config import Config
from src.config import load_config
from src.constants import PROJECT_ROOT_DIR
from src.constants import VERSION
from src.logger import logger
from src.scheduler import setup_scheduler


async def main(conf: Config) -> None:
    bot: Bot = setup_bot(token=conf.bot.token.get_secret_value())
    dp: Dispatcher = setup_dispatcher()
    scheduler = setup_scheduler(conf=conf, bot=bot)

    try:
        scheduler.start()
        await dp.start_polling(bot)
        await logger.aerror("Graceful start")
    finally:
        await dp.storage.close()
        await bot.session.close()
        await logger.aerror("Graceful shutdown")


if __name__ == "__main__":
    logger.info(f"{VERSION}, Load config")

    config: Config = load_config(filepath=os.path.join(PROJECT_ROOT_DIR, "config.yaml"))

    asyncio.run(main(conf=config))
