from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from unittest.mock import patch, call
from shoppingBasket import PriceValidatyDuration
from appObj import appObj

class test_api(testHelperAPIClient):
  def test_getShoppingBasketWithZeroItems(self):
    return

  @patch('CurrencyConverter.CurrencyConverter.convertFromGBPtoUSD')
  def test_getShoppingBasketWithZeroItems(self,mockConvertFromGBPtoUSD):
    responses = []
    responses.append(123)
    mockConvertFromGBPtoUSD.side_effect = responses

    curDateTime = appObj.getCurDateTime()
    appObj.setTestingDateTime(curDateTime)
    expectedPriceExpiryDateTime = curDateTime + PriceValidatyDuration


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
      },
      'Totals': {
        'DiscountPercentage': 10,
        'TotalPayable': {'Amount': 0, 'CurrencyCode': 'USD'}
        },
      'PriceExpiry': expectedPriceExpiryDateTime.isoformat()
    }
    actualResult = self.testClient.post('/api/shoppingBasket/',json=inputPayloadWithZeroItems)
    self.assertEqual(actualResult.status_code, 200)
    actualResultJSON = json.loads(actualResult.get_data(as_text=True))
    self.assertJSONStringsEqual(actualResultJSON, expectedResult)
'''
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
