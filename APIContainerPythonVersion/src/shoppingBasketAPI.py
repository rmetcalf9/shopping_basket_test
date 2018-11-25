from flask_restplus import Resource, fields
import datetime
import pytz
from baseapp_for_restapi_backend_with_swagger import readFromEnviroment

'''
This file contains the shopping basket API code.
'''


'''
This generates the API Model. This is used by Flask_Rest_plus to geneate the swagger file and marshal response payloads
'''
def getAPIModel(appObj):
  serverInfoServerModel = appObj.flastRestPlusAPIObject.model('mainAPI', {
    'Version': fields.String(default='DEFAULT', description='Version of container running on server')
  })
  return appObj.flastRestPlusAPIObject.model('ServerInfo', {
    'aaa': fields.Raw(),
    'Server': fields.Nested(serverInfoServerModel)
  })  


'''
Function called by appObj in order to register the API
'''
def registerAPI(appObj):
  nsShoppingBasket = appObj.flastRestPlusAPIObject.namespace('shoppingBasket', description='Shopping basket cost caculation')
  @nsShoppingBasket.route('/')
  class servceInfo(Resource):
    '''General Server Operations XXXXX'''
    @nsShoppingBasket.doc('getserverinfo')
    @nsShoppingBasket.marshal_with(getAPIModel(appObj))
    @nsShoppingBasket.response(200, 'Success')
    def post(self):
     '''Get general information about the dockjob server'''
     curDatetime = datetime.datetime.now(pytz.utc)
     return { 
      'aaa': appObj.currencyConverter.convertFromGBPtoUSD(123)
     }, 200
