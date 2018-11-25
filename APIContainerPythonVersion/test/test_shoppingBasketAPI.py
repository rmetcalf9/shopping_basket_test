from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from unittest.mock import patch, call
from shoppingBasket import PriceValidatyDuration, discountPercentage
from appObj import appObj
import copy

inputPayloadWithZeroItems = {
  'Basket': {
    'Items': [
    ]
  }
}


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

    #If we have a 0 total cost the function hsould not try and convert
    self.assertEqual(mockConvertFromGBPtoUSD.call_args_list,[],"Wrong calls to API")


  @patch('CurrencyConverter.CurrencyConverter.convertFromGBPtoUSD')
  def test_getShoppingBasketWithSingleItem(self, mockConvertFromGBPtoUSD):
    preConversionItemAmount = 2000
    postConversionItemAmount = 2368
    
    #since the discount is applied BEFORE the conversion and we are mocking the conversion function
    #with a fixed result the discount amount will not effect the output
    
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
        'TotalPayable': {'Amount': postConversionItemAmount, 'CurrencyCode': 'USD'}
        },
      'PriceExpiry': expectedPriceExpiryDateTime.isoformat()
    }
    actualResult = self.testClient.post('/api/shoppingBasket/',json=inputPayloadWithOneItem)
    self.assertEqual(actualResult.status_code, 200)
    actualResultJSON = json.loads(actualResult.get_data(as_text=True))
    self.assertJSONStringsEqual(actualResultJSON, expectedResult)

    #Finally we must also check the discount was correctly applied
    discountToApply = preConversionItemAmount * (discountPercentage / 100)
    self.assertEqual(mockConvertFromGBPtoUSD.call_args_list,[call(preConversionItemAmount - discountToApply)],"Wrong calls to API")

  @patch('CurrencyConverter.CurrencyConverter.convertFromGBPtoUSD')
  def test_getShoppingBasketWithThreeItems(self, mockConvertFromGBPtoUSD):
    itemDescriptions = ["Item A", "Item B", "Item C"]
    preConversionItemAmount = [2000, 111, 222]
    postConversionItemAmount = 55567
    
    #since the discount is applied BEFORE the conversion and we are mocking the conversion function
    #with a fixed result the discount amount will not effect the output
    
    responses = []
    responses.append(postConversionItemAmount)
    mockConvertFromGBPtoUSD.side_effect = responses

    curDateTime = appObj.getCurDateTime()
    appObj.setTestingDateTime(curDateTime)
    expectedPriceExpiryDateTime = curDateTime + PriceValidatyDuration
  
    inputPayload = copy.deepcopy(inputPayloadWithZeroItems) #dict function ensures we copy the object
    for a in range(0,3):
      inputPayload["Basket"]["Items"].append({
              'Description': itemDescriptions[a],
              'ItemPrice': {'Amount': preConversionItemAmount[a], 'CurrencyCode': 'GBP'}
      })

    expectedResult = {
      'Basket': inputPayload["Basket"],
      'Totals': {
        'DiscountPercentage': 10,
        'TotalPayable': {'Amount': postConversionItemAmount, 'CurrencyCode': 'USD'}
        },
      'PriceExpiry': expectedPriceExpiryDateTime.isoformat()
    }
    actualResult = self.testClient.post('/api/shoppingBasket/',json=inputPayload)
    self.assertEqual(actualResult.status_code, 200)
    actualResultJSON = json.loads(actualResult.get_data(as_text=True))
    self.assertJSONStringsEqual(actualResultJSON, expectedResult)

    #Finally we must also check the discount was correctly applied
    totalGBP = 0
    for a in preConversionItemAmount:
      totalGBP = totalGBP + a
    discountToApply = int(round(totalGBP * (discountPercentage / 100),0))
    self.assertEqual(mockConvertFromGBPtoUSD.call_args_list,[call(totalGBP - discountToApply)],"Wrong calls to API")


##TODO Test timelimit reached. My next task would be to create tests for error output and ensure the correct status codes are returned

