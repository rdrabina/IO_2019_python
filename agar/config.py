from math import log
from math import sqrt


class Config:
    PLAYER_STARTING_WEIGHT = 3
    PLANKTON_WEIGHT = 1
    MAP_WIDTH = 4000
    MAP_HEIGHT = 3000
    COORDS_MIN_DIFFERENCE = 0.1

    @staticmethod
    def velocity_function(weight):
        return 10 - log(weight)

    @staticmethod
    def player_diameter_function(weight):
        return sqrt(weight) + 20

    @staticmethod
    def plankton_diameter_function(weight):
        return 4 * sqrt(weight) + 5

    @staticmethod
    def powerup_diameter_function(weight):
        return sqrt(weight) + 20
