from agar.config import Config
import agar.command as command


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
        # TODO proper double comparison
        return filter(lambda p: p.coordinates == coordinates, self.plankton)

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


class MapObject:
    def __init__(self, x=0, y=0):
        self.coordinates = (x, y)
        self.weight = Config.PLANKTON_WEIGHT

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
