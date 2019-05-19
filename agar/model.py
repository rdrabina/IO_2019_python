from agar.config import Config


class GameState(object):
    def __init__(self):
        self.players = {}
        self.plankton = []

    def get_player(self, login):
        return self.players.get(login, None)

    def add_player(self, player):
        login = player.login
        if self.get_player(login) is not None:
            raise Exception("Player already exists: {0}".format(login))
        self.players[login] = player

    def get_plankton(self, coordinates):
        return filter(lambda p: p.coordinates == coordinates, self.plankton)

    def add_plankton(self, plankton):
        self.plankton.append(plankton)


class MapObject:
    def __init__(self, x=0, y=0):
        self.coordinates = (x, y)
        self.weight = Config.PLANKTON_WEIGHT


class Player(MapObject):
    def __init__(self, login, department, image=None):
        # TODO randomly spawn of new player
        super(Player, self).__init__(5, 5)
        self.login = login
        self.department = department
        self.image = image
        self.weight = Config.PLAYER_STARTING_WEIGHT
        self.velocity = 0
        self.direction = (0, 0)

    def calculate_velocity(self):
        self.velocity = Config.velocity_function(self.weight)
        return self.velocity


class Plankton(MapObject):
    def __init__(self, x, y):
        super(Plankton, self).__init__(x, y)
