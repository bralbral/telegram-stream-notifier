from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pydantic import TypeAdapter

from src.config import Config
from src.logger import logger
from src.youtube_notify import ChannelDescription
from src.youtube_notify import send_report


def setup_scheduler(conf: Config, bot: Bot) -> AsyncIOScheduler:
    logger.info("Setup Scheduler")
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

    scheduler = AsyncIOScheduler(timezone=conf.timezone)
    scheduler.add_job(
        send_report,
        trigger=IntervalTrigger(seconds=conf.interval_s),
        kwargs=notify_kwargs,
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    return scheduler


__all__ = ["setup_scheduler"]
