from aiogram import Bot
from sulguk import AiogramSulgukMiddleware


def setup_bot(token: str):
    bot = Bot(token=token)
    bot.session.middleware(AiogramSulgukMiddleware())

    return bot


__all__ = ["bot"]
