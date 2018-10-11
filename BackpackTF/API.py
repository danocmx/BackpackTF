import aiohttp
from pyee import EventEmitter
import json
import asyncio
from time import time

from Objects.IGetSpecialItems import IGetSpecialItems
from Objects.Listings import ClassifiedsSearch, MyListings
from Objects.IGetPrices import IGetPrices
from Objects.IGetPriceHistory import IGetPriceHistory
from Objects.IGetCurrencies import IGetCurrencies
from Objects.IGetUserInfo import IGetUserInfo


def token_check(func):
    async def wrapper(*args, **kwargs):
        self = args[0]
        if not self.token:
            if not self.key:
                raise ValueError('No api key set.')
            else:
                await self.get_access_token()

        return await func(*args, **kwargs)

    return wrapper


def key_check(func):
    async def wrapper(*args, **kwargs):
        self = args[0]
        if not self.key:
            raise ValueError('No api key set')

        return await func(*args, **kwargs)

    return wrapper


class API(EventEmitter):

    def __init__(self, token='', key='', to_json: bool=True, rate_limit: bool=True,
                 session: aiohttp.ClientSession=aiohttp.ClientSession()):
        self.token = token
        self.key = key

        self.session = session
        self.request_ = self.async_request

        self.to_json = to_json

        self.rate_limit = rate_limit
        self.requests_count = 0
        self.last_request = 0

        EventEmitter.__init__(self)

    async def async_request(self, method, api, **kwargs):
        """
        Request function, if self.rate_limit is True, limits the number of requests per minute to not get banned
        :param method: GET, POST, or DELETE
        :param api: all the apis can be found here https://backpack.tf/developer
        :param kwargs: options: params or json
        :return bool, response_text: True if request was successful, response_text from the server
        """

        if self.rate_limit:
            req_time = time() - self.last_request
            if req_time > 60:
                self.requests_count = 0
            if self.requests_count >= 50 and req_time < 60:
                self.emit('RateLimit', self.requests_count, req_time)
                asyncio.sleep(60 - req_time)
                self.requests_count = 0

        url = 'https://backpack.tf/api/' + api
        async with self.session.request(method.upper(), url, **kwargs) as response:

            self.last_request = time()

            response_text = await response.text()

            try:
                response_text = json.loads(response_text)
            except json.JSONDecodeError:
                pass

            if 300 > response.status > 199:
                return True, response_text

            return False, response_text

    @key_check
    async def get_access_token(self):
        """
        Set's self.token to the your current backpack.tf token
        :return response: more in self.request_
        """

        response = await self.request_('GET', 'aux/token/v1', params={'key': self.key})

        successful, message = response
        self.emit('Token', successful, message)
        if successful:
            self.token = message.get('token')

        return response

    @token_check
    async def heartbeat(self, automatic: str='all'):
        """
        Sends heartbeat to backpack.tf
        :param automatic: 'all' to bump all listings, 'sell' for sell listings only
        :return response: more in self.request_
        """

        response = await self.request_('POST', 'aux/heartbeat/v1', params={'token': self.token, 'automatic': automatic})

        successful, message = response
        self.emit('Heartbeat', successful, message)

        return response

    @token_check
    async def create_listings(self, listings: list):
        """
        Creates listing(s) on backpack.tf"s classifieds
        :param listings: form - https://backpack.tf/api/docs/create_listings
        :return response: more in self.request_
        """

        response = await self.request_('POST', 'classifieds/list/v1', json={'token': self.token, 'listings': listings},
                                       json_=True)

        successful, message = response
        self.emit('ListingsCreated', successful, message)

        return response

    @token_check
    async def delete_listings(self, listings):
        """
        Deletes listing(s) on backpack.tf"s classifieds
        :param listings: list of listing ids you want to delete, form buy: 'game-id_your-steamid_listing-id',
                                                                      sell: 'game-id_listing-id'
        :return response: more in self.request_
        """

        response = await self.request_('DELETE', 'classifieds/delete/v1', json={'token': self.token,
                                                                                'listing_ids': listings}, json_=True)

        successful, message = response
        self.emit('ListingsDeleted', successful, message)

        return response

    @token_check
    async def my_listings(self, item_names=1, intent='dual', inactive=0):
        """
        Gets your current listings from backpack.tf
        :param item_names: adds 'name' property to item
        :param intent: 'sell', 'buy' or 'dual'
        :param inactive: if 1, shows hidden listings you have
        :return successful, message: more in self.request_
        """

        response = await self.request_('GET', 'classifieds/listings/v1', params={'item_names': item_names,
                                                                                 'intent': intent, 'inactive': inactive,
                                                                                 'token': self.token})
        successful = response[0]
        message = MyListings(response[1])
        self.emit('MyListings', successful, message)

        return successful, message

    @key_check
    async def i_get_prices(self, raw=1, since=1):
        """
        Get"s all prices from backpack.tf
        :param raw: found here https://backpack.tf/api/docs/IGetPrices
        :param since: if you want to get prices updated after this time
        :return successful, message: more in self.request_
        """

        params = {'format': 'json', 'raw': raw, ' since': since, 'key': self.key}

        response = await self.request_('GET', 'IGetPrices/v4', params=params)

        successful = response[0]
        message = IGetPrices(response[1].get('response'))
        self.emit('IGetPrices', successful, message)

        return successful, message

    @key_check
    async def i_get_currencies(self, raw=1):
        """
        Value of currencies from backpack.tf
        :param raw: found here https://backpack.tf/api/docs/IGetCurrencies
        :return successful, message: more in self.request_
        """

        params = {'format': 'json', 'raw': raw, 'key': self.key}

        response = await self.request_('GET', 'IGetCurrencies/v1', params=params)

        successful = response[0]
        message = IGetCurrencies(response[1])
        self.emit('IGetCurrencies', successful, message)

        return successful, message

    @key_check
    async def i_get_user_info(self, steamids):
        """
        Gets user info from backpack.tf
        :param steamids: array of steamids if more than 1 steamid, if only 1 steamid can be str
        :return successful, message: more in self.request_
        """

        response = await self.request_('GET', 'users/info/v1', params={'key': self.key, 'steamids': steamids})

        successful = response[0]
        message = IGetUserInfo(response[1])
        self.emit('IGetUserInfo', successful, message)

        return successful, message

    @key_check
    async def i_get_price_history(self, item, quality, tradable=1, craftable=1, priceindex=0):
        """
        Get's price history of an item
        :param item: name of the item you want to find
        :param quality: name or a definition index
        :param tradable: 1 if tradable, 0 if non-tradable
        :param craftable: 1 if craftable, 0 if non-craftable
        :param priceindex:
        :return successful, message: more in self.request_
        """

        params = {'item': item, 'quality': quality, 'tradable': tradable, 'craftable': craftable,
                  'priceindex': priceindex, 'format': 'json', 'key': self.key}

        response = await self.request_('GET', 'IGetPriceHistory/v1', params=params)

        successful = response[0]
        message = IGetPriceHistory(response[1].get('response', {}))
        self.emit('IGetPriceHistory', successful, message)

        return successful, message

    @key_check
    async def classifieds_search(self, item, quality=0, particle=0, craftable=1, australium=0, wear_tier=0,
                                 texture_name='', paint=0, killstreak=0, item_names=1, steamid='', intent='dual',
                                 page_size=10, fold=0):
        """
        Searches classifieds on backpack.tf
        :param item: name of the item you want to search for, can include quality, killstreak, australium stats, str
        :param quality: quality of the item, is not necessery if quality is in item parameter, str or int
        :param particle: necessery if you want to search for unusuals, int
        :param craftable: if item is craftable or not, int
        :param australium: australium 1 if not 0
        :param wear_tier: if item is an war paint or weapon skin
        :param texture_name: name of the texture we want
        :param paint: search for paint only
        :param killstreak: if item has a killstreak or not
        :param item_names: if set, adds name parameter to searched listings
        :param steamid: listings of steamid set
        :param intent: 'sell', 'buy' or 'dual'
        :param page_size: min 1, max 30
        :param fold: if 1 listings are folded, if 0 can show multiple same listings from 1 person
        :return successful, message: more in self.request_
        """

        params = {'item': item, 'craftable': craftable, 'killstreak_tier': killstreak, 'australium': australium,
                  'item_names': item_names, 'intent': intent, 'page_size': page_size, 'fold': fold, 'key': self.key}

        if quality:
            params['quality'] = quality
        if particle:
            params['particle'] = particle
        if steamid:
            params['steamid'] = steamid
        if wear_tier:
            params['wear_tier'] = wear_tier
        if texture_name:
            params['texture_name'] = texture_name
        if paint:
            params['paint'] = paint

        response = await self.request_("GET", 'classifieds/search/v1', params=params)

        successful = response[0]
        message = ClassifiedsSearch(response[1])
        self.emit('ClassifiedsSearch', successful, message)

        return successful, message

    @key_check
    async def i_get_special_items(self, appid=440):
        """
        Gets all special Items
        :param appid: game id of the game you want to get SpecialItems from, viable options 440, 570 or 730
        :return successful, message: more in self.request_
        """

        params = {'format': 'json', 'appid': appid, 'key': self.key}

        response = await self.request_("GET", 'IGetSpecialItems/v1', params=params)

        successful = response[0]
        message = IGetSpecialItems(response[1])
        self.emit('IGetSpecialItems ', successful, message)

        return successful, message
