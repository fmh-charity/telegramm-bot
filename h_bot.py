# from aiogram import Router
from aiogram.types import *

from config import bot_owner_id
from misc import bot

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
    # log.info(f'Установлен список команд BotCommandScopeChat(chat_id={bot_owner_id})')
    # await bot.set_my_commands(commands, BotCommandScopeChat(chat_id=bot_owner_id))


async def send_msg2owner(msg):
    await bot.send_message(chat_id=bot_owner_id, text=msg)
    print()



