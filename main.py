from state import ImageState
import effects.demotivator as demotivator

from email.message import Message
import os
import logging

from PIL import Image
from aiogram.types import (
    ContentTypes,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, # TODO
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Bot, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TOKEN"))
storage = MemoryStorage()
dispatcher = Dispatcher(bot=bot, storage=storage)


@dispatcher.message_handler(commands=["start"])
async def start_handler(message: Message):
    await ImageState.image.set()

    await message.answer(text="Привет, этот бот позволяет делать разные эффекты с картинками. Чтобы что-то сделать с картинкой, просто отправь ее сюда.")

@dispatcher.message_handler(state='*', commands='cancel')
@dispatcher.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)

    await state.finish()
    await message.answer(text="Хорошо, может начнем все с начало?")


@dispatcher.message_handler(content_types=ContentTypes.PHOTO, state="*")
async def demotivator_handler(message: Message, state: FSMContext):
    logging.info("[ Command ] %s use [ demotivator_handler ]", message.from_user.username)

    async with state.proxy() as data:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)

        data['image'] = Image.open(fp=await bot.download_file(file_path=file.file_path))

    keyboard_markup = ReplyKeyboardMarkup()

    keyboard_markup.add("Демотиватор")

    await ImageState.next()
    await message.reply("Хорошо, теперь выбирите эффект.", reply_markup=keyboard_markup)


@dispatcher.message_handler(Text(equals='демотиватор', ignore_case=True), state=ImageState.title)
async def process_title(message: Message, state: FSMContext):
    await message.reply("Вы выбрали демотиватор, теперь введите заголовок.")
    await state.set_state(ImageState.title.state)


@dispatcher.message_handler(state=ImageState.title)
async def process_title(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await message.reply("Отлично, теперь введите текст.")
    await state.set_state(ImageState.text.state)


@dispatcher.message_handler(state=ImageState.text)
async def process_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    user_state = await state.get_data("image")

    await state.finish()
    dem = demotivator.create_demotivator(im=user_state["image"], title=user_state["title"], text=user_state["text"])
    dem.save(fp="output.png")

    with open("output.png", "rb") as file:
        await bot.send_photo(chat_id=message.chat.id, photo=file)


if __name__ == "__main__":
    executor.start_polling(dispatcher)