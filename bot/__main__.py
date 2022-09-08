import asyncio
import logging
from logging.config import fileConfig

from aiogram import Dispatcher
from yoyo import read_migrations, get_backend
from yoyo.backends import DatabaseBackend


from bot import admin_handlers, h_bot, h_handler
from bot.config import pg_db_user, pg_db_host, pg_db_database, pg_db_password, pg_db_schema
from bot.misc import bot


fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)


def database_migrations():
    log.info('Запуск миграций')
    backend: DatabaseBackend = get_backend(f'postgres://{pg_db_user}:{pg_db_password}@{pg_db_host}/{pg_db_database}?schema={pg_db_schema}')
    migrations = read_migrations('./migrations')
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
        # backend.rollback_migrations(backend.to_rollback(migrations))
    log.info('Миграции завершены')


# Запуск процесса поллинга новых апдейтов
async def main():
    database_migrations()
    log.info("Запуск приложения.")
    dp = Dispatcher()
    try:
        await h_bot.set_commands()
        dp.include_router(h_handler.router)
        dp.include_router(admin_handlers.router)
        await dp.start_polling(bot)
    except TypeError:
        log.error("Цикл main был завершен по невнятным причинам")
    except KeyboardInterrupt:
        log.error("Цикл main был завершен клавиатурной прерывашкой")
    except RuntimeError:
        log.error("Цикл main был завершен в рантайме")

if __name__ == "__main__":
    asyncio.run(main())



