import asyncio
import logging
from aiohttp import ClientConnectorError
from bot import bot, dp, scheduler, set_commands
from handlers import start

async def on_startup():
    while True:
        try:
            await bot.get_me()
            print("Бот успешно подключился!")
            break
        except ClientConnectorError:
            print("Ошибка подключения. Повтор через 5 секунд...")
            await asyncio.sleep(5)

async def main():
    await on_startup()

    print("Настроим команды...")
    await set_commands()

    print("Подключаем обработчики...")
    dp.include_router(start.start_router)

    print("Запуск планировщика...")
    scheduler.start()

    print("Начинаем polling...")
    await dp.start_polling(bot, skip_updates=True, request_timeout=60)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
