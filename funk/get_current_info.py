import time

from binance.client import Client
from pybit.unified_trading import HTTP
import requests
import aiohttp
import ccxt
import sqlite3
from threading import Thread
import asyncio
import hmac
import hashlib
import base64
import json
from datetime import datetime
import concurrent.futures
from functools import partial


from math import fabs
api_Dict = {"Binance":"Swdzc6acJSywWHABrwCRxRzOmbaLs4YJVToqUvR0trSOHJ0RCfeBZ8X3OjPfYbul  0uH0KTpTLFDygkggs88XOvjjixvBP6VWa1PhYquVNNtNuq4eg5evLbMHisSEcahU", 
            "Bybit":"0UaYZ2OE1arzvkwR5l  iLChytx6eRvXa5piLF0kP3ZTPNej7wpLMbG1",
            "Kucoin":"64fd7d0a4d99de000198d77a  ed9211ce-ba00-48ce-8362-8e433359630c",
            "Phemex":"56e8e6bc-6ce9-4b91-83fa-ecb73f7d8abf  -4J2HBVFfnW6MWLlIdkqAKITwdRExDlk2alSIdJB1Dc4MjY2YTEzMS05NmNmLTQwNTAtYmNjNS03NDY4ZWYyODRiNDY",
            "Huobi":"1qdmpe4rty-481e3962-929f2383-1bdab  91ce0047-d5b0b9f0-26ebfa18-cc8d5",
            "GateIo":"1",
            "OKX":"b1dfd253-16ea-4036-9962-e9b65c69a057  BA379B781C16574C1CC39C5503CF40BF  DSAWwww!23"}

# Словарь с конфигурациями записи монет на биржах, тоесть как по какому инмени они получаются на бирже
burs_file_config = {"Binance":"space=0 letter=up", 
            "Bybit":"space=0 letter=up",
            "Kucoin":"space=- letter=up",
            "Phemex":"space=/ letter=up",
            "Huobi":"space=/ letter=up",
            "GateIo":"space=_ letter=low",
            "OKX":"space=- letter=up"}
# Создание таблиц
def Create_tables(db):
    for burse in api_Dict.keys():
        db.create_tables_Burse(burse)



# Проверка всех подключений к биржам
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
def check_binance():
    try:
        api_binance,secret_binance = tuple(api_Dict["Binance"].split("  "))
        client = Client(api_binance, secret_binance)
        print("Есть подключение к binance")
        return True
    except:
        print("Ошибка с binance API")
        return False

def check_bybit():
    try:
        session = HTTP(testnet=True)
        print("Есть подключение к Bybit")
        return True
    except:
        print("Ошибка с подключением Bybit")
        return False
    

def check_kucoin():
    try:
        response = requests.get(" https://api.kucoin.com/")
        print("Есть подключение к Kucoin")
        return True
    except:
        print("Ошибка с подключением Bybit")
        return False
    

def check_phemex():
    try:
        api_phemex,secret_phemex = tuple(api_Dict["Phemex"].split("  "))
        
        phemex = ccxt.phemex({
            "enableRateLimit": True,
            "apiKey": api_phemex,
            "secret": secret_phemex
        })
        
        print("Есть подключение к Phemex")
        return True
    except:
        print("Ошибка с подключением Phemex")
        return False    
        

def chech_huobi():

    try:
        response = requests.get(" https://api.huobi.pro")
        print("Есть подключение к Huobi")
        return True
    except:
        print("Ошибка с подключением Huobi")
        return False   


def chech_gateIo():
    try:
        response = requests.get("https://api.gateio.ws/api/v4")
        print("Есть подключение к Gate.io")
        return True
    except:
        print("Ошибка с подключением Gate.io")
        return False   


