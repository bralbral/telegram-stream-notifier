from datetime import datetime
from typing import Any
from typing import Optional
from typing import TextIO

import yt_dlp
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.config import Config
from src.constants import COOKIES_FILE_PATH
from src.db import DataAccessLayer
from src.scheduler.jobs.telegram_notify_job import notify


def setup_scheduler(conf: Config, bot: Bot, dal: DataAccessLayer) -> AsyncIOScheduler:
    """
    :param dal:
    :param conf:
    :param bot:
    :return:
    """

    scheduler = AsyncIOScheduler()

    cookiefile: Optional[TextIO]
    try:
        cookiefile = open(file=COOKIES_FILE_PATH, encoding="utf-8")
    except FileNotFoundError:
        cookiefile = None

    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
    ydl_opts: dict[str, Any] = {
        "cookiefile": cookiefile,
        "quiet": True,
        "load-pages": False,
        "extract_flat": True,
        "skip_download": True,
        "getcomments": False,
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)

    notify_kwargs = {
        "bot": bot,
        "chat_id": conf.chat_id,
        "temp_chat_id": conf.temp_chat_id,
        "ydl": ydl,
        "report_template": conf.report.template,
        "empty_template": conf.report.empty,
        "dal": dal,
    }
    scheduler.add_job(
        notify,
        trigger=IntervalTrigger(seconds=conf.interval_s),
        kwargs=notify_kwargs,
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        next_run_time=datetime.now(),
    )

    # TODO TEMPRORARY COMMENT
    # JUST CLARIFY ERROR
    # auto_turn_off_kwargs = {"dal": dal}
    # scheduler.add_job(
    #     auto_turn_off,
    #     trigger=IntervalTrigger(seconds=conf.interval_s * 2),
    #     kwargs=auto_turn_off_kwargs,
    #     replace_existing=True,
    #     max_instances=1,
    #     coalesce=True,
    #     next_run_time=datetime.now(),
    # )

    return scheduler


__all__ = ["setup_scheduler"]
