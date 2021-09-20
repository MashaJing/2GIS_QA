import datetime
#import traceback
import time
import requests
from requests import cookies

def get_token(s):
    request = s.post('https://regions-test.2gis.com/v1/auth/tokens')
    dict_cookie = requests.utils.dict_from_cookiejar(request.cookies)
    start_time = time.time() #зафиксируем время получения токена
    dict_cookie.update({'time' : start_time})
    return dict_cookie #токен в виде словаря {'token': 'значение_токена', 'time' : время получения токена}

def refresh_token(func):
    def wrapper(token, data):
        if time.time() - token['time'] < 1.6: #если от получения токена прошло менее 1.6 с
            #выполняем с тем же токеном
            return func(token, data)
        else:
            # миначе обращаемся к функции и получаем новый токен
            s = requests.Session()
            new_token = get_token(s)
            # обновив токен, пытаемся повторить действие
            return func(new_token, data)
    return wrapper

@refresh_token
def create_place(dict_token, data): 
    cookies = {'token' : dict_token['token'] } #??
    r = requests.post('https://regions-test.2gis.com/v1/favorites', cookies = cookies, data=data)
    
    return r.json()
'''
s = requests.Session()
data = {
    'title' : 'Камень',     # title - Название места. Может содержать латинские и кириллические символы, цифры и знаки
                            #препинания. Минимальная длина — 1 символ. Максимальная длина — 999 символов
    'lat': '55.036500',    #lat - Широта (latitude) места
    'lon': '82.925642',    #lon - Долгота (longitude) места
    'color': 'BLUE'        #color - Цвет иконки места. Может принимать значения: BLUE, GREEN, RED, YELLOW
    }
token = get_token(s)
dict_res = create_place(token, data)
print(dict_res)
time.sleep(1)
dict_res = create_place(token, data)
print(dict_res)
'''