import asyncio
import platform

from tortoise import Tortoise

from .db import TORTOISE_ORM, DataAccessLayer
from .db.models import UserModel, UserRoleModel
from .db.models.user_role import UserRole
from .logger import logger
from src.bot import setup_bot, setup_dispatcher
from src.config import load_config
from src.constants import CONFIG_FILE_PATH, VERSION
from src.scheduler import setup_scheduler
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

if platform.system() == "linux":
    import uvloop
    uvloop.install()


async def init_db():
    await Tortoise.init(db_config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()


async def ensure_superuser(dal: DataAccessLayer, superuser_id: int) -> None:
    """Ensure superuser exists, create if not"""
    if not await dal.is_superusers_exists():
        await logger.ainfo(f"Creating superuser with ID: {superuser_id}")
        role = UserRoleModel(role=UserRole.SUPERUSER)
        user = UserModel(user_id=superuser_id, role=role)
        result = await dal.create_user(obj=user)
        if isinstance(result, UserModel) and result.id is not None:
            await logger.ainfo("Superuser created successfully")
        else:
            await logger.aerror("Failed to create superuser")
    else:
        await logger.ainfo("Superuser already exists")


async def main() -> None:
    await init_db()
    try:
        config = load_config(config_path=CONFIG_FILE_PATH)
        dal = DataAccessLayer()

        # Ensure superuser exists
        await ensure_superuser(dal, config.superuser_id)

        users = await dal.get_users(superusers=False)
        superusers = await dal.get_users(superusers=True)

        if not await dal.is_superusers_exists():
            await logger.aerror("No superusers found in database")
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
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())