# from aiogram import Router
from aiogram.types import *

from bot.misc import bot

import logging
from logging.config import fileConfig


fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands():
    commands = [
        BotCommand(command="/start", description="Старт"),
        BotCommand(command="/buttons", description="⌨️Кнопочки"),
        # BotCommand(command="/help", description="❓ Справка"),
    ]
    log.info(f'Установлен список команд BotCommandScopeDefault()')
    await bot.set_my_commands(commands, BotCommandScopeDefault())




