'''
Business logic for shopping basket
'''
from dateutil.relativedelta import relativedelta

PriceValidatyDuration = relativedelta(minutes=30)


def caculateBasket(appObj, recievedBasketJSON):
   #appObj.currencyConverter.convertFromGBPtoUSD(123)
   curDatetime = appObj.getCurDateTime()
   return { 
    'Basket': {
      'Items': []
    },
    'PriceExpiry': curDatetime + PriceValidatyDuration,
    'Totals': {
      'DiscountPercentage': 10,
      'TotalPayable': {
        'Amount': 0,
        'CurrencyCode': "USD"
      }
    }
   }, 200