def create_signature(timestamp, method, request_path, secret, body = ""):
    if str(body) =="{}" or str(body) =="None":
        body = ''
    message = str(timestamp) + str.upper(method) +request_path +str(body)
    mac = hmac.new(bytes(secret, encoding="utf-8"), bytes(message, encoding="utf-8"), digestmod="sha256")
    d = mac.digest()
    return base64.b64encode(d)



def check_okx():
    timestep = datetime.utcnow().isoformat("T", "milliseconds") + "Z"
    method ="GET"
    endpoint = '/api/v5/account/balance'
    url = 'https://www.okx.cab'+endpoint
    
    
    api_okx,secret_okx,passphrase = tuple(api_Dict["OKX"].split("  "))

    
    
    headers = {
        'OK-ACCESS-KEY': api_okx,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'OK-ACCESS-TIMESTAMP': timestep,
        'OK-ACCESS-SIGN': create_signature(timestep, method, endpoint,secret_okx)
    }

    # Выполняем GET-запрос
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Есть подключение к OKX")
        return True
    else:

        print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")    
        return False



def get_vol_token_binance(token):
    try:
        api_binance,secret_binance = tuple(api_Dict["Binance"].split("  "))
        client = Client(api_binance, secret_binance)
        symbol = token
        ticker = client.get_ticker(symbol=symbol)
        return float(ticker["quoteVolume"])
    except:
        print("При получении объёмов о монете с binance ошибка")
        return False

# Функции для получения объёмов по заданой монете с бирж
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def get_vol_token_bybit(token):
    try:
        exchange = ccxt.bybit()
        symbol = token
        ticker = exchange.fetch_ticker(symbol)
        return float(ticker["quoteVolume"])

    except:
        print("При получении объёмов о монете с bybit ошибка")
        return False 

def get_vol_token_kucoin(token):
    try:
        exchange = ccxt.kucoin()
        symbol = token.split("USDT")[0]+"-"+"USDT"
        ticker = exchange.fetch_ticker(symbol)
        return float(ticker["quoteVolume"])
    except:
        print("При получении объёмов о монете с Kucoin ошибка")
        return False 

def get_vol_token_phemex(token):
    try:
        exchange = ccxt.phemex()
        symbol = token.split("USDT")[0]+"/"+"USDT"


        ticker = exchange.fetch_ticker(symbol)
        return float(ticker["quoteVolume"])
    except:
        print("При получении объёмов о монете с phemex ошибка")
        return False 

def get_vol_token_huobi(token):
    try:
        exchange = ccxt.huobi()
        symbol = token.split("USDT")[0]+"/"+"USDT"


        ticker = exchange.fetch_ticker(symbol)
        return float(ticker["quoteVolume"])
    except Exception as e:
        print("Ошибка huobi",e)
        print("При получении объёмов о монете с huobi ошибка",token)
        return False 

def get_vol_token_gateio(token):
    try:
        exchange = ccxt.gateio()
        symbol = token.split("USDT")[0]+"/"+"USDT"


        ticker = exchange.fetch_ticker(symbol)
        return float(ticker["quoteVolume"])
    except :
        print("При получении объёмов о монете с Gate.Io ошибка")
        return False 


def get_vol_token_okx(token):

    try:
        exchange = ccxt.okex()
        symbol = token.split("USDT")[0]+"/"+"USDT"


        ticker = exchange.fetch_ticker(symbol)
        return float(ticker["quoteVolume"])
    except :
        print("При получении объёмов о монете с OKX ошибка")
        return False 

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



# Функция для обработки объёмов 2 бирж по монете что бы объёмы были не ниже допустимых 


def process_vol_two_burs(burs1 , burs2 , token_name):
# Словарь с функциями где ключи это название (для удобсва)
    burs_funk_dict= {
        "Binance":get_vol_token_binance, 
        "Bybit":get_vol_token_bybit,
        "Kucoin":get_vol_token_kucoin,
        "Phemex":get_vol_token_phemex,
        "Huobi":get_vol_token_huobi,
        "GateIo": get_vol_token_gateio,
        "OKX":get_vol_token_okx}

    try:
        if burs_funk_dict[burs1](token_name)>=50000 and burs_funk_dict[burs2](token_name)>=50000:
            return True
        else:
            return False
    except:
        print("Произлшла ошибка при получения объёмов с двух бирж при создании связки")
        return False

# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# Получение словаря со словарями где ключ это биржа а второй ключ это монета
def get_Allburse_coin_dict(db):
    dict_burs_price = {}
    for burs in api_Dict.keys():
        # print(db.get_allInfo_for_byrse(burs))
        dict_burs_price[burs] = db.get_allInfo_for_byrse(burs)
    return dict_burs_price



def get_dict_burs_price(dict_burs):
    with open('coins_main.txt', 'r', encoding='utf-8') as file:
        coins = file.read().split()       
    dict_all_price_burse = {}
    for coin in coins:
        burses_price = {}
        for burs in dict_burs:
            try:
                burs_name_dict = dict_burs[burs]

                burses_price[burs] = burs_name_dict[coin]
                # print("Успешно")
            except:
                continue
        dict_all_price_burse[coin] = burses_price

    return dict_all_price_burse


def create_fileAllpars():
    burs = api_Dict.keys()
    with open('allPars.txt', 'w', encoding='utf-8') as file:
        l = []
        for burse1 in burs:

            for burse2 in burs:

                if burse1 == burse2:
                    continue
                else:
                    if burse2 + "-" + burse1 in l: 
                        
                        continue
                    else:
                        l.append(burse1 + "-" + burse2)
                        file.write(burse1 + "-" + burse2+'\n')



def get_coinsDif_allBurse(dict_coin_price):
    # count_burse = api_Dict.keys()
    
    # print(len(count_burse))
    
    coin_dif_allBurse_dict = {}
    for coin in dict_coin_price:
        coin_dict = dict_coin_price[coin]
        pars_dict = {}
        for burse1 in coin_dict:
            burs_name1, coin_price1 = burse1, coin_dict[burse1]

            for burse2 in coin_dict:
            
                
                if burse1 == burse2:
                    continue
                else:
                    burs_name2, coin_price2 = burse2, coin_dict[burse2]
                    if coin_price1!=None and coin_price2!=None :
                        if float(coin_price1)!=0 and float(coin_price2!=0) :
                           
                            pars_dict[burse1 + "-" + burse2] = abs(float(coin_price1) - float(coin_price2)) * 100 / float(coin_price1)
                    
                    else:
                        continue
        
        coin_dif_allBurse_dict[coin] = pars_dict
    return coin_dif_allBurse_dict

def normal_format_dif(coin_dif_allBurse_dict):
    
    with open('allPars.txt', 'r', encoding='utf-8') as file:
        pars = file.read().split()
    
    
    with open('result_pars.txt', 'w', encoding='utf-8') as fileres:
        
        for coin in coin_dif_allBurse_dict:
            
            burs_dict = coin_dif_allBurse_dict[coin]

            for par in pars:
                try:
                    # Проверка что если больше 1.7 процентов разницы выводить
                    if float(burs_dict[par])>=1.7:
                       
                        # s += f"Пара:{par}-разинца в цене{burs_dict[par]}\n"
                        
                        burs1_name, burs2_name = tuple(par.split("-"))
                        if process_vol_two_burs(burs1_name,burs2_name,coin):

                            fileres.write(f" Монета:{coin}|Пара: {par}|разинца в цене: {round(float(burs_dict[par]),3)}%\n")
                        else:
                            continue
                except:
                    continue
   

    # for coin in coin_dif_allBurse_dict:




