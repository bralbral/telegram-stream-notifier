import platform
from typing import Optional

import asyncclick as click
from aiogram import Bot
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .db import DataAccessLayer
from .db.models import UserModel
from .db.models import UserRoleModel
from .db.models.user_role import UserRole
from .logger import logger
from src.bot import setup_bot
from src.bot import setup_dispatcher
from src.config import Config
from src.config import load_config
from src.constants import CONFIG_FILE_PATH
from src.constants import VERSION
from src.scheduler import setup_scheduler

if platform.system() == "linux":
    import uvloop

    uvloop.install()


async def create_super_user(telegram_id: int) -> None:
    dal = DataAccessLayer()

    role = UserRoleModel(role=UserRole.SUPERUSER)

    user = UserModel(user_id=telegram_id, role=role)

    result = await dal.create_user(obj=user)

    if isinstance(result, UserModel) and result.id is not None:
        await logger.ainfo("User created.")
    else:
        await logger.error("Cannot create user.")


async def run_bot() -> None:
    config: Config = load_config(config_path=CONFIG_FILE_PATH)

    dal: DataAccessLayer = DataAccessLayer()

    users: list[int] = await dal.get_users(superusers=False)
    superusers: list[int] = await dal.get_users(superusers=True)

    if not await dal.is_superusers_exists():
        await logger.aerror(
            "You must to create superuser before start. Restart with --telegram_id YOUR_TELEGRAM_ID option"
        )
        return

    bot: Bot = await setup_bot(
        config=config.bot, users_id=users, superusers_id=superusers
    )

    await logger.ainfo("Setup scheduler")
    scheduler: AsyncIOScheduler = setup_scheduler(bot=bot, conf=config, dal=dal)
    if config.start_scheduler:
        await logger.ainfo("Starting scheduler")
        scheduler.start()

    dp: Dispatcher = setup_dispatcher(
        chat_id=config.chat_id, dal=dal, scheduler=scheduler
    )

    await logger.aerror(f"Starting bot, version: {VERSION}")

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
