from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from unittest.mock import patch, call
from shoppingBasket import PriceValidatyDuration, discountPercentage
from appObj import appObj

class test_api(testHelperAPIClient):
  def test_getShoppingBasketWithZeroItems(self):
    return

  @patch('CurrencyConverter.CurrencyConverter.convertFromGBPtoUSD')
  def test_getShoppingBasketWithZeroItems(self, mockConvertFromGBPtoUSD):
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

  @patch('CurrencyConverter.CurrencyConverter.convertFromGBPtoUSD')
  def test_getShoppingBasketWithSingleItem(self, mockConvertFromGBPtoUSD):
    preConversionItemAmount = 2000
    postConversionItemAmount = 2368
    
    discountAmount = int(round( postConversionItemAmount * (discountPercentage / 100),0))
    print(discountAmount)
    totalPayableAfterDiscount = postConversionItemAmount - ( discountAmount)
    
    responses = []
    responses.append(postConversionItemAmount)
    mockConvertFromGBPtoUSD.side_effect = responses

    curDateTime = appObj.getCurDateTime()
    appObj.setTestingDateTime(curDateTime)
    expectedPriceExpiryDateTime = curDateTime + PriceValidatyDuration

    inputPayloadWithOneItem = {
      'Basket': {
        'Items': [
          {
            'Description': 'Raspberry Pi',
            'ItemPrice': {'Amount': preConversionItemAmount, 'CurrencyCode': 'GBP'}
          }
        ]
      }
    }
    expectedResult = {
      'Basket': {
        'Items': [
          {
            'Description': 'Raspberry Pi',
            'ItemPrice': {'Amount': preConversionItemAmount, 'CurrencyCode': 'GBP'}
          }
        ],
      },
      'Totals': {
        'DiscountPercentage': 10,
        'TotalPayable': {'Amount': totalPayableAfterDiscount, 'CurrencyCode': 'USD'}
        },
      'PriceExpiry': expectedPriceExpiryDateTime.isoformat()
    }
    actualResult = self.testClient.post('/api/shoppingBasket/',json=inputPayloadWithOneItem)
    self.assertEqual(actualResult.status_code, 200)
    actualResultJSON = json.loads(actualResult.get_data(as_text=True))
    self.assertJSONStringsEqual(actualResultJSON, expectedResult)

