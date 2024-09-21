from datetime import datetime
from typing import Any
from typing import Optional
from typing import TextIO

import yt_dlp
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from twitchAPI.twitch import Twitch

from src.config import Config
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
        youtube = conf.youtube
        if conf.youtube:
            cookies_filepath = youtube.cookies_filepath
            cookiefile = open(file=cookies_filepath, encoding="utf-8")
        else:
            cookiefile = None
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
        "extractor_args": {"youtubetab": {"skip": "authcheck"}},
    }

    if conf.twitch:
        twitch = Twitch(app_id=conf.twitch.app_id, app_secret=conf.twitch.app_secret)
    else:
        twitch = None

    ydl = yt_dlp.YoutubeDL(ydl_opts)

    notify_kwargs = {
        "bot": bot,
        "chat_id": conf.chat_id,
        "temp_chat_id": conf.temp_chat_id,
        "ydl": ydl,
        "report_template": conf.report.template,
        "empty_template": conf.report.empty,
        "dal": dal,
        "twitch": twitch,
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

    return scheduler


__all__ = ["setup_scheduler"]
