from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

db = sqlite3.connect("mainData.db")
cur = db.cursor()

storage = MemoryStorage()

bot = Bot(token="5455972890:AAFwDafR0rc8EIPzRZl5rLEG7A2VmzI1lUQ")
dp = Dispatcher(bot, storage=storage)