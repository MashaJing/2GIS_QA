#import datetime
#import traceback
import time
import requests
from requests import cookies

class req_sneder():
    #общая сессия для всех запросов
    s = requests.Session()
    #токен
    token = None
    #время получения токена
    token_time = None

    def __init__(self):
        self.get_token()
        self.s = requests.Session()

    #посылает пустой post-запрос для получения токена
    def get_token(self):
        request = self.s.post('https://regions-test.2gis.com/v1/auth/tokens')
        self.token = requests.utils.dict_from_cookiejar(request.cookies)['token']
        self.token_time = time.time() #зафиксируем время получения токена

    #декоратор для обновления токена по необходимости
    def refresh_token(func):
        def wrapper(self, data):
            if time.time() - self.token_time < 1.6: #если от получения токена прошло менее 2 секунд с учетом погрешности
                #выполняем с тем же токеном
                return func(self, data)
            else:
                # иначе обращаемся к функции и получаем новый токен
                self.get_token()
                # обновив токен, пытаемся повторить действие
                return func(self, data)
        return wrapper

    #метод создания избранного места
    @refresh_token
    def create_place(self, data): 
        cookies = {'token' : self.token }
        r = requests.post('https://regions-test.2gis.com/v1/favorites', cookies = cookies, data=data)
        
        if r.status_code != 200:
            raise ConnectionError
        return r.json()

'''
req = req_sneder()
data = {
    'title' : 'Камень',     # title - Название места. Может содержать латинские и кириллические символы, цифры и знаки
                            #препинания. Минимальная длина — 1 символ. Максимальная длина — 999 символов
    'lat': '55.036500',    #lat - Широта (latitude) места
    'lon': '82.925642',    #lon - Долгота (longitude) места
    'color': 'BLUE'        #color - Цвет иконки места. Может принимать значения: BLUE, GREEN, RED, YELLOW
    }

dict_res = req.create_place(data)
print(dict_res)
time.sleep(2)
dict_res = req.create_place(data)
print(dict_res)
'''