# Загрузка  биржи Binance
def get_current_info_binance(db):
    # db = Burse_Info_Db('burseInfo.db')
    try:
        
        start_binance = time.time()

        with open('funk/coins_binance.txt', 'r', encoding='utf-8') as file:
            coins = file.read().split()   

        # for coin in coins:

            api_binance,secret_binance = tuple(api_Dict["Binance"].split("  "))
            client = Client(api_binance, secret_binance)
            tikers = client.get_all_tickers()
            for coin in tikers:
                if coin["symbol"] in coins:
                    db.insert_coin_info_for_burse('Binance', coin["symbol"], coin["price"])
        print(f"Время выполнения загрузки в бд Binance: {time.time()-start_binance}")
        return True
    except:
        print("Ошибка Binance")
        return False
# 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# Загрузка  биржи Bybit
def get_current_info_Bybit(db):
    # db = Burse_Info_Db('burseInfo.db')
    try:
        start_bybit = time.time()
        url = 'https://api.bybit.com/v2/public/tickers'
        response = requests.get(url)

        if response.status_code == 200:

            with open('funk/coins_bybit.txt', 'r', encoding='utf-8') as file:
                coins = file.read().split() 

            data = response.json()
            data_res = data["result"]

            for coin in data_res:
                if coin["symbol"] in coins:
                    db.insert_coin_info_for_burse('Bybit', coin["symbol"], coin['last_price'])
                # if coin["symbol"] in coins:
                #     db.insert_coin_info_for_burse('Binance', coin["symbol"], coin["price"])        
            print(f"Время выполнения загрузки в бд Bybit: {time.time()-start_bybit}")
            return True
        else:

            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
            return False
    except:
        
        print("Ошибка Bybit")
        return False

# 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# Загрузка  биржи Kucoin
def get_current_info_Kucoin(db):
    # db = Burse_Info_Db('burseInfo.db')
    try:

        start_Kucoin = time.time()
        url = 'https://api.kucoin.com/api/v1/market/allTickers'
        response = requests.get(url)

        if response.status_code == 200:

            with open('funk/coins_kucoin.txt', 'r', encoding='utf-8') as file:
                coins = file.read().split() 


            data = response.json()
            data_data =data["data"] 
            # print(data_data["ticker"]) 

            for coin in data_data["ticker"]:
                if coin["symbol"] in coins:
                    db.insert_coin_info_for_burse('Kucoin', coin["symbol"].replace('-', ''), coin['last'])

            # for coin in data_res:
            #     print(coin["symbol"])
            #     if coin["symbol"] in coins:

                    # db.insert_coin_info_for_burse('Bybit', coin["symbol"], coin['last_price'])
                # if coin["symbol"] in coins:
                #     db.insert_coin_info_for_burse('Binance', coin["symbol"], coin["price"])        
            print(f"Время выполнения загрузки в бд Kucoin: {time.time()-start_Kucoin}")
            return True
        else:
            
            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
            return False
    except:
        print("Ошибка Kucoin")
        return False    




# 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

# Загрузка  биржи Phemex
def get_current_info_Phemex(db):
    # db = Burse_Info_Db('burseInfo.db')
    try:
        start_Phemex = time.time()
        api_phemex,secret_phemex = tuple(api_Dict["Phemex"].split("  "))
        
        phemex = ccxt.phemex({
            "enableRateLimit": True,
            "apiKey": api_phemex,
            "secret": secret_phemex
        })
        
        with open('funk/coins_phemex.txt', 'r', encoding='utf-8') as file:
            coins = file.read().split()    
        
        markets = phemex.fetch_tickers()
        
        
        for coin in markets:
            coin_dict = markets[coin]
            formatted_number=0
            
            if coin_dict["symbol"] in coins:
                
                if coin_dict["last"]!= None:
                    number = float(coin_dict["last"])
                    formatted_number = "{:.15f}".format(number)
                else:
                    formatted_number=None

                db.insert_coin_info_for_burse('Phemex', coin_dict["symbol"].replace('/', ''), formatted_number)
    
        print(f"Время выполнения загрузки в бд Phemex: {time.time()-start_Phemex}")
        return True
    except Exception as ex:
        print("Ошибка Phemex",ex)
        return False

        
