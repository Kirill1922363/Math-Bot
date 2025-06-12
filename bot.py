import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from app.keyboards import math_menu_keyboard
from settings import TOKEN
from app.handlers import router

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привіт, {message.from_user.full_name}!", reply_markup=math_menu_keyboard()
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустити бота"),
            BotCommand(command="calculator", description="Обчислити вираз"),
            BotCommand(command="geometric_calculator", description="Геометричний калькулятор"),
            BotCommand(command="help", description="Довідка"),
        ]
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


