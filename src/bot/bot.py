from aiogram import Bot
from sulguk import AiogramSulgukMiddleware

from src.logger import logger


def setup_bot(token: str):
    logger.info("Setup Bot")

    bot = Bot(token=token)
    bot.session.middleware(AiogramSulgukMiddleware())

    return bot


__all__ = ["bot"]
