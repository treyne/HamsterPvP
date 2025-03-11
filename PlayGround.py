import httpx
import time
import random
import uuid
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Загрузка переменных из .env файла
load_dotenv()
Bearer = os.getenv('Token')
DEBUG = True
LOG_ON = False

# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post

configurations = [
    {'app_token': 'ed526e8c-e6c8-40fd-b72a-9e78ff6a2054', 'promo_id': 'ed526e8c-e6c8-40fd-b72a-9e78ff6a2054','rnd1':'60','rnd2':'100','game':'Cooking Stories'}, 
    {'app_token': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833', 'promo_id': 'dc128d28-c45b-411c-98ff-ac7726fbaea4','rnd1':'60','rnd2':'100','game':'Merge Away'},
    {'app_token': 'ab93d8d2-bd0b-47c9-98f6-e202f900b5df', 'promo_id': 'ab93d8d2-bd0b-47c9-98f6-e202f900b5df','rnd1':'60','rnd2':'100','game':'Draw To Smash'}, 
    {'app_token': 'd02fc404-8985-4305-87d8-32bd4e66bb16', 'promo_id': 'd02fc404-8985-4305-87d8-32bd4e66bb16','rnd1':'60','rnd2':'100','game':'Factory World'},         
    {'app_token': '13f7bd7c-b4b3-41f1-9905-a7db2e814bff', 'promo_id': '13f7bd7c-b4b3-41f1-9905-a7db2e814bff','rnd1':'60','rnd2':'100','game':'Merge Dale'},         
    {'app_token': 'e53b902b-d490-406f-9770-21a27fff1d31', 'promo_id': 'e53b902b-d490-406f-9770-21a27fff1d31','rnd1':'60','rnd2':'100','game':'Doodle God'},     
    {'app_token': 'bc72d3b9-8e91-4884-9c33-f72482f0db37', 'promo_id': 'bc72d3b9-8e91-4884-9c33-f72482f0db37','rnd1':'60','rnd2':'100','game':'Bouncemasters'},         
    {'app_token': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b', 'promo_id': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b','rnd1':'60','rnd2':'100','game':'Zoopolis'},     
    {'app_token': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71', 'promo_id': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71','rnd1':'60','rnd2':'100','game':'Polysphere'},     
    #{'app_token': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promo_id': 'b4170868-cef0-424f-8eb9-be0622e8e8e3','rnd1':'20','rnd2':'30','game':'Chain Cube 2048'},     
    #{'app_token': '82647f43-3f87-402d-88dd-09a90025313f', 'promo_id': 'c4480ac7-e178-4973-8061-9ed5b2e17954','rnd1':'125','rnd2':'140','game':'Train Miner'},   
    #{'app_token': 'eb518c4b-e448-4065-9d33-06f3039f0fcb', 'promo_id': 'eb518c4b-e448-4065-9d33-06f3039f0fcb','rnd1':'100','rnd2':'122','game':'Infected Frontier'},  
    #{'app_token': '53bf823a-948c-48c4-8bd5-9c21903416df', 'promo_id': '53bf823a-948c-48c4-8bd5-9c21903416df','rnd1':'100','rnd2':'122','game':'Tower Defense'},    
    
]

def debug_print(*args):
    if DEBUG:
        print(*args)



def LOG(*args):
    if LOG_ON:
        current_time = datetime.now()
        file_name = f"PlayGround_{current_time.strftime('%d.%m.%Y_%H-%M')}.txt"
        try:
            with open(file_name, 'a', encoding='utf-8') as file:
                file.write(' '.join(map(str, args)) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")



def countdown_timer(seconds, text):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = text + " {:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print(' ' * len(timer), end='\r')



def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"



def login_client(app_token):
    client_id = generate_client_id()
    try:
        with httpx.Client(http2=True) as client:
            response = client.post('https://api.gamepromo.io/promo/login-client', json={
                'appToken': app_token,
                'clientId': client_id,
                'clientOrigin': 'android',
            }, headers={'Content-Type': 'application/json; charset=utf-8'})
            response.raise_for_status()
            data = response.json()
            print('login-client [clientToken] = ', data['clientToken'])
            LOG('login-client [clientToken] = ', data['clientToken'])
            return data['clientToken']
    except httpx.RequestError as error:
        print(f'Ошибка при входе клиента: {error}')
        LOG(f'Ошибка при входе клиента: {error}')
        countdown_timer(20, 'timer after login_client Error')
        return login_client(app_token)


def register_event(token, promo_id, delay):
    event_id = str(uuid.uuid4())
    try:
        with httpx.Client(http2=True) as client:
            response = client.post('https://api.gamepromo.io/promo/register-event', json={
                'promoId': promo_id,
                'eventId': event_id,
                'eventOrigin': 'undefined'
            }, headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json; charset=utf-8',
            })
            response.raise_for_status()
            data = response.json()
            if not data.get('hasCode', False):
                countdown_timer(random.randint(delay[0], delay[1]), 'next try register_event')
                return register_event(token, promo_id, delay)
            return True
    except httpx.RequestError as error:
        print(f'Ошибка при register_event: {error}')
        LOG(f'Ошибка при register_event: {error}')
        countdown_timer(120, 'Задержка после ошибки register_event')
        return register_event(token, promo_id, delay)




def create_code(token, promo_id):
    while True:
        try:
            with httpx.Client(http2=True) as client:
                response = client.post('https://api.gamepromo.io/promo/create-code', json={
                    'promoId': promo_id
                }, headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json; charset=utf-8',
                })
                response.raise_for_status()
                data = response.json()
                return data['promoCode']
        except httpx.RequestError as error:
            print(f'Ошибка при создании кода: {error}')
            LOG(f'Ошибка при создании кода: {error}')
            countdown_timer(120, 'Задержка после ошибки создания кода')






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



   
    
    
def main():
    i = 0
    while i < 4:
        for config in configurations:
            token = login_client(config['app_token'])
            countdown_timer(random.randint(80, 100), 'wait for login')
            register_event(token, config['promo_id'], (int(config['rnd1']), int(config['rnd2'])))
            code_data = create_code(token, config['promo_id'])
            print(f'Сгенерированный код для {config['game']}: {code_data}')
            LOG(f'Сгенерированный код для {config['game']}: {code_data}')
            # print(f'Тест для {config['game']}: Test')
            url = "https://node1.cl.hamsterpvp.com/prod/bitquest/code/apply"
            httpx_request(url, "POST", data={"payload":{"promoCode":code_data}})
        i += 1        
        countdown_timer(random.randint(14450,14495 ), 'До следующего пака ключей')    
    
    
    




if __name__ == "__main__":
    main()