# Загрузка  биржи huobi
def get_current_info_huobi(db):
    try:
        start_huobi = time.time()
        api_huobi, secret_huobi = tuple(api_Dict["Huobi"].split("  "))
        huobi = ccxt.huobi({
            "enableRateLimit": True,
            "apiKey": api_huobi,
            "secret": secret_huobi,
        })

        with open('funk/coins_huobi.txt', 'r', encoding='utf-8') as file:
            coins = file.read().split()

        markets = huobi.fetch_tickers()

        for coin in markets:
            coin_dict = markets[coin]
            formatted_number = 0

            if coin_dict["symbol"] in coins:

                if coin_dict["last"] != None:
                    number = float(coin_dict["last"])
                    formatted_number = "{:.15f}".format(number)
                else:
                    formatted_number = None

                db.insert_coin_info_for_burse('Huobi', coin_dict["symbol"].replace('/', ''), formatted_number)

        print(f"Время выполнения загрузки в бд Huobi: {time.time() - start_huobi}")
        return True
    except Exception as ex:
        print("Ошибка Huobi", ex)
        return False
# 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111





# 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# Загрузка  биржи Gateio
def get_current_info_Gateio(db):
    # db = Burse_Info_Db('burseInfo.db')
    try:
        start_GateIo = time.time()
        url = 'https://api.gate.io/api2/1/tickers'
        with open('funk/coins_gateio.txt', 'r', encoding='utf-8') as file:
            coins = file.read().split()    

        # for coin in coins:
        #     print(coin.replace("-","_"))

        # Выполняем GET-запрос
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for pair, info in data.items():
                # print(pair)
                # print(coins)
                if pair in coins:
                    last_price = info['last']  # Получаем последнюю цену
                    db.insert_coin_info_for_burse('GateIo', pair.replace('_', '').upper(), last_price)  
            print(f"Время выполнения загрузки в бд Gate.Io: {time.time()-start_GateIo}")
            return True
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
            return False
    except:
        print(f"Ошибка при выполнении запроса GateIo:") 
        return False

# 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

# Получение данных с okx
def get_current_info_Okx(db):
    # db = Burse_Info_Db('burseInfo.db')
    try:
        start_Okx = time.time()
        with open('funk/coins_okx.txt', 'r', encoding='utf-8') as file:
            coins = file.read().split()       
        api_okx, secret_okx, passphrase = tuple(api_Dict["OKX"].split("  "))
        endpoint = '/api/v5/market/tickers'
        url = 'https://www.okx.cab' + endpoint
        timestamp = datetime.utcnow().isoformat("T", "milliseconds") + "Z"
        signature = create_signature(timestamp, 'GET', endpoint, secret_okx)
        headers = {
            'OK-ACCESS-KEY': api_okx,
            'OK-ACCESS-PASSPHRASE': passphrase,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-SIGN': signature
        }
        params = {
            'instType': 'SPOT'  # Укажите желаемый тип инструмента
        }    
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()



            for ticker in data['data']:
                symbol = ticker['instId']
                if symbol in coins:


                    price = ticker['last']
                    db.insert_coin_info_for_burse('OKX', symbol.replace('-', ''), price) 
            print(f"Время выполнения загрузки в бд Okx: {time.time()-start_Okx}")
            return True
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")    
            return False
    except:
        print(f"Ошибка при выполнении запроса OKX:")  
        return False        



# Функция для создания файлов с названиями монет для разных бирж


