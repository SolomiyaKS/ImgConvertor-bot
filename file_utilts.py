from io import BytesIO
from skimage import io as sk_io
from aiogram import Bot

async def download_and_convert_image(bot: Bot, file_id: str, format_to_convert: str, message_id: int):
    file_info = await bot.get_file(file_id)
    file = await bot.download_file(file_info.file_path)

    img = sk_io.imread(BytesIO(file.read()))
    output_path = f'{message_id}.{format_to_convert}'
    sk_io.imsave(output_path, img)

    return output_path
