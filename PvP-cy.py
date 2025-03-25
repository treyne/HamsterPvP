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
                    return response_json,response.status_code
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


         


def Auth():
    def httpx(string):
        import httpx
        url = "https://node1.cl.hamsterpvp.com/prod/auth/telegram"
        headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"}
        body  = f"initData={string}"
        
        
        try:
            with httpx.Client(http2=True, timeout=10.0) as client:
                response = client.post(url, headers=headers, data=body)
            print(f"Status Code: {response.status_code}")
            if response.content:
                try:
                    response_json = response.json()
                    print('info = ', response_json)
                    return response_json
                    
                except json.JSONDecodeError as e:
                    print("JSON decode error: ", e)
                    return None
        except httpx.RequestError as e:
            print(f"Ошибка сети: {e}")
            return None


    with open("auth.txt", "r", encoding="utf-8") as file:
        authURL = file.read().strip()  # Читаем содержимое и удаляем лишние пробелы/переносы строк
        url = authURL
    # print(authURL)  # Вывод для проверки
    # url = input("Введите строку авторизации: ")  # Ожидаем ввод от пользователя
    
    
    

    query_start = url.find("query_id%3D")

    if query_start != -1:
        trimmed_url = url[query_start:]
        # print(trimmed_url)
    else:
        print("query_id не найден")
        
            
    telegramAuth = httpx(trimmed_url)
    token = telegramAuth["payload"]["token"]


    import re
    env_file = ".env"  # Имя файла .env

    # Читаем содержимое .env
    with open(env_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Заменяем строку Token = <значение> 
    updated_content = re.sub(r"^Token\s*=\s*.*$", f"Token = {token}", content, flags=re.MULTILINE)

    # Записываем обратно в .env
    with open(env_file, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print(f"Значение Token заменено на {token}")




def checkAuth(con):
    url = f"https://{con}/prod/profile/get"
    ADS_resp = httpx_request(url, "POST", data={})  # POST с JSON
    if ADS_resp[1] == 200:
        print("Полная норма, продолжаем.")
        return False
    if ADS_resp[1] == 401:
        print("Токен просрочен! Нужен новый.")
        return 'start'

                
           
def ADS(con):
    url = f"https://{con}/prod/ads/rewarded/info"
    print (url)
    viewsCount = httpx_request(url, "POST", data={})[0]
    print (viewsCount)
    viewsCount = viewsCount["payload"]["rewarded"]["viewsCount"] 
    if viewsCount < 10:
        for _ in range(10 - viewsCount):
            url = f"https://{con}/prod/ads/rewarded/watched"
            ADS_resp = httpx_request(url, "POST", data={})
            if ADS_resp[1] == 200:
                countdown_timer(random.randint(10, 20),'До следующей рекламы: ')
            if ADS_resp[1] == 401:    
                Auth()
    else:
        print ("Всю рекламу уже посмотрели")         
    return None



def start(con, tryFlag=False):
    url = f"https://{con}/prod/profile/get"
    AccounInfo = httpx_request(url, "POST", data={})[0]  # POST с JSON
    energy = AccounInfo["payload"]["items"]["energy"]["count"]
    ownerId = AccounInfo["payload"]["unit"]["ownerId"]
    energyUncommonBooster = AccounInfo["payload"]["items"]["energyUncommonBooster"]["count"]
    print (AccounInfo["payload"]["items"]["energyUncommonBooster"]["count"])
    # if energyUncommonBooster > 0:
        # print (f"Применяем {energyUncommonBooster} бустеров")
        # for _ in range(energyUncommonBooster):
            # url = "https://node1.cl.hamsterpvp.com/prod/items/boost"
            # httpx_request(url, "POST", data={"payload":{"boosterId":"energyUncommonBooster"}})
            # countdown_timer(random.randint(1, 3),'До применения следующего бустера: ')
    # else:
        # print ("Бустеров нет!")


    countBattle = energy // 25
    if countBattle > 0:
        print (f"Число раундов = {countBattle}")
        print (f"Энергия = {energy}")
        for _ in range(countBattle):
            url = f"https://{con}/prod/pvp/start"
            BattleInfo = httpx_request(url, "POST", data={})[0]  # POST с JSON
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
                BattleInfo = httpx_request(url, "POST", data={})[0]  # POST с JSON
                tryFlag = True
                print (f"Энергия = {energy}")
                return start(con, tryFlag=True)  # Передаём изменённое значение флага
        else:
            print (f"Энергия = {energy}")
            print (f"Не хватает энергии!")

                
def balancer():
    url = "https://balancer.cl.hamsterpvp.com/connections"
    response = httpx_request(url, "GET", {})  # GET с параметрами
    return response[0]
    
    


connections = balancer()
ads_con = random.choice(connections)
print (ads_con)
auth = checkAuth(ads_con)

if auth=="start":
    Auth()

ADS(ads_con)
start(random.choice(connections))

countdown_timer(1500,'До следующего раунда: ')

while True:
    auth = checkAuth(ads_con)
    if auth=="start":
        Auth()
    ADS(ads_con)    
    start(random.choice(connections))
    countdown_timer(1500,'До следующего раунда: ')
