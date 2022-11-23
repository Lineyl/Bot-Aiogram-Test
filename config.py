from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

back = types.KeyboardButton("Назад")
cancel = types.KeyboardButton("Отмена")

cancelKB = types.ReplyKeyboardMarkup([[cancel]], resize_keyboard=True)

choiceRedKB = types.ReplyKeyboardMarkup([
    [
        types.KeyboardButton("Название"),
        types.KeyboardButton("Описание")
    ],
    [cancel]
], resize_keyboard=True)

mainU = types.ReplyKeyboardMarkup([
    [
        types.KeyboardButton("Добавить"),
        types.KeyboardButton("Редактировать"),
        types.KeyboardButton("Удалить")
    ],
    [back]
], resize_keyboard=True, one_time_keyboard=True)

mainKB = types.ReplyKeyboardMarkup([
    [
        types.KeyboardButton("Подтвердить заказы"),
        types.KeyboardButton("Журнал заказов")
    ],
    [
        types.KeyboardButton("Клиенты")
    ],
    [
        types.KeyboardButton("Услуги"),
        types.KeyboardButton("Профиль")
    ]
], resize_keyboard=True)

regb = types.InlineKeyboardButton("Регистрация", callback_data="reg")
regKB = types.InlineKeyboardMarkup().add(regb)

class RegSpec(StatesGroup):
    prof = State()
    surname = State()
    name = State()
    tNumber = State()
    email = State()
    adress = State()
    tWork = State()

class addUslug(StatesGroup):
    name = State()
    opis = State()

class redUslug(StatesGroup):
    waitID = State()
    waitWhat = State()
    waitName = State()
    waitOpis = State()

class delUslug(StatesGroup):
    waitID = State()
