class Heartbeat:

    def __init__(self, data):
        self.bumped = data.get('bumped')
        self.message = data.get('message')


class GetAccessToken:

    def __init__(self, data):
        self.token = data.get('token')
        self.message = data.get('message')