def createFiles_all_burs():
    with open('coins_main.txt', 'r', encoding='utf-8') as file_coins:
        coins = file_coins.read().split() 
    for burs_name_conf in burs_file_config:
        name_burs = burs_name_conf.lower()
        space, letter = tuple(burs_file_config[burs_name_conf].split(' '))
        space = space.split("=")[1]
        letter = letter.split("=")[1]
        with open(f'funk/coins_{name_burs}.txt', 'w', encoding='utf-8') as file:
            if space == "0":
                
                for coin in coins:
                    
                    if letter =="up":
                        file.write(f"{coin.upper()}\n")
                    if letter =="low":
                        file.write(f"{coin.lower()}\n")
            else:

                for coin in coins:
                    coin = coin.split("USDT")[0]+space+"USDT"
                    if letter =="up":
                        file.write(f"{coin.upper()}\n")
                    if letter =="low":
                        file.write(f"{coin.lower()}\n")                

        

# функция для проверки всех бирж
def check_all_burs_working():
    tasks = [
        check_binance,
        check_bybit,
        check_kucoin,
        check_phemex,
        chech_huobi,
        chech_gateIo,
        check_okx
        
    ]
    
    for task in tasks:
        if task():
            continue
        else:
            return False

    return True


def start_updateBd_allBurse(db):
    tasks = [
    get_current_info_huobi,
    get_current_info_binance,
    get_current_info_Bybit,
    get_current_info_Kucoin,
    get_current_info_Phemex,
    get_current_info_Gateio,
    get_current_info_Okx    
    ]
    for task in tasks:
        if task(db):
            continue
        else:
            print("При загрузки всех цен в бд произошла ошибка в одной или нескольких загруках")
            return False

    return True    


# загрузка в бд всех бирж
def get_all_info_burse(db):


    if start_updateBd_allBurse(db):

        create_fileAllpars()
        dict_burse = get_Allburse_coin_dict(db)
        coins_price_all_burse = get_dict_burs_price(dict_burse)
        coin_dif_allBurse_dict = get_coinsDif_allBurse(coins_price_all_burse)
        normal_format_dif(coin_dif_allBurse_dict)
        return True
    else:
        return False



























# Если чё то пойдёт не так 
# def get_all_info_burse(db):
#     # def wrapper_get_current_info_binance():
#     #     get_current_info_binance(db)
        
#     # def wrapper_get_current_info_Bybit():
#     #     get_current_info_Bybit(db)
        
#     # def wrapper_get_current_info_Kucoin():
#     #     get_current_info_Kucoin(db)
        
#     # def wrapper_get_current_info_Phemex():
#     #     get_current_info_Phemex(db)
        
#     # def wrapper_get_current_info_Gateio():
#     #     get_current_info_Gateio(db)
        
#     # def wrapper_get_current_info_Okx():
#     #     get_current_info_Okx(db)
        
#     # def wrapper_get_current_info_hyobi():
#     #     get_current_info_hyobi(db)

#     with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
#         wrapped_functions = [
#             partial(get_current_info_binance, db),
#             partial(get_current_info_Bybit, db),
#             partial(get_current_info_Kucoin, db),
#             partial(get_current_info_Phemex, db),
#             partial(get_current_info_Gateio, db),
#             partial(get_current_info_Okx, db),
#             partial(get_current_info_hyobi, db),
#         ]
#         results = list(executor.map(lambda func: func(), wrapped_functions))

#     if all(results):
#         print("Все загрузки успешны.")
#     else:
#         print("Одна или несколько загрузок не удалось.")
# # Загрузка  биржи Binance
# def get_current_info_binance(db):
#     try:
#         start_binance = time.time()

#         with open('funk/coins_binance.txt', 'r', encoding='utf-8') as file:
#             coins = file.read().split()   

#         # for coin in coins:

#             api_binance,secret_binance = tuple(api_Dict["Binance"].split("  "))
#             client = Client(api_binance, secret_binance)
#             tikers = client.get_all_tickers()
#             for coin in tikers:
#                 if coin["symbol"] in coins:
#                     db.insert_coin_info_for_burse('Binance', coin["symbol"], coin["price"])
#         print(f"Время выполнения загрузки в бд Binance: {time.time()-start_binance}")
#         return True
#     except:
#         return False
# # 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# # Загрузка  биржи Bybit
# def get_current_info_Bybit(db):
#     start_bybit = time.time()
#     url = 'https://api.bybit.com/v2/public/tickers'
#     response = requests.get(url)
    
