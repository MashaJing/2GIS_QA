import requests
from requests import cookies

def get_token(s):
    request = s.post('https://regions-test.2gis.com/v1/auth/tokens')
    dict_cookie = requests.utils.dict_from_cookiejar(request.cookies)
    return dict_cookie #токен в виде словаря {'token': 'значение_токена', 'date': 'время создания'}


def create_place(token, data): 
    cookies = { 'token' : token }
    r = requests.post('https://regions-test.2gis.com/v1/favorites', cookies = cookies, data=data)
    return r.json()

s = requests.Session()
data = {
    'title' : 'Камень',     # title - Название места. Может содержать латинские и кириллические символы, цифры и знаки
                            #препинания. Минимальная длина — 1 символ. Максимальная длина — 999 символов
    'lat': '55.036500',    #lat - Широта (latitude) места
    'lon': '82.925642',    #lon - Долгота (longitude) места
    'color': 'BLUE'        #color - Цвет иконки места. Может принимать значения: BLUE, GREEN, RED, YELLOW
    }
dict_token = get_token(s)
print(create_place(dict_token['token'], data))
