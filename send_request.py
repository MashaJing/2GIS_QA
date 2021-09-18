import requests

# title - Название места. Может содержать латинские и кириллические символы, цифры и знаки
#препинания. Минимальная длина — 1 символ. Максимальная длина — 999 символов

#lat - Широта (latitude) места

#lon - Долгота (longitude) места

#color - Цвет иконки места. Может принимать значения: BLUE, GREEN, RED, YELLOW

#автотест = ф-ия отправки запроса + тест

def get_token(s):

    request = s.post('https://regions-test.2gis.com/v1/auth/tokens')
    dict_cookie = requests.utils.dict_from_cookiejar(request.cookies)
    token = dict_cookie['token']
    return token


s = requests.Session()

cookies = { 'token': get_token(s) }

data = {
    'title' : 'Камень',
    'lat': '55.036500',
    'lon': '82.925642'
    }

r = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=cookies, data=data)
print(r.json())
