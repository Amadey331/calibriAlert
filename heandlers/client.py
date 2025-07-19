from aiogram import types,Dispatcher
from createBot import dp,bot
import asyncio

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher.filters import Text







# async def send_info():
#     while True:
#         await bot.send_message(-4020727828, "Инфа")

async def start_bot(message:types.Message):
    
    if message.from_user.id == 896957462:
        chat_id = message.chat.id
        await message.answer("Запущенно")
        await message.answer(chat_id)


async def noCommand(message:types.Message):
    
    if message.from_user.id == 896957462:
        await message.answer("Такой команды нет, для ознакомления используйте /help")
        await message.delete()
    else:
        await message.delete()








async def on_start(dp):
    asyncio.create_task(send_info())


# def heandler_regClient(dp:Dispatcher):
#     dp.register_message_handler(send_info)
#     dp.register_message_handler(start_bot ,commands=["start","help"])
#     dp.register_message_handler(noCommand)