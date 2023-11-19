import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import client
import get_test

from dotenv import load_dotenv

# Загрузить переменные окружения из .env файла
load_dotenv()

# Получить значение переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")


bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# client.register_handlers_client(dp)
# admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)

async def main():
    dp.include_routers(get_test.router, client.router)
    # dp.include_router(client.router)
    # dp.include_router(get_test.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())