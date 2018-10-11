class CreateListings:

    def __init__(self, data):
        self.message = data.get('message')
        self.listings = data.get('listings')


class DeleteListings:

    def __init__(self, data):
        self.deleted_listings = data.get('blah')


class MyListings:

    def __init__(self, data):
        self.message = data.get('message', '')
        self.cap = data.get('cap')
        self.promotes_remaining = data.get('promotes_remaining')
        self.listings_raw = data.get('listings')
        self.listings = []
        if self.listings_raw:
            for listing in self.listings_raw:
                self.listings.append(Listings(listing))


class Listings:

    def __init__(self, data):
        self.id = data.get('id')
        self.item = data.get('item')
        self.appid = data.get('appid')
        self.currencies = {'keys': data.get('currencies').get('keys', 0),
                           'metal': data.get('currencies').get('metal', 0)}
        self.buyout = data.get('buyout', 0)
        self.offers = data.get('offers', 0)
        self.details = data.get('details')
        self.created = data.get('created')
        self.bump = data.get('bump')
        self.intent = data.get('intent')
        self.automatic = data.get('automatic', 0)
        self.count = data.get('count', 0)


class ClassifiedsSearch:

    def __init__(self, data):
        self.message = data.get('message')
        self.total = data.get('total')
        self.skip = data.get('skip')
        self.page_size = data.get('page_size')
        self.buy = Intent(data.get('buy'))
        self.sell = Intent(data.get('sell'))


class Intent:

    def __init__(self, data):
        self.total = data.get('total')
        self.listings_raw = data.get('listings')
        self.listings = []
        if self.listings_raw:
            for listing in self.listings_raw:
                self.listings.append(Listings(listing))
