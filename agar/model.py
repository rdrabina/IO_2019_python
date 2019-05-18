from collision import Vector


class GameState(object):
    def __init__(self):
        players = []
        plankton = []


class MapObject:
    def __init__(self, x=0, y=0):
        coordinates = (x, y)


class Player(MapObject):
    def __init__(self, login, department, image=None):
        super(Player, self).__init__(5, 5)
        self.login = login
        self.department = department
        self.image = image
        self.velocity = 0
        self.direction = Vector(0, 0)
