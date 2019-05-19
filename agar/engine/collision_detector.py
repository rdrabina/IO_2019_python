import collision
from .. import model
from ..config import Config
from itertools import combinations


class Detector(object):
    def __init__(self, command_invoker):
        self.command_invoker = command_invoker

    def detect_collisions(self, game_state):
        pass

    def detect_player_collisions(self, players):
        for (player1, player2) in list(combinations(players, 2)):
            if self.players_collide(player1, player2):
                # TODO build update
                return None

    def players_collide(self, p1, p2):
        if p1.login == p2.login:
            raise Exception("Players with same login: {0}".format(p1.login))
        distance = self.get_object_distance(p1, p2)
        p1_radius = Config.player_diameter_function(p1.weight) / 2
        p2_radius = Config.player_diameter_function(p2.weight) / 2

    def get_object_distance(self, p1, p2):
        (p1_x, p1_y) = p1.coordinates
        (p2_x, p2_y) = p2.coordinates
        distance_vector = collision.Vector(p2_x - p1_x, p2_y - p1_y)
        return distance_vector.ln()

    def check_objects_collision(self, o1, o2):
        pass
