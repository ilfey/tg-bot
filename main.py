from email.message import Message
import os
import logging

from aiogram.types import Message
from aiogram import Bot, executor, Dispatcher


logging.basicConfig(filename="logs.txt", level=logging.INFO)
# logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TOKEN"))
dispatcher = Dispatcher(bot=bot)


@dispatcher.message_handler(commands=["start"])
async def start_handler(message: Message):
    logging.info("[ Command ] %s use [ start_handler ]", message.from_user.username)
    await message.reply("Hello world")


if __name__ == "__main__":
    executor.start_polling(dispatcher)