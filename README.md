# BackpackTF
BackpackTF Api wrapper

Note: Some api's require elevated access to api key, you have to request it on the api key page, 
      it should take 24-48 hours to get elevated access.



#####TODO:
1. Add web cookies methods
2. Add regular web methods

Pretty much just made this for myself but anyone can download this lib.
I'd like to receive all feedback from you since I'am still learning how to do this.
I'd be glad if someone could help me with Steam openID login to backpack.tf.

##### Example: 
```python
from BackpackTF.API import API
import asyncio

api = API(key='your api key, https://backpack.tf/developer/apikey/view')


@api.on('Token')
async def token_set(successful, message):
    if successful:
        print('Token received from backpack.tf')
    else:
        print(f'Token was not received from backpack.tf, message: {message.message}')


@api.on('Heartbeat')
async def heartbeat_response(successful, message):
    if successful:
        print(f'Heartbeat sent to backpack.tf, bumped {message.bumped}')
    else:
        print(f'Heartbeat was not sent to backpack.tf, message: {message.message}')


loop = asyncio.get_event_loop()
loop.run_until_complete(api.heartbeat())

```
Returns:
successful - if request was successful or not
response object - includes message if request wasnt successful, check Objects folder for all objects

All available events: 
"Token", "Heartbeat", "ListingsCreated", "ListingsDeleted", "MyListings", "IGetPrices", "IGetCurrencies", "IGetUserInfo", "IGetPriceHistory", "ClassifiedsSearch", "IGetSpecialItems"