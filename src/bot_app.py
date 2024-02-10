import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


from sqlalchemy import create_engine

from src.settings import Settings, get_db_uri
from src.employee.entrypoints.tg_app import employee_router
from src.employee.adapters import orm


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    db_engine = create_engine(get_db_uri())
    orm.mapper_registry.metadata.create_all(bind=db_engine)
    orm.start_mappers()

    dp = Dispatcher()
    dp.include_router(employee_router)

    settings = Settings()
    bot = Bot(settings.bot_token, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
