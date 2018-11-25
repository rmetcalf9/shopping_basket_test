'''
Business logic for shopping basket
'''
from dateutil.relativedelta import relativedelta

PriceValidatyDuration = relativedelta(minutes=30)
InvalidRecievedCurrencyException = Exception("Invalid recieved currenct - can only use GBP")

discountPercentage = 10 #candidate for external paramater


def caculateBasket(appObj, recievedBasketJSON):
   curDatetime = appObj.getCurDateTime()
   
   totalPayableInUSD = 0
   
   basketItems = []
   for item in recievedBasketJSON["Basket"]["Items"]:
     if item["ItemPrice"]["CurrencyCode"] != "GBP":
       raise InvalidRecievedCurrencyException
     convertedAmount = appObj.currencyConverter.convertFromGBPtoUSD(item["ItemPrice"]["Amount"])
     discountToApply = int(round(convertedAmount * (discountPercentage / 100),0))
     totalPayableInUSD = (totalPayableInUSD + convertedAmount) - discountToApply
     basketItems.append(item)
   
   return { 
    'Basket': {
      'Items': basketItems
    },
    'PriceExpiry': curDatetime + PriceValidatyDuration,
    'Totals': {
      'DiscountPercentage': discountPercentage,
      'TotalPayable': {
        'Amount': totalPayableInUSD,
        'CurrencyCode': "USD"
      }
    }
   }, 200
