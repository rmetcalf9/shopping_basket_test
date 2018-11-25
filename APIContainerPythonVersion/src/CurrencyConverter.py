import requests
import json
from dateutil.relativedelta import relativedelta

'''
This file contains CurrencyConverter code including the CurrencyConverter class which:
 - Provides function to convert currency from GBP to USD
 - Queries webservice to find currency conversion rate (fixer.io)
 - Caches conversion rate for a set period of time
'''

MissingGBPRateException = Exception("Webservice response dosen't have a USD to GBP rate")
BadServiceResponse = Exception("Currency response was not a success code")

'''
Helper class to call fixerIO webservice. This function can be patched during testing to allow me to mock the fixerIO response
It is more flexible to patch this function rather than patching request.get function since I have more graunlar control over
individual responses
'''
def getLatestRatesFromFixerIO(apikey):
  result = requests.get("http://data.fixer.io/api/latest?access_key=" + apikey)
  if result.status_code!=200:
    print(result)
    raise BadServiceResponse
  return json.loads(result.text)

'''
Main class
 - This is dependent on the global application object which is passed in on construction - dependancy required to allow cache expiry testing
'''
class CurrencyConverter:
  GBPtoUSDConversionMultiplier = None
  APIKEY = None
  appObj = None
  rateRefreshInterval = relativedelta(minutes=10) #This is a candidate to become a configuratoin paramater
  rateLoadedTime = None
  
  def __init__(self, appObj, APIKEY):
    self.APIKEY = APIKEY
    self.appObj = appObj
    
  def isLoadRequired(self):
    if self.GBPtoUSDConversionMultiplier is None:
      return True
    if (self.appObj.getCurDateTime() > (self.rateLoadedTime + self.rateRefreshInterval)):
      return True
    return False
  
  def loadRate(self):
    self.rateLoadedTime = self.appObj.getCurDateTime() #Must use appObj to get time to ensure we get proper state for test cases
    webresponseJSON = getLatestRatesFromFixerIO(self.APIKEY)["rates"]
    for rate in webresponseJSON:
      if rate=="GBP":
        self.GBPtoUSDConversionMultiplier=1/(webresponseJSON[rate])
        return
    raise MissingGBPRateException
  
  def convertFromGBPtoUSD(self, amount):
    if self.isLoadRequired():
      self.loadRate()
    return amount * self.GBPtoUSDConversionMultiplier
