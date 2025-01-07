import asyncio 
from aiogram import Bot 
import logging 
from bot import bot, dp, scheduler, set_commands
from handlers import (
    start
)


async def main():
    await set_commands()
    dp.include_router(start.start_router)

    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())