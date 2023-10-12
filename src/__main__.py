import asyncio
import platform

import structlog
from aiogram import Bot
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.bot import setup_bot
from src.bot import setup_dispatcher
from src.config import Config
from src.config import load_config
from src.constants import CONFIG_FILE_PATH
from src.db.session import session_maker
from src.scheduler import setup_scheduler

if platform.system() == "linux":
    import uvloop

    uvloop.install()


async def main() -> None:
    logger = structlog.stdlib.get_logger()
    config: Config = load_config(config_path=CONFIG_FILE_PATH)

    dp: Dispatcher = setup_dispatcher(
        logger=logger, chat_id=config.chat_id, session_maker=session_maker
    )

    bot: Bot = await setup_bot(config=config.bot)

    await logger.ainfo("Starting scheduler")
    scheduler: AsyncIOScheduler = await setup_scheduler(bot=bot, conf=config)
    scheduler.start()

    await logger.ainfo("Starting bot")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except (KeyboardInterrupt, SystemExit):
        await logger.error("Bot stopped!")


if __name__ == "__main__":
    asyncio.run(main())
