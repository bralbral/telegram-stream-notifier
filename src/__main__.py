import asyncio
import os.path
from datetime import datetime
from datetime import timedelta

from aiogram import Bot
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import TypeAdapter

from src.bot import setup_bot
from src.bot import setup_dispatcher
from src.channel_description import ChannelDescription
from src.config import Config
from src.config import load_config
from src.constants import PROJECT_ROOT_DIR
from src.constants import VERSION
from src.logger import logger
from src.utils import send_report


async def main(conf: Config) -> None:
    await logger.ainfo("Setup Bot")

    bot: Bot = setup_bot(token=conf.bot.token.get_secret_value())

    await logger.ainfo("Setup Dispatcher")

    dp: Dispatcher = setup_dispatcher()

    # setup kwargs for notify
    channel_descriptions_adapter = TypeAdapter(list[ChannelDescription])
    channel_descriptions = channel_descriptions_adapter.validate_python(
        [channel.model_dump() for channel in conf.channels]
    )

    notify_kwargs = {
        "bot": bot,
        "channel_descriptions": channel_descriptions,
        "chat_id": conf.bot.chat_id.get_secret_value(),
    }

    await logger.ainfo("Setup Scheduler")

    scheduler = AsyncIOScheduler(timezone=conf.timezone)
    scheduler.add_job(
        send_report,
        trigger="date",
        run_date=datetime.now() + timedelta(seconds=conf.interval_s),
        kwargs=notify_kwargs,
    )

    if conf.fire_when_starts:
        await logger.ainfo("Fire when starts")
        await send_report(**notify_kwargs)

    try:
        scheduler.start()

        await logger.aerror("Scheduler starts")

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
