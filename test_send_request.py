import unittest
from send_request import create_place, get_token
import requests

class TestCreatePlace(unittest.TestCase):
    def test_request(self):
        s = requests.Session()
        token = get_token(s)
        data = {
        'title' : 'Камень',
        'lat': '-55.036500', 
        'lon': '-82.925642',
        'color': 'blue' 
        }
        dict_res = create_place(token, data)
        print(dict_res)
        self.assertEqual(dict_res['lon'], -82.925642)

#def check_token():
