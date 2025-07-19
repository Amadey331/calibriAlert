from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


storage = MemoryStorage()

bot= Bot(token="6585331872:AAHCf10OaZKn6O79Lm9d2zsLM0nrPoB6Ljo")



dp=Dispatcher(bot, storage=storage)