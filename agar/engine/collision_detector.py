from .. import model
from ..config import Config
from itertools import combinations
import agar.command as command
import copy


class Detector(object):
    def __init__(self):
        pass

    def detect_collisions(self, game_state):
        commands = []
        commands += self.detect_player_collisions(game_state.players)
        commands += self.detect_plankton_collisions(game_state.players, game_state.plankton)
        commands += self.detect_powerup_collisions(game_state.players, game_state.powerups)
        return commands

    def detect_player_collisions(self, players):
        commands = []
        for (player1, player2) in list(combinations(players, 2)):
            (player_to_eat, player_to_grow) = self.players_collide(player1, player2)
            if player_to_eat is not None:
                player_to_grow_copy = copy.deepcopy(player_to_grow)
                player_to_grow_copy.eat(player_to_eat)
                remove_player_command = command.RemovePlayer(player_to_eat)
                update_player_command = command.UpdatePlayer(player_to_grow_copy)
                commands.append(remove_player_command)
                commands.append(update_player_command)
        return commands

    def players_collide(self, p1, p2):
        if p1.login == p2.login:
            raise Exception("Players with same login: {0}".format(p1.login))
        r1 = Config.player_diameter_function(p1.weight) / 2
        r2 = Config.player_diameter_function(p2.weight) / 2
        return self.check_objects_collision(p1, r1, p2, r2)

    def detect_plankton_collisions(self, players, plankton):
        commands = []
        for player in players.values():
            player_radius = Config.player_diameter_function(player.weight) / 2
            for p in plankton:
                p_radius = Config.plankton_diameter_function(p.weight)
                (food, player_checked) = self.check_objects_collision(player, player_radius, p, p_radius)
                if food is not None:
                    print("COLLISION HURRAY with food" + food)
                    player_copy = copy.deepcopy(player)
                    player_copy.eat(food)
                    remove_plankton_command = command.RemovePlankton(food)
                    update_player_command = command.UpdatePlayer(player_copy)
                    commands.append(remove_plankton_command)
                    commands.append(update_player_command)
                if player_checked is not None:
                    player = player_checked
        return commands

    def detect_powerup_collisions(self, players, powerups):
        commands = []
        for player in players.values():
            player_radius = Config.player_diameter_function(player.weight) / 2
            for p in powerups:
                p_radius = Config.powerup_diameter_function()
                (powerup, player_checked) = self.check_objects_collision(player, player_radius, p, p_radius)
                if powerup is not None:
                    player_copy = copy.deepcopy(player)
                    player_copy.eat(powerup)
                    remove_powerup_command = command.RemovePowerup(powerup)
                    update_player_command = command.UpdatePlayer(player_copy)
                    commands.append(remove_powerup_command)
                    commands.append(update_player_command)
                if player_checked is not None:
                    player = player_checked
        return commands

    # return (winner, loser) of collision or else (None, None) (if there is no collision)
    def check_objects_collision(self, o1, r1, o2, r2):
        distance = model.MapObject.get_objects_distance(o1, o2)
        if r1 >= distance or r2 >= distance:
            if r1 > r2:
                return o1, o2
            else:
                return o2, o1
        return None, None
