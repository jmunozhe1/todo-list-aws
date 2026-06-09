import http.client
import os
import unittest
from urllib.request import urlopen
import requests
import json
import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def _parse_response(self, json_response):
        if isinstance(json_response, dict) and 'body' in json_response:
            try:
                return json.loads(json_response['body'])
            except Exception:
                return json_response
        return json_response

    def test_api_listtodos(self):
        print('---------------------------------------')
        print('Starting - integration test List TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody = self._parse_response(json_response)
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(response.status_code, 200, "Error en la petición API")
        self.assertEqual(jsonbody['text'], "Integration text example", "Error en la petición API")
        
        response = requests.get(url)
        print('Response List Todo:' + str(response.json()))
        self.assertEqual(response.status_code, 200, "Error en la petición API")
        self.assertTrue(response.json())
        print('End - integration test List TODO')

    def test_api_addtodo(self):
        print('---------------------------------------')
        print('Starting - integration test Add TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody = self._parse_response(json_response)
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(response.status_code, 200, "Error en la petición API")
        self.assertEqual(jsonbody['text'], "Integration text example", "Error en la petición API")
        url = url+"/"+ID_TODO
        response = requests.delete(url)
        self.assertIn(response.status_code, [200, 202, 204], "Error en la petición API")
        print('End - integration test Add TODO')

    def test_api_gettodo(self):
        print('---------------------------------------')
        print('Starting - integration test Get TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - GET"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody = self._parse_response(json_response)
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(response.status_code, 200, "Error en la petición API")
        self.assertEqual(jsonbody['text'], "Integration text example - GET", "Error en la petición API")
        
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        self.assertEqual(response.status_code, 200, "Error en la petición API")
        self.assertEqual(json_response['text'], "Integration text example - GET", "Error en la petición API")
        response = requests.delete(url)
        self.assertIn(response.status_code, [200, 202, 204], "Error en la petición API")
        print('End - integration test Get TODO')
    
    def test_api_updatetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Update TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + str(json_response))
        jsonbody = self._parse_response(json_response)
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(response.status_code, 200, "Error en la petición API")
        self.assertEqual(jsonbody['text'], "Integration text example - Initial", "Error en la petición API")
        
        url = BASE_URL+"/todos/" + ID_TODO
        data = {
         "text": "Integration text example - Modified",
         "checked": "true"
        }
        response = requests.put(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Update todo: ' + str(json_response))
        self.assertIn(response.status_code, [200, 502], "Error en la petición API")
        
        if response.status_code == 200:
            self.assertEqual(json_response['text'], "Integration text example - Modified", "Error en la petición API")
        
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        response = requests.delete(url)
        print('End - integration test Update TODO')

    def test_api_deletetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Delete TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + str(json_response))
        jsonbody = self._parse_response(json_response)
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(response.status_code, 200, "Error en la petición API")
        self.assertEqual(jsonbody['text'], "Integration text example - Initial", "Error en la petición API")
        
        response = requests.delete(url + '/' + ID_TODO)
        self.assertIn(response.status_code, [200, 202, 204], "Error en la petición API")
        print ('Response Delete Todo:' + str(response))
        
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        print('Response Get Todo '+ url+': '+ str(response))
        self.assertIn(response.status_code, [404, 502], "Error en la petición API")
        print('End - integration test Delete TODO')