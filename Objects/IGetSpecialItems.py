class IGetSpecialItems:

    def __init__(self, data):
        self.success = data.get('success')
        self.message = data.get('message')
        self.current_time = data.get('current_time')
        self.items = []
        if data.get('items'):
            for item in data.get('item'):
                self.items.append(SpecialItem(item))


class SpecialItem:

    def __init__(self, data):
        self.name = data.get("name")
        self.item_name = data.get('item_name')
        self.defindex = data.get('defindex')
        self.item_class = data.get('item_class')
        self.item_type_name = data.get('item_type_name')
        self.item_description = data.get('item_description')
        self.item_quality = data.get('item_quality')
        self.min_ilevel = data.get('min_ilevel')
        self.max_ilevel = data.get('max_ilevel')
        self.image_url = data.get('image_url')
        self.image_url_large = data.get('image_url_large')
        self.appid = data.get('appid')
