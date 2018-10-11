class IGetUserInfo:

    def __init__(self, data):
        self.users_raw = data.get('users')
        if self.users_raw:
            for user in self.users_raw:
                User(self.users_raw[user], user)


class User:

    def __init__(self, data, steamid):
        self.steamid = steamid
        self.name = data.get('name')
        self.avatar = data.get('avatar')
        self.last_online = data.get('last_online')
        self.donated = data.get('donated', 0)
        self.premium = data.get('premium', 0)
        self.premium_months_gifted = data.get('premium_months_gifted')
        self.integrations = Integrations(data.get('integrations'))
        self.bans = data.get('bans', 0)
        self.voting = Voting(data.get('voting'))
        self.inventory = data.get('inventory')
        self.trust = data.get('trust')


class Integrations:

    def __init__(self, data):
        self.group_member = data.get('group_member', 0)
        self.marketplace_seller = data.get('marketplace_seller', 0)
        self.automatic = data.get('automatic', 0)
        self.steamrep_admin = data.get('steamrep_admin', 0)


class Voting:

    def __init__(self, data):
        self.reputation = data.get('reputation')
        self.votes = data.get('votes')
        self.suggestions = data.get('suggestions')
