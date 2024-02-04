import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.filters.command import Command

from settings import Settings


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


inline_keybouard = Command("inline")
reply_keybouard = Command("reply")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(
        f"Приветствую, {hbold(message.from_user.full_name)}!\n",
    )


@dp.message(inline_keybouard)
async def inline(message: Message) -> None:
    start_button = InlineKeyboardButton(text="Начать смену", callback_data="start work")
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[[start_button]])

    await message.answer(
        f"Приветствую, {hbold(message.from_user.full_name)}!\n",
        reply_markup=inline_markup,
    )


@dp.message(reply_keybouard)
async def reply(message: Message) -> None:
    start_button = KeyboardButton(text="Начать смену")
    markup = ReplyKeyboardMarkup(keyboard=[[start_button]])

    await message.answer(
        f"Приветствую, {hbold(message.from_user.full_name)}!\n",
        reply_markup=markup,
    )


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    settings = Settings()
    bot = Bot(settings.bot_token, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
