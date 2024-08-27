from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import SUPPORTED_FORMATS

async def send_extensions(message: Message):
    available_formats = "\n".join(SUPPORTED_FORMATS)
    response_text = f"Доступні формати для конвертації:\n\n{available_formats}"
    await message.answer(response_text)

def register_extensions_handler(dp: Dispatcher):
    dp.message.register(send_extensions, Command('extensions'))
