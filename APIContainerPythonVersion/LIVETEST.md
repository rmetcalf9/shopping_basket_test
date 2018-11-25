# Livetest

I have deployed this container onto my peronal webserver which runs docker. (See my blogpost of how this is setup - https://code.metcarob.com/node/217)
This uses kong as an API gateway and I have configured this basic auth.
I have provided users with a username and password seperatly.

To do a live test:
visit: https://api.metcarob.com/shopping/apidocs/
enter username and password

You can run shopping basket post with the following example payload:
```
{
  "Basket": {
    "Items": [
      {
        "Description": "Some Item Description 1",
        "ItemPrice": {
          "Amount": 123,
          "CurrencyCode": "GBP"
        }
      },
      {
        "Description": "Some Item Description 2",
        "ItemPrice": {
          "Amount": 2400,
          "CurrencyCode": "GBP"
        }
      },
      {
        "Description": "Some Item Description 3",
        "ItemPrice": {
          "Amount": 1220,
          "CurrencyCode": "GBP"
        }
      }
    ]
  }
}
```

You should see a response. (The total is based on a live curracy conversion.

