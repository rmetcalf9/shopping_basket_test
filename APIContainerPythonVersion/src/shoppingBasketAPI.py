from flask import request
from flask_restplus import Resource, fields
import datetime
import pytz
from baseapp_for_restapi_backend_with_swagger import readFromEnviroment
from shoppingBasket import caculateBasket

'''
This file contains the shopping basket API code.
'''


'''
This generates the API Model. This is used by Flask_Rest_plus to geneate the swagger file and marshal response payloads
this is where the data structure used in the API is described
'''
def getAPIModel(appObj):
  itemModel = appObj.flastRestPlusAPIObject.model('Item', {
    'Version': fields.String(default='DEFAULT', description='Version of container running on server')
  })
  basketModel = appObj.flastRestPlusAPIObject.model('Basket', {
    'Items': fields.List(fields.Nested(itemModel))
  })
  currencyAmountModel = appObj.flastRestPlusAPIObject.model('Currency Amount', {
    'Amount': fields.Integer(default='0',description='Integer amount value (e.g. in GBP this will be pence, for USD it\'s cents)'),
    'CurrencyCode': fields.String(default='GBP', description='Currecny code')
  })
  totalModel = appObj.flastRestPlusAPIObject.model('Totals', {
    'DiscountPercentage': fields.Integer(default='0',description='Discount percentage that has been applied to the basket'),
    'TotalPayable': fields.Nested(currencyAmountModel)
  })
  return appObj.flastRestPlusAPIObject.model('Shopping Basket Result', {
    'Basket': fields.Nested(basketModel),
    'PriceExpiry': fields.DateTime(dt_format=u'iso8601', description='Current server date time'),
    'Totals': fields.Nested(totalModel)
  })  


'''
Function called by appObj in order to register the API
'''
def registerAPI(appObj):
  nsShoppingBasket = appObj.flastRestPlusAPIObject.namespace('shoppingBasket', description='Shopping basket cost caculator')
  @nsShoppingBasket.route('/')
  class servceInfo(Resource):
    '''General Server Operations XXXXX'''
    @nsShoppingBasket.doc('getserverinfo')
    @nsShoppingBasket.marshal_with(getAPIModel(appObj))
    @nsShoppingBasket.response(200, 'Success')
    def post(self):
     '''Get general information about the dockjob server'''
     return caculateBasket(appObj, request.get_json())
