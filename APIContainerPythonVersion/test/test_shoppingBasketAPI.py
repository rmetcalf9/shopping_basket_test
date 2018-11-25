from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json

class test_api(testHelperAPIClient):
  def test_getShoppingBasketWithZeroItems(self):
    return
'''
  def test_getShoppingBasketWithZeroItems(self):
    inputPayloadWithZeroItems = {
      'Basket': {
        'Items': [
        ]
      }
    }
    expectedResult = {
      'Basket': {
        'Items': [
        ]
      }
    }
    actualResult = self.testClient.post('/api/basket/',json=inputPayloadWithZeroItems)
    self.assertEqual(actualResult.status_code, 200)
    actualResultJSON = json.loads(actualResult.get_data(as_text=True))
    self.assertJSONStringsEqual(actualResultJSON, expRes)

  def test_getShoppingBasketWithSingleItem(self):
    inputPayloadWithZeroItems = {
      'Basket': {
        'Items': [
          {
            'Description': 'Raspberry Pi',
            'ItemPrice': {'Amount': 2000, 'CurrencyCode': 'GBP'}
          }
        ]
      }
    }
    expectedResult = {
      'Basket': {
        'Items': [
          {
            'Description': 'Raspberry Pi',
            'ItemPrice': {'Amount': 2000, 'CurrencyCode': 'GBP'}
          }
        ],
        'Totals': {
          'DiscountPercentage': 10,
          'TotalPayable': {'Amount': 2568, 'CurrencyCode': 'USD'}
          },
        'PriceExpiry': 'TODODATE'
        }
    }
    actualResult = self.testClient.post('/api/basket/',json=inputPayloadWithZeroItems)
    self.assertEqual(actualResult.status_code, 200)
    actualResultJSON = json.loads(actualResult.get_data(as_text=True))
    self.assertJSONStringsEqual(actualResultJSON, expRes)
'''