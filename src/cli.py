import platform
from typing import Optional

import asyncclick as click
from aiogram import Bot
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .db import DataAccessLayer
from .logger import logger
from .schemas import UserSchema
from src.bot import setup_bot
from src.bot import setup_dispatcher
from src.config import Config
from src.config import load_config
from src.constants import CONFIG_FILE_PATH
from src.db import session_maker
from src.scheduler import setup_scheduler

if platform.system() == "linux":
    import uvloop

    uvloop.install()


async def create_super_user(telegram_id: int) -> None:
    dal = DataAccessLayer()

    user_dto = UserSchema(user_id=telegram_id, is_superuser=True, is_admin=True)

    result = await dal.user_repo.create(user_schema=user_dto)

    if isinstance(result, UserSchema) and result.id is not None:
        await logger.ainfo("User created.")
    else:
        await logger.error("Cannot create user.")


async def run_bot() -> None:
    config: Config = load_config(config_path=CONFIG_FILE_PATH)

    dal: DataAccessLayer = DataAccessLayer()

    if not await dal.check_superusers():
        await logger.aerror("You must to create superuser before start.")
        return

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


@click.command()
@click.option("--telegram_id", help="TelegramID of User", type=int)
async def start(telegram_id: Optional[int] = None):
    if telegram_id is not None:
        await create_super_user(telegram_id=telegram_id)
    else:
        await run_bot()


__all__ = ["start"]
