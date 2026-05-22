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


async def ensure_admin(dal: DataAccessLayer, admin_id: int) -> None:
    """Ensure admin exists, create if not"""
    if not await dal.is_admins_exists():
        await logger.ainfo(f"Creating admin with ID: {admin_id}")
        role = UserRoleModel(role=UserRole.ADMIN)
        user = UserModel(user_id=admin_id, role=role)
        result = await dal.create_user(obj=user)
        if isinstance(result, UserModel) and result.id is not None:
            await logger.ainfo("Admin created successfully")
        else:
            await logger.aerror("Failed to create admin")
    else:
        await logger.ainfo("Admin already exists")


async def main() -> None:
    await init_db()
    try:
        config = load_config(config_path=CONFIG_FILE_PATH)
        dal = DataAccessLayer()

        # Ensure admin exists
        await ensure_admin(dal, config.admin_id)

        users = await dal.get_users(admins=False)
        admin_users = await dal.get_users(admins=True)

        if not await dal.is_admins_exists():
            await logger.aerror("No admins found in database")
            return

        bot: Bot = await setup_bot(
            config=config.bot, users_id=users, admins_id=admin_users
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
