from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ...filters import RoleFilter
from ...filters import UserRole

scheduler_router = Router(name="scheduler")


@scheduler_router.message(
    Command("scheduler_start"),
    RoleFilter(role=[UserRole.SUPERUSER]),
    State(state="*"),
)
async def start_scheduler(message: Message, scheduler: AsyncIOScheduler, **kwargs):
    if scheduler.running:
        scheduler.resume()
    else:
        scheduler.start()

    await message.answer("Scheduler started.")


@scheduler_router.message(
    Command("scheduler_pause"),
    RoleFilter(role=[UserRole.SUPERUSER]),
    State(state="*"),
)
async def stop_scheduler(message: Message, scheduler: AsyncIOScheduler, **kwargs):
    scheduler.pause()
    await message.answer("Scheduler paused.")


__all__ = ["scheduler_router"]
