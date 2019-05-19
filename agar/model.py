from agar.config import Config
import agar.command as command
import collision


class GameState(object):
    def __init__(self):
        self.players = {}
        self.plankton = []
        self.powerUps = []

    def get_player(self, login):
        return self.players.get(login, None)

    def add_player(self, player):
        login = player.login
        if self.get_player(login) is not None:
            raise Exception("Player already exists: {0}".format(login))
        self.players[login] = player

    def update_player(self, player):
        player_to_update = self.get_player(player.login)
        if player_to_update is None:
            print("Warning: player to update not found: {0}".format(player.login))
            return
        player_to_update.coordinates = player.coordinates
        player_to_update.weight = player.weight
        player_to_update.velocity = player.velocity
        player_to_update.direction = player.direction
        return

    def delete_player(self, login):
        player_to_remove = self.get_player(login)
        if player_to_remove is None:
            print("Warning: player to delete not found: {0}".format(login))
            return
        self.players.pop(login)

    def get_plankton(self, coordinates):
        return filter(lambda p: GameState.is_very_close(p.coordinates, coordinates), self.plankton)

    def add_plankton(self, plankton):
        self.plankton.append(plankton)

    def delete_plankton(self, coordinates):
        for p in self.get_plankton(coordinates):
            self.plankton.remove(p)

    def get_commands_creating_current_state(self):
        commands = []
        for p in self.plankton:
            commands.append(command.AddPlankton(p))
        for player in self.players.values():
            commands.append(command.AddPlayer(player))
        return commands

    def add_powerup(self, powerup):
        self.powerUps.append(powerup)

    def get_powerup(self, coordinates):
        return filter(lambda p: GameState.is_very_close(p.coordinates, coordinates), self.powerUps)

    @staticmethod
    def is_very_close(c1, c2):
        return MapObject.get_coords_distance(c1, c2) < Config.COORDS_MIN_DIFFERENCE


class MapObject:
    def __init__(self, x=0, y=0):
        self.coordinates = (x, y)
        self.weight = Config.PLANKTON_WEIGHT

    @staticmethod
    def get_objects_distance(o1, o2):
        return MapObject.get_coords_distance(o1.coordinates, o2.coordinates)

    @staticmethod
    def get_coords_distance(c1, c2):
        (o1_x, o1_y) = c1
        (o2_x, o2_y) = c2
        distance_vector = collision.Vector(o2_x - o1_x, o2_y - o1_y)
        return distance_vector.ln()

    def to_dict(self):
        (x, y) = self.coordinates
        return {'coordinates': [x, y], 'weight': self.weight}


class Player(MapObject):
    def __init__(self, login, department, image=None):
        # TODO randomly spawn of new player
        super(Player, self).__init__(5, 5)
        self.login = login
        self.department = department
        self.image = image
        self.weight = Config.PLAYER_STARTING_WEIGHT
        self.velocity = 0
        self.direction = 0

    def calculate_velocity(self):
        self.velocity = Config.velocity_function(self.weight)
        return self.velocity

    def eat(self, obj):
        self.weight += obj.weight

    def to_dict(self):
        result = super().to_dict()
        result['login'] = self.login
        result['velocity'] = self.velocity
        result['direction'] = self.direction
        return result

    def to_full_dict(self):
        result = self.to_dict()
        result['department'] = self.department
        result['image'] = self.image
        return result


class Plankton(MapObject):
    def __init__(self, x, y):
        super(Plankton, self).__init__(x, y)

    def to_dict(self):
        return super().to_dict()


class Powerup(MapObject):
    def __init__(self, x, y):
        super(Powerup, self).__init__(x, y)

    def to_dict(self):
        return super().to_dict()
