from aiogram.types import BotCommand


def superuser_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="add_admin", description="Promote user to admin."),
        BotCommand(command="users", description="Start Users Administration Dialog."),
        BotCommand(command="add_channels", description="Add channels from file."),
        BotCommand(command="scheduler_start", description="Start scheduler"),
        BotCommand(command="scheduler_pause", description="Stop scheduler"),
    ]
    return commands


def admin_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="add_channel", description="Add channel."),
        BotCommand(
            command="channels", description="Start Channels Administration Dialog."
        ),
        BotCommand(command="cancel", description="Clear current state."),
    ]
    return commands


__all__ = ["admin_commands", "superuser_commands"]
