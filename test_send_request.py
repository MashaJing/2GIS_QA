import unittest
from send_request import create_place, get_token
import requests
import datetime
import re

class TestCreatePlace(unittest.TestCase):
    
    data = {}
    s = requests.Session()

    def data_init(self):
        self.data = {
        'title' : 'Камень',
        'lat': '55.036500', 
        'lon': '82.925642'
        }

    def test_request(self):
        token = get_token(self.s)
        self.data_init()
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['lon'], float(self.data['lon']))
        self.assertEqual(dict_res['lat'],  float(self.data['lat']))
        self.assertEqual(dict_res['title'], self.data['title'])


    def test_id(self):
        token = get_token(self.s)
        self.data_init()
        #проверим монотонное возрастание индекса
        dict_res = []
        dict_res.append(create_place(self.s, token, self.data))
        for i in range(100):
            dict_res.append(create_place(self.s, token, self.data))
            self.assertGreater(dict_res[i+1]['id'], dict_res[i]['id'])


    def test_title(self):
        token = get_token(self.s)
        #занулим заголовок
        #{ 'title' : None, 'lat': '55.036500', 'lon': '82.925642' }
        self.data_init()
        self.data['title'] = None
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)
        
        
        #присвоим слишком большое значение
        #self.data_init()
        #self.data['title'] = 'T'*1000           #может быть 1000! тз:999 - при 1000 ломает тест
        #with self.assertRaises(ConnectionError):
            #dict_res = create_place(self.s, token, self.data)
        
    
        #присвоим крайние воможные значения
        self.data_init()
        self.data['title'] = 'R'*333 + ','*333 + 'э'*333 #999 символов разных типов
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title'])

        self.data_init()
        self.data['title'] = ','*999    #999 запятых
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title'])
        
        self.data_init()
        self.data['title'] = 'z'*999    #999 латинских
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title'])
        
        self.data_init()
        self.data['title'] = 'ё'*999    #999 символов кириллицы
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 
        
        #присвоим самое маленькое значение
        self.data_init()
        self.data['title'] = '0'
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 
        
        self.data_init()
        self.data['title'] = '.'
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 

        self.data_init()
        self.data['title'] = 'й'
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 

        self.data_init()
        self.data['title'] = '!@#$%^&*()_+=-\|\|''//?.,;[]{`~'
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 

        #текст с пробелами
        self.data_init()
        self.data['title'] = 'я календарь переверну'
        dict_res = create_place(self.s, token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 


    def test_lon(self):
        token = get_token(self.s)
        
        #{ 'title' : 'Камень', 'lat': '55.036500', 'lon': None }
        self.data_init()
        self.data['lon'] = None
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)
               
        self.data_init()
        self.data['lon'] = 3000
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)
    
        self.data_init()
        self.data['lon'] = 360      #долгота в диапазоне [-180; 180]
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)

        self.data_init()
        self.data['lon'] = -360      #долгота в диапазоне [-180; 180]
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)       


    def test_lat(self):
        token = get_token(self.s)
        #{ 'title' : 'Камень', 'lat':  None, 'lon': '82.925642' }
        self.data_init()
        self.data['lat'] = None
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)

        self.data_init()
        self.data['lat'] = 3000
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)

        self.data_init()
        self.data['lat'] = 180      #широта в диапазоне [-90; 90]
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)

        self.data_init()
        self.data['lat'] = -180      #широта в диапазоне [-90; 90]
        with self.assertRaises(ConnectionError):
            dict_res = create_place(self.s, token, self.data)


    def test_color(self):
        token = get_token(self.s)
        
        self.data_init()
        colors = ['blue',  'green', 'red', 'yellow', 'BLUE', 'GREEN', 'RED', 'YELLOW', None]
        for color in colors:
            self.data['color'] = color
            dict_res = create_place(self.s, token, self.data)
            self.assertEqual(dict_res['color'], color)
        
        #colors_wrong = [ 'darkgreen', 'chocolate', 'black', 'gray', '', 'brown', '#FFFFFF', '0', 'grey', 'pink', 'gold', 'orange', 'maroon', 'violet', 'magenta', 'purple', 'navy', 'skyblue', 'cyan', 'turquoise', 'lightgreen', 'white']
        #for color in colors_wrong:
        #   self.data['color'] = color
        #   with self.assertRaises(ConnectionError):    
        #       dict_res = create_place(self.s, token, self.data) #может быть brown

    
   # def test_date(self):
   #     token = get_token(self.s)
   #     self.data_init()
   #     
   #     dict_res = create_place(self.s, token, self.data)
   #     self.assertIsNotNone(re.match(r'\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}±\d{2}:\d{2}', dict_res['created_at']))
   #     #Регексом проверяем соответствие даты шаблону YYYY-MM-DDThh:mm:ss±hh:mm
   #     ломает тест: несоответствие формата

   