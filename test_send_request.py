from math import inf
import unittest
from send_request import req_sneder
#import requests
import re

class TestCreatePlace(unittest.TestCase):
    #Данные для запросов
    data = {}
    #Объект для отправки запросов и автоматического получения/обновления токенов
    sender = req_sneder()

    def data_init(self):
        self.data = {
        'title': 'Камень',
        'lat': '55.036500', 
        'lon': '82.925642',
        'color': None
        }


    def test_request(self):

        try:
            
            self.data_init() 
            self.sender.create_place(self.data) 
        
            
            self.data = {
            'title' : 'Камень',
            'lat': 75, 
            'lon': 44 }
            
            self.sender.create_place(self.data)

            self.data = {
            'title' : 'Камень',
            'lat': '0.0', 
            'lon': '0.0' }
            
            self.sender.create_place(self.data) #ошибка 500

            self.data = {
            'title' : 'Камень',
            'lat': 89, 
            'lon': 179 }
            self.sender.create_place(self.data)
            
            self.data = {
            'title' : 'Камень',
            'lat': 9, 
            'lon': 10 }
            self.sender.create_place(self.data)

        except ConnectionError:
            self.fail("test_request() raised ConnectionError unexpectedly!")
    

    def test_id(self):
        #каждый тест строится в 2 этапа:
        self.data_init() #1) инициализация данных для запроса
        res = []
        #2) Изучение резултатов запроса: например, проверим монотонное возрастание индекса и его тип
        res.append(self.sender.create_place(self.data)) 
        for i in range(1):
            res.append(self.sender.create_place(self.data))
            self.assertGreater(res[i+1]['id'], res[i]['id'])
            self.assertEqual(type(res[i]['id']), int)


    def test_title(self):
        #занулим заголовок
        self.data_init()
        self.data['title'] = None
        with self.assertRaises(ConnectionError):
            self.sender.create_place(self.data)
            
    
        self.data['title'] = '你好'       #может быть иероглифами
        with self.assertRaises(ConnectionError):
            self.sender.create_place(self.data)
    
        
        #присвоим слишком большое значение
        self.data['title'] = 'T'*1000           #может быть 1000, ТЗ:999
        with self.assertRaises(ConnectionError):
            self.sender.create_place(self.data)
    
        #присвоим крайние воможные значения.
        #самые большие возможные строки разного состава

        kir = 'ё'*999   #999 символов кириллицы
        lat = 'r'*999   #999 латинских
        punct = '.'*999 #999 знаков препинания
        digits = '123456789'*111 #999 цифр
        all_kinds = 'R'*333 + ','*333 + 'э'*330 + '3'*3 #999 символов разных типов

        for i in (digits, kir, lat, punct, all_kinds):
            self.data['title'] = i
            dict_res = self.sender.create_place(self.data)
            self.assertEqual(dict_res['title'], self.data['title'])

        #самые маленькие значения, строки со знаками препинания, пробелами
        with_spaces = 'текст с пробелами'
        many_punc = '!@#$%^&*()_+=-\|\|\'\'//?.,;[]{`~'

        for i in ('1', 'й', '.', 'q', many_punc, with_spaces):
            self.data['title'] = i
            dict_res = self.sender.create_place(self.data)
            self.assertEqual(dict_res['title'], self.data['title'])
     

    def test_lon(self):
        self.data_init()

        for i in (181, -181, inf, 'string', None, True, complex(1, 2)):
            self.data['lon'] = i
            with self.assertRaises(ConnectionError):
                self.sender.create_place(self.data)

        for i in (180, -180, -179, 179, 0): #долгота должна быть в диапазоне [-180; 180]
            self.data['lon'] = i
            dict_res = self.sender.create_place(self.data)
            self.assertEqual(dict_res['lon'], self.data['lon'])
            self.assertEqual(type(dict_res['lon']), float)
            

    def test_lat(self):
        self.data_init()

        for i in (91, -91, inf, 'string', None, True, complex(1, 2)):
            self.data['lat'] = i
            with self.assertRaises(ConnectionError):
                self.sender.create_place(self.data)

        for i in (90, 89, -90, -89, 0): #широта должна быть в диапазоне [-90; 90]
            self.data['lat'] = i
            dict_res = self.sender.create_place(self.data)
            self.assertEqual(dict_res['lat'], self.data['lat'])
            self.assertEqual(type(dict_res['lat']), float)


    def test_color(self):   
        self.data_init()
        colors = ['blue',  'green', 'red', 'yellow', 'BLUE', 'GREEN', 'RED', 'YELLOW', None]
        for color in colors:
            self.data['color'] = color
            dict_res = self.sender.create_place(self.data)
            self.assertEqual(dict_res['color'], color)
            
        colors_wrong = [ 'darkgreen', 'chocolate', 'black', 'gray', '', 'brown', '#FFFFFF', '0', 'grey', 'pink', 'gold', 'orange', 'maroon', 'violet', 'magenta', 'purple', 'navy', 'skyblue', 'cyan', 'turquoise', 'lightgreen', 'white']
        for color in colors_wrong:
          self.data['color'] = color
          with self.assertRaises(ConnectionError):    
              self.sender.create_place(self.data) #может быть brown

    
    def test_date(self):
       self.data_init()
       
       dict_res = self.sender.create_place(self.data)
       self.assertIsNotNone(re.match(r'\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}±\d{2}:\d{2}', dict_res['created_at']))
   #     #Регексом проверяем соответствие даты шаблону YYYY-MM-DDThh:mm:ss±hh:mm
   #     ломает тест: несоответствие формата
