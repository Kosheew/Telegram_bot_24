from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from .routers import film_router

load_dotenv()

root_router = Router()
root_router.include_router(film_router)

@root_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

async def main() -> None:
    TOKEN = getenv("BOT_TOKEN")
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_router(root_router)

    await dp.start_polling(bot)
