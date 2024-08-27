import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command

from config import SUPPORTED_FORMATS, file_storage
from file_utilts import download_and_convert_image

from os import remove

async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.first_name}! Надішліть, будь ласка, фото, яке потрібно конвертувати.")

async def handle_image(message: Message):
    file_id = message.photo[-1].file_id
    message_id = message.message_id
    file_storage[message_id] = file_id

    keyboard = InlineKeyboardBuilder()
    for fmt in SUPPORTED_FORMATS:
        keyboard.add(InlineKeyboardButton(text=fmt.upper(), callback_data=f"{fmt}:{message_id}"))
    keyboard.adjust(2)

    await message.answer("Виберіть формат для конвертації зображення:", reply_markup=keyboard.as_markup())

async def process_callback(callback_query: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    format_to_convert, message_id_str = callback_query.data.split(':')
    message_id = int(message_id_str)
    file_id = file_storage.get(message_id)

    if file_id:
        processing_message = await callback_query.message.answer("Processing", reply_markup=None)
        
        previous_text = "Processing"
        for i in range(4): 
            await asyncio.sleep(0.5) 
            new_text = "Processing" + "." * i
            if new_text != previous_text:
                await bot.edit_message_text(
                    text=new_text,
                    chat_id=callback_query.message.chat.id,
                    message_id=processing_message.message_id
                )
                previous_text = new_text

        output_path = await download_and_convert_image(bot, file_id, format_to_convert, message_id)

        input_file = FSInputFile(output_path)
        await bot.send_document(callback_query.from_user.id, input_file)

        del file_storage[message_id]
        remove(output_path)

        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=processing_message.message_id)
    else:
        await callback_query.message.answer("Помилка: файл не знайдено.")

async def send_extensions(message: Message):
    available_formats = "\n".join(SUPPORTED_FORMATS)
    response_text = f"Доступні формати для конвертації:\n\n{available_formats}"
    await message.answer(response_text)

async def send_help(message: Message):
    await message.answer(
        "Just send me any image *as file* ☺️\n\n"
        "👨‍💻 [Author](tg://resolve?domain=ImSaasha)\n"
        "🤖 [Source code]()",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )

async def echo(message: Message):
    await message.answer("I don't understand you! Send me a photo to convert.")

def register_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(start, CommandStart())
    dp.message.register(handle_image, F.photo)
    dp.callback_query.register(process_callback, F.data)
    dp.message.register(send_extensions, Command('extensions'))
    dp.message.register(send_help, Command("help"))
    dp.message.register(echo)
