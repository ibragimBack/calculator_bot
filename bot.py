from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token='7568275743:AAGZsTwlQ7X154-RJavkGrOkhZoA1J6ElfE')
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command='start', description='выбор рассрочки'),
        types.BotCommand(command='stop', description='завершение процесса'),
    ])