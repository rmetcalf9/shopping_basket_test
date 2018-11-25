'''
Business logic for shopping basket
'''
from dateutil.relativedelta import relativedelta

PriceValidatyDuration = relativedelta(minutes=30)
InvalidRecievedCurrencyException = Exception("Invalid recieved currenct - can only use GBP")

discountPercentage = 10 #candidate for external paramater


def caculateBasket(appObj, recievedBasketJSON):
   curDatetime = appObj.getCurDateTime()
   
   #Cacualte total in GBP then convert once
   #Discount must be applyed before conversion
   totalPayableInGBP = 0
   totalPayableInUSD = 0
   
   basketItems = []
   for item in recievedBasketJSON["Basket"]["Items"]:
     if item["ItemPrice"]["CurrencyCode"] != "GBP":
       raise InvalidRecievedCurrencyException
     totalPayableInGBP = totalPayableInGBP + item["ItemPrice"]["Amount"]
     basketItems.append(item)
    
   if totalPayableInGBP != 0:
     discountAmount = int(round(totalPayableInGBP * (discountPercentage / 100),0))
     amountToConvert = totalPayableInGBP - discountAmount
     convertedAmount = appObj.currencyConverter.convertFromGBPtoUSD(amountToConvert)
     totalPayableInUSD = convertedAmount

   
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
