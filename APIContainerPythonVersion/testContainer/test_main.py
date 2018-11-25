#Script to test a running container
import unittest
import requests

baseURL="http://shopping_basket_technical_test:8098"

class test_containerAPI(unittest.TestCase):
#Actual tests below

  def test_WeCanGetToSwaggerFile(self):
    result = requests.get(baseURL + "/api/swagger.json")
    self.assertEqual(result.status_code, 200)
    
