class IGetPriceHistory:

    def __init__(self, data):
        self.success = data.get('success')
        if not self.success:
            self.message = data.get('message')
        self.history_raw = data.get('history')
        self.history = []
        if self.history_raw:
            for price in self.history_raw:
                self.history.append(History(price))


class History:

    def __init__(self, data):
        self.value = data.get('value')
        self.value_high = data.get('value_high', self.value)
        self.currency = data.get('currency')
        self.timestamp = data.get('timestamp')
