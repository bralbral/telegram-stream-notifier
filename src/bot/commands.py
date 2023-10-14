from aiogram.types import BotCommand


def superuser_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="promote", description="Promote user to admin."),
        BotCommand(command="revoke", description="Revoke admin rights."),
    ]
    return commands


__all__ = ["superuser_commands"]