#     if response.status_code == 200:
        
#         with open('funk/coins_bybit.txt', 'r', encoding='utf-8') as file:
#             coins = file.read().split() 
        
#         data = response.json()
#         data_res = data["result"]
        
#         for coin in data_res:
#             if coin["symbol"] in coins:
#                 db.insert_coin_info_for_burse('Bybit', coin["symbol"], coin['last_price'])
#             # if coin["symbol"] in coins:
#             #     db.insert_coin_info_for_burse('Binance', coin["symbol"], coin["price"])        
#         print(f"Время выполнения загрузки в бд Bybit: {time.time()-start_bybit}")
#         return True
#     else:

#         print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
#         return False


# # 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# # Загрузка  биржи Kucoin
# def get_current_info_Kucoin(db):
#     start_Kucoin = time.time()
#     url = 'https://api.kucoin.com/api/v1/market/allTickers'
#     response = requests.get(url)
    
#     if response.status_code == 200:
        
#         with open('funk/coins_cucoin.txt', 'r', encoding='utf-8') as file:
#             coins = file.read().split() 
        

#         data = response.json()
#         data_data =data["data"] 
#         # print(data_data["ticker"]) 

#         for coin in data_data["ticker"]:
#             if coin["symbol"] in coins:
#                 db.insert_coin_info_for_burse('Kucoin', coin["symbol"].replace('-', ''), coin['last'])

#         # for coin in data_res:
#         #     print(coin["symbol"])
#         #     if coin["symbol"] in coins:

#                 # db.insert_coin_info_for_burse('Bybit', coin["symbol"], coin['last_price'])
#             # if coin["symbol"] in coins:
#             #     db.insert_coin_info_for_burse('Binance', coin["symbol"], coin["price"])        
#         print(f"Время выполнения загрузки в бд Kucoin: {time.time()-start_Kucoin}")
#         return True
#     else:
        
#         print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
#         return False





# # 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

# # Загрузка  биржи Phemex
# def get_current_info_Phemex(db):
#     try:
#         start_Phemex = time.time()
#         api_phemex,secret_phemex = tuple(api_Dict["Phemex"].split("  "))
        
#         phemex = ccxt.phemex({
#             "enableRateLimit": True,
#             "apiKey": api_phemex,
#             "secret": secret_phemex
#         })
        
#         with open('funk/coins_phemex.txt', 'r', encoding='utf-8') as file:
#             coins = file.read().split()    
        
#         markets = phemex.fetch_tickers()
        
        
#         for coin in markets:
#             coin_dict = markets[coin]
#             formatted_number=0
            
#             if coin_dict["symbol"] in coins:
                
#                 if coin_dict["last"]!= None:
#                     number = float(coin_dict["last"])
#                     formatted_number = "{:.15f}".format(number)
#                 else:
#                     formatted_number=None

#                 db.insert_coin_info_for_burse('Phemex', coin_dict["symbol"].replace('/', ''), formatted_number)
    
#         print(f"Время выполнения загрузки в бд Phemex: {time.time()-start_Phemex}")
#         return True
#     except Exception as ex:
#         print("Ошибка Phemex",ex)
#         return False

        
# # Загрузка  биржи huobi
# def get_current_info_hyobi(db):
#     # Устанавливаем соединение с базой данных
#     # connection = sqlite3.connect('my_database.db')
#         # cursor = connection.cursor()
#     try:
#         start_Hyobi = time.time()
#         successful_counter = 0
#         unsuccesful_counter = 0
#         # Создаем объект биржи Huobi
#         start_time = time.time()
#         exchange = ccxt.huobi({
#             'enableRateLimit': False,  # Включить ограничение скорости запросов
#         })


