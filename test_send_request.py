from send_request import create_place, get_token
import unittest
import requests

#def check_token():


class TestCreatePlace(unittest.TestCase):
    def test_request(self):
        s = requests.Session()
        token = get_token(s)
        data = {
        'title' : 'Камень',
        'lat': '55.036500', 
        'lon': '82.925642',
        'color': 'BLUE' 
        }
        self.assertDictEqual(create_place(token, data), ...)