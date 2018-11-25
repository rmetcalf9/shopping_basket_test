from CurrencyConverter import CurrencyConverter
from TestHelperSuperClass import testHelperAPIClient, env
from unittest.mock import patch, call
from appObj import appObj
from dateutil.relativedelta import relativedelta

'''
Tests for CurrencyConverter class
 - Shows individual test cases
 - Shows use of unittest.mock to simulate result of service call
 - Shows setting of time to test expiring conversion rate without forcing test to wait until the rate has expired
'''

apikey='sdasgfgfdr32545435432'

#Sample responses for our mock service
getLatestRatesFromFixerIO_Response_RateOf2 = {
    "base": "USD",
    "date": "2018-02-13",
    "rates": {
       "CAD": 1.260046,
       "CHF": 0.933058,
       "EUR": 0.806942,
       "GBP": 0.500000 #this makes 1 GBP = 2 USD
    }
}
getLatestRatesFromFixerIO_Response_RateOf4 = {
    "base": "USD",
    "date": "2018-02-13",
    "rates": {
       "CAD": 1.260046,
       "CHF": 0.933058,
       "EUR": 0.806942,
       "GBP": 0.250000 #this makes 1 GBP = 4 USD
    }
}
testAmounts = { "GBP": 12340, "USD2": 24680, "USD4": 49360 }


class test_api(testHelperAPIClient):
  @patch('CurrencyConverter.getLatestRatesFromFixerIO')
  def test_singleConversion(self, mockGetLatestRatesFromFixerIO):
    #Setup mock to return a rate of 2
    mockGetLatestRatesFromFixerIO.side_effect  = [ 
      getLatestRatesFromFixerIO_Response_RateOf2,
    ]
    
    converterInstance = CurrencyConverter(appObj, apikey)
    self.assertEqual(converterInstance.convertFromGBPtoUSD(testAmounts['GBP']), testAmounts['USD2'], "Incorrect currency conversion result")
    
    #Make sure there was only one call with the correct APIKEY
    self.assertEqual(mockGetLatestRatesFromFixerIO.call_args_list,[call(apikey)],"Wrong calls to API")
    return

  @patch('CurrencyConverter.getLatestRatesFromFixerIO')
  def test_singleConversionDifferentRate(self, mockGetLatestRatesFromFixerIO):
    #Setup mock to return a rate of 4
    mockGetLatestRatesFromFixerIO.side_effect  = [ 
      getLatestRatesFromFixerIO_Response_RateOf4,
    ]
    
    converterInstance = CurrencyConverter(appObj, apikey)
    self.assertEqual(converterInstance.convertFromGBPtoUSD(testAmounts['GBP']), testAmounts['USD4'], "Incorrect currency conversion result")

    #Make sure there was only one call and it had the correct APIKEY
    self.assertEqual(mockGetLatestRatesFromFixerIO.call_args_list,[call(apikey)],"Wrong calls to API")
    return

  @patch('CurrencyConverter.getLatestRatesFromFixerIO')
  def test_conversionRateIsCachedBetweenCalls(self, mockGetLatestRatesFromFixerIO):
    numberOfCallsToMake = 4
    
    #setup mock object - setting up a number of responses even though we should only use the first one
    responses = []
    for c in range(0, numberOfCallsToMake):
      responses.append(getLatestRatesFromFixerIO_Response_RateOf4)
    mockGetLatestRatesFromFixerIO.side_effect = responses
    
    #Set a time in the appObj to initiate testing mode (Will stop any chance of expiry during the test)
    curDateTime = appObj.getCurDateTime()
    appObj.setTestingDateTime(curDateTime)
    
    #call code under test
    converterInstance = CurrencyConverter(appObj, apikey)
    for c in range(0, numberOfCallsToMake):
      self.assertEqual(converterInstance.convertFromGBPtoUSD(testAmounts['GBP']), testAmounts['USD4'], "Incorrect currency conversion result")

    #Make sure there was only one call with the correct APIKEY
    self.assertEqual(mockGetLatestRatesFromFixerIO.call_args_list,[call(apikey)],"Wrong calls to API")
    return

  @patch('CurrencyConverter.getLatestRatesFromFixerIO')
  def test_conversionRateChangesAndIsReloaded(self, mockGetLatestRatesFromFixerIO):
    #In this test we are going to make some calls, then arrange for the rate to expire and a new one to be loaded
    # we will then make some more calls and check we get expected results
    responses = []
    responses.append(getLatestRatesFromFixerIO_Response_RateOf4)
    responses.append(getLatestRatesFromFixerIO_Response_RateOf2)
    mockGetLatestRatesFromFixerIO.side_effect = responses

    #Set a time in the appObj to initiate testing mode (Will stop any chance of expiry during the test)
    curDateTime = appObj.getCurDateTime()
    appObj.setTestingDateTime(curDateTime)

    converterInstance = CurrencyConverter(appObj, apikey)

    #call the code under test a number of times before the cache expiry
    numberOfCallsToMake = 4
    for c in range(0, numberOfCallsToMake):
      self.assertEqual(converterInstance.convertFromGBPtoUSD(testAmounts['GBP']), testAmounts['USD4'], "Incorrect currency conversion result")

    #go forward 30 mintues - the rate should have changed because the cache will be invalidated
    appObj.setTestingDateTime(curDateTime + converterInstance.rateRefreshInterval + relativedelta(minutes=30))

    #call the code under test a number of times after the cache expiry (new result)
    for c in range(0, numberOfCallsToMake):
      self.assertEqual(converterInstance.convertFromGBPtoUSD(testAmounts['GBP']), testAmounts['USD2'], "Incorrect currency conversion result")

    #Make sure there were two calls to the mock, one before the cache expiry and one after
    self.assertEqual(mockGetLatestRatesFromFixerIO.call_args_list,[call(apikey),call(apikey)],"Wrong calls to API")
    return
