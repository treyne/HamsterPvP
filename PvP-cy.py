import time
import random
import os
import datetime
from dotenv import load_dotenv
import re
from datetime import datetime
import base64
import httpx
import json

# Загрузка переменных из .env файла
load_dotenv()
Bearer = os.getenv('Token')
DEBUG = False




# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post



def countdown_timer(seconds, text):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = text + " {:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")  # Перезаписываем строку
        time.sleep(1)
        seconds -= 1
    # Очищаем строку после завершения
    print(' ' * len(timer), end='\r')



def debug_print(*args):
    if DEBUG:
        print(*args)

   


def httpx_request(url, method, data=None):
    """Отправляет HTTP-запрос с указанным методом и данными."""
    
    headers_post = get_headers_post(Bearer)  # Получаем заголовки
    
    try:
        with httpx.Client(http2=True, timeout=10.0) as client:
            method_func = getattr(client, method.lower(), None)
            if method_func is None:
                debug_print(f"Ошибка: метод {method} не поддерживается")
                return None
            
            # Разные параметры для GET и остальных методов
            kwargs = {"headers": headers_post}
            if method.upper() == "GET":
                kwargs["params"] = data  # GET использует params
            else:
                kwargs["json"] = data  # Остальные методы используют json
            
            response = method_func(url, **kwargs)
            debug_print(f"Status Code: {response.status_code}")

            if response.content:
                try:
                    response_json = response.json()
                    debug_print("info =", response_json)
                    return response_json
                except json.JSONDecodeError as e:
                    debug_print("JSON decode error:", e)
                    return None
    except httpx.RequestError as e:
        debug_print(f"Ошибка сети: {e}")
        return None





def account_info(con):
    # payload.items.energy.count
    url = f"https://{con}/prod/profile/get"
    # perform_options_request(url)  # Выполняем OPTIONS-запрос
    accountInfo = httpx_request(url, "POST", data={})
    return accountInfo


         
                
           
def ADS(con):
    url = f"https://{con}/prod/ads/rewarded/info"
    viewsCount = httpx_request(url, "POST", data={})
    # print (viewsCount)
    viewsCount = viewsCount["payload"]["rewarded"]["viewsCount"] 
    if viewsCount < 10:
        for _ in range(10 - viewsCount):
            url = f"https://{con}/prod/ads/rewarded/watched"
            httpx_request(url, "POST", data={})
            countdown_timer(random.randint(10, 20),'До следующей рекламы: ')
    else:
        print ("Всю рекламу уже посмотрели")         
    return None



def start(con, tryFlag=False):
    url = f"https://{con}/prod/profile/get"
    AccounInfo = httpx_request(url, "POST", data={})  # POST с JSON
    energy = AccounInfo["payload"]["items"]["energy"]["count"]
    ownerId = AccounInfo["payload"]["unit"]["ownerId"]
    countBattle = energy // 25
    if countBattle > 0:
        print (f"Число раундов = {countBattle}")
        for _ in range(countBattle):
            url = f"https://{con}/prod/pvp/start"
            BattleInfo = httpx_request(url, "POST", data={})  # POST с JSON
            winnerId = BattleInfo["payload"]["battle"]["winnerId"]
            if winnerId == ownerId:
                print ("You Win!")
                print (f"You ID = {ownerId}")
            else:
                print ("You Lose!")
                print (f"Winner ID = {winnerId}")
            countdown_timer(random.randint(10, 20),'До следующего раунда: ')    
    else:
        if not tryFlag:
                print ("Один раз пробуем на тоненького!")
                url = f"https://{con}/prod/pvp/start"
                BattleInfo = httpx_request(url, "POST", data={})  # POST с JSON
                tryFlag = True
                print (f"Энергия = {energy}")
                return start(con, tryFlag=True)  # Передаём изменённое значение флага
        else:
            print (f"Энергия = {energy}")
            print (f"Не хватает энергии!")

                
def balancer():
    url = "https://balancer.cl.hamsterpvp.com/connections"
    response = httpx_request(url, "GET", {})  # GET с параметрами
    return response
    
    


connections = balancer()
ads_con = random.choice(connections)
print (ads_con)
ADS(ads_con)
start(random.choice(connections))