#         # Получаем список доступных валютных пар
#         markets = exchange
#         # print(markets)
#         # Выводим цены и объем торгов всех валютных пар
#         with open('funk/coins_huobi.txt', 'r', encoding='utf-8') as file:
#             coins = file.read().split()
#         for symbol in coins:

#             try:
#                 # print(symbol)
#                 ticker = exchange.fetch_ticker(symbol)
#                 # print(f"Пара: {symbol}, Цена: {ticker['last']}")
#                 successful_counter += 1
#                 # print("успешных получений: ", successful_counter)
#                 number = float(ticker['last'])
#                 formatted_number = "{:.15f}".format(number)  # Указываем количество знаков после запятой
#                 # print(formatted_number)
#                 db.insert_coin_info_for_burse('Huobi', symbol.replace('/', ''), formatted_number)

#             except Exception as ex:
#                 unsuccesful_counter += 1
#                 # print("неуспешные: ", unsuccesful_counter)
#                 # print(ex)
#             # print(time.time()-start_time)
#         print(f"Время выполнения загрузки в бд Hyobi: {time.time()-start_Hyobi}")
#         return True
#             # Добавляем нового пользователя
#             # cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)',
#             #                ('newuser', 'newuser@example.com', 28))
#             #
#             # # Сохраняем изменения и закрываем соединение
#             # connection.commit()
#             # connection.close()
#     except Exception as ex:
#         print("Ошибка Huobi:",ex)
#         return False
# # 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111





# # 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# # Загрузка  биржи Gateio
# def get_current_info_Gateio(db):
#     start_GateIo = time.time()
#     url = 'https://api.gate.io/api2/1/tickers'
#     with open('funk/coins_gateio.txt', 'r', encoding='utf-8') as file:
#         coins = file.read().split()    

#     # for coin in coins:
#     #     print(coin.replace("-","_"))

#     # Выполняем GET-запрос
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()
#         for pair, info in data.items():
#             # print(pair)
#             # print(coins)
#             if pair in coins:
#                 last_price = info['last']  # Получаем последнюю цену
#                 db.insert_coin_info_for_burse('GateIo', pair.replace('_', '').upper(), last_price)  
#         print(f"Время выполнения загрузки в бд Gate.Io: {time.time()-start_GateIo}")
#         return True
#     else:
#         print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
#         return False


# # 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

# # Получение данных с okx
# def get_current_info_Okx(db):
#     start_Okx = time.time()
#     with open('funk/coins_okx.txt', 'r', encoding='utf-8') as file:
#         coins = file.read().split()       
#     api_okx, secret_okx, passphrase = tuple(api_Dict["OKX"].split("  "))
#     endpoint = '/api/v5/market/tickers'
#     url = 'https://www.okx.cab' + endpoint
#     timestamp = datetime.utcnow().isoformat("T", "milliseconds") + "Z"
#     signature = create_signature(timestamp, 'GET', endpoint, secret_okx)
#     headers = {
#         'OK-ACCESS-KEY': api_okx,
#         'OK-ACCESS-PASSPHRASE': passphrase,
#         'OK-ACCESS-TIMESTAMP': timestamp,
#         'OK-ACCESS-SIGN': signature
#     }
#     params = {
#         'instType': 'SPOT'  # Укажите желаемый тип инструмента
#     }    
#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         data = response.json()



#         for ticker in data['data']:
#             symbol = ticker['instId']
#             if symbol in coins:

                
#                 price = ticker['last']
#                 db.insert_coin_info_for_burse('OKX', symbol.replace('-', ''), price) 
#         print(f"Время выполнения загрузки в бд Okx: {time.time()-start_Okx}")
#         return True
#     else:
#         print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")    
#         return False
# # check_binance()
# # check_bybit()
# # check_kucoin()
# # check_phemex()
# # chech_huobi()
# # chech_gateIo()