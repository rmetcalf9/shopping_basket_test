#appObj.py - This file contains the main application object
# an instance of this is created in app.py
# this class inherits from AppObjBaseClass which provides utility features that make the application run nicely in a container

import pytz

from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass as parAppObj, readFromEnviroment
from flask_restplus import fields
import time
import datetime
from shoppingBasketAPI import registerAPI as registerShoppingBasketAPI
from CurrencyConverter import CurrencyConverter

class appObjClass(parAppObj):
  curDateTimeOverrideForTesting = None
  serverStartTime = None
  version = None
  currencyConverter = None

  def init(self, env, serverStartTime, testingMode = False):
    self.curDateTimeOverrideForTesting = None
    self.serverStartTime = serverStartTime
    self.version = readFromEnviroment(env, 'APIAPP_VERSION', None, None)
    apikey = readFromEnviroment(env, 'APIAPP_FIXERIO_APIKEY', None, None)
    self.currencyConverter = CurrencyConverter(self, apikey)
    super(appObjClass, self).init(env)

  def initOnce(self):
    super(appObjClass, self).initOnce()
    registerShoppingBasketAPI(self)
    self.flastRestPlusAPIObject.title = "Shopping Cart Caculator - Prototype API"
    self.flastRestPlusAPIObject.description = "API created as part of technical test - Please ignore the default namespace"
    

  def setTestingDateTime(self, val):
    self.curDateTimeOverrideForTesting = val
  def getCurDateTime(self):
    if self.curDateTimeOverrideForTesting is None:
      return datetime.datetime.now(pytz.timezone("UTC"))
    return self.curDateTimeOverrideForTesting


appObj = appObjClass()
