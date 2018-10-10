class IGetCurrencies:

    def __init__(self, data):
        self.success = data.get('success')
        self.message = data.get('message', '')
        self.currencies_raw = data.get('currencies', {})
        self.earbuds = Currency(self.currencies_raw.get('earbuds', {}))
        self.keys = Currency(self.currencies_raw.get('keys', {}))
        self.metal = Currency(self.currencies_raw.get('metal', {}))
        self.hat = Currency(self.currencies_raw.get('hat', {}))


class Currency:

    def __init__(self, data):
        self.name = data.get('name')
        self.quality = data.get('quality')
        self.priceindex = data.get('priceindex')
        self.single = data.get('single')
        self.round = data.get('round')
        self.craftable = data.get('craftable')
        self.defindex = data.get('defindex')
        self.active = data.get('active')
        self.price_raw = data.get('price')
        self.value = self.price_raw.get('value')
