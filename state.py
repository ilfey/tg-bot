from aiogram.dispatcher.filters.state import State, StatesGroup

class ImageState(StatesGroup):
    image = State()
    title = State()
    text = State()