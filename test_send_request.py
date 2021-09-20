import unittest
from send_request import create_place, get_token
import requests
import datetime

class TestCreatePlace(unittest.TestCase):
    
    def data_init(self):
        self.data = {
        'title' : 'Камень',
        'lat': '55.036500', 
        'lon': '82.925642'
        }

    def test_request(self):
        s = requests.Session()
        token = get_token(s)
        self.data_init()
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['lon'], float(self.data['lon']))
        self.assertEqual(dict_res['lat'],  float(self.data['lat']))
        self.assertEqual(dict_res['title'], self.data['title'])
        
    def test_id(self):
        s = requests.Session()
        token = get_token(s)
        self.data_init()
        
        dict_res = []
        dict_res.append(create_place(token, self.data))
        for i in range(9):
            dict_res.append(create_place(token, self.data))
            self.assertGreater(dict_res[i+1]['id'], dict_res[i]['id'])


    def test_title(self):
        s = requests.Session()
        token = get_token(s)
        #по очереди занулим каждое значение в данных
        self.data_init()
        self.data['title'] = None
        dict_res = create_place(token, self.data)
        self.assertIn('error', dict_res.keys())
        
        #присвоим слишком большое значение
        #self.data_init()
        #self.data['title'] = 'T'*1000           #может быть 1000! тз:999 - при 1000 ломает тест
        #dict_res = create_place(token, self.data)
        #self.assertIn('error', dict_res.keys())
        
        
        #присвоим крайние воможные значения
        self.data_init()
        self.data['title'] = 'R'*333 + ','*333 + 'э'*333 #999 символов разных типов
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['title'], self.data['title'])

        self.data_init()
        self.data['title'] = ','*999    #999 запятых
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['title'], self.data['title'])
        
        self.data_init()
        self.data['title'] = 'z'*999    #999 латинских
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['title'], self.data['title'])
        
        self.data_init()
        self.data['title'] = 'ё'*999    #999 символов кириллицы
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 
        
        #присвоим самое маленькое значение
        self.data_init()
        self.data['title'] = '0'
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 
        
        self.data_init()
        self.data['title'] = '.'
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 

        self.data_init()
        self.data['title'] = 'й'
        dict_res = create_place(token, self.data)
        self.assertEqual(dict_res['title'], self.data['title']) 


    def test_lon(self):
        s = requests.Session()
        token = get_token(s)
        
        self.data_init()
        self.data['lon'] = None
        dict_res = create_place(token, self.data)
        self.assertIn('error', dict_res.keys())
               
        self.data_init()
        self.data['lon'] = 3000
        dict_res = create_place(token, self.data)
        self.assertIn('error', dict_res.keys())
    
        self.data_init()
        self.data['lon'] = 360      #долгота в диапазоне [-180; 180]
        dict_res = create_place(token, self.data)
        self.assertIn('error', dict_res.keys())
        

    def test_lat(self):
        s = requests.Session()
        token = get_token(s)
        
        self.data_init()
        self.data['lat'] = None
        dict_res = create_place(token, self.data)
        self.assertIn('error', dict_res.keys())

        self.data_init()
        self.data['lat'] = 3000
        dict_res = create_place(token, self.data)
        self.assertIn('error', dict_res.keys())

        self.data_init()
        self.data['lat'] = 180      #широта в диапазоне [-90; 90]
        dict_res = create_place(token, self.data)
        self.assertIn('error', dict_res.keys())

    #def test_date(self):
     #   s = requests.Session()
     #   token = get_token(s)
        
     #   self.data_init()
        
     #   dict_res = create_place(token, self.data)
     #   self.assertEqual(str(datetime.datetime.now), dict_res['created_at'])

    def test_color(self):
        s = requests.Session()
        token = get_token(s)
        
        self.data_init()
        colors = ['blue',  'green', 'red', 'yellow', 'BLUE', 'GREEN', 'RED', 'YELLOW', None]
        for color in colors:
            self.data['color'] = color
            dict_res = create_place(token, self.data)
            self.assertEqual(dict_res['color'], color)
        
        #colors_wrong = [ 'darkgreen', 'chocolate', 'brown', 'black', 'gray', 'white'] #'#FFFFFF', '0', 'grey', 'pink', 'gold', 'orange', 'maroon', 'violet', 'magenta', 'purple', 'navy', 'skyblue', 'cyan', 'turquoise', 'lightgreen', 
        #for color in colors_wrong:
            #self.data['color'] = color
            #dict_res = create_place(token, self.data)
            #print(dict_res)
            #self.assertIn('error', dict_res.keys()) #может быть brown
        
        





        
#def check_token():
