import os
import sys
from pathlib import Path
import django

# Add the root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()

from handlers import registration, category, product, basket, order, language
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(registration.router)
    dp.include_router(category.router)
    dp.include_router(product.router)
    dp.include_router(basket.router)
    dp.include_router(order.router)
    dp.include_router(language.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
