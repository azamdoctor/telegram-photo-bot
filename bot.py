import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType
from aiogram.client.default import DefaultBotProperties

API_TOKEN = os.getenv("BOT_TOKEN")
SAVE_DIR = 'saved_photos'
os.makedirs(SAVE_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(F.content_type == ContentType.PHOTO)
async def save_any_photo(message: Message):
    thread_id = getattr(message, "message_thread_id", None)
    logging.info(f"[PHOTO] Chat ID: {message.chat.id} | Thread ID: {thread_id} | User: {message.from_user.full_name}")
    photo = message.photo[-1]
    filename = f"{message.chat.id}_{message.message_id}_{photo.file_unique_id}.jpg"
    path = os.path.join(SAVE_DIR, filename)
    await bot.download(photo.file_id, destination=path)
    await message.reply("✅ Фото сохранено локально.")

@dp.message()
async def log_all(message: Message):
    thread_id = getattr(message, "message_thread_id", None)
    logging.info(f"[DEBUG] Chat ID: {message.chat.id} | Thread ID: {thread_id} | Text: {message.text}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
