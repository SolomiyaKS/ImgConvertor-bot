import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import register_handlers

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

register_handlers(dp, bot) 

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
