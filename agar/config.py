from math import log


class Config:
    PLAYER_STARTING_WEIGHT = 3
    PLANKTON_WEIGHT = 1
    MAP_WIDTH = 4000
    MAP_HEIGHT = 3000

    @staticmethod
    def velocityFunction(weight):
        return 10 - log(weight)
