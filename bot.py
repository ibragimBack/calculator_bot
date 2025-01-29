from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from os import getenv
# session = AiohttpSession(proxy="http://proxy.server:3128")
load_dotenv()
bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command='start', description='выбор рассрочки'),
        types.BotCommand(command='stop', description='завершение процесса'),
    ])
