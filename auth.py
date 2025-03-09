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





url = input("Введите строку авторизации: ")  # Ожидаем ввод от пользователя

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


 