from aiogram.utils import executor
from createBot import dp,bot
import asyncio
from heandlers import client
from connection import Burse_Info_Db
from funk import get_current_info
import sqlite3
from datetime import datetime
import time
async def bot_start(_):
    try:
        
        print("Бот работает")

    except:
        print("Ошибка")

async def send_current_pars ():
    with open('result_pars.txt', 'r', encoding='utf-8') as fileres:
        lines = fileres.readlines()
     

    
    if len(lines) == 0:
        s="Нету сделок"
        return s
    

    
    else:
        len_list = len(lines)
        
        if len_list>=20:
            coin_line =0
            s=""
            s+=f"_______Время сделок {str(datetime.now())[:16]}_______\n"
            for line in lines:
                if coin_line>20:
                    
                    await bot.send_message(-1001975417836, s)
                    s=""
                    coin_line=0
                    s+=line+"\n"
                else:
                    s+=line+"\n"
                    coin_line+=1
        else:
            s=""
            s+=f"_______Время актуальных пар {str(datetime.now())[:16]}_______\n"
            for line in lines:
                s+=line+"\n"   
            await bot.send_message(-1001975417836, s)

async def send_info():
    db = Burse_Info_Db('burseInfo.db')
    get_current_info.Create_tables(db)
    # get_current_info.createFiles_all_burs()
    while True:
        start_time = time.time()
        if get_current_info.check_all_burs_working():
            end_time = time.time()
            print(end_time - start_time)
            # await send_current_pars()
            if get_current_info.get_all_info_burse(db):
                
                await send_current_pars()
            else:
                continue
        
        
    


# client.heandler_regClient(dp)

async def on_start(dp):
    asyncio.create_task(send_info())

executor.start_polling(dp, skip_updates=True, on_startup=on_start)
