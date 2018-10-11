class IGetPrices:

    def __init__(self, data):
        self.success = data.get('success')
        self.message = data.get('message', '')
        self.current_time = data.get('current_time')
        self.raw_usd_value = data.get('raw_usd_value')
        self.usd_currency = data.get('usd_currency')
        self.usd_currency_index = data.get('usd_currency_index')
        self.items = data.get('items')
