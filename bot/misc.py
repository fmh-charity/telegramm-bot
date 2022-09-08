from aiogram import Bot
from bot import config


bot = Bot(token=config.TOKEN, parse_mode='HTML')
