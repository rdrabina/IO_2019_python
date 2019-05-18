from math import log


class Config:
    PLAYER_STARTING_WEIGHT = 3
    PLANKTON_WEIGHT = 1

    @staticmethod
    def velocity_function(weight):
        return 10 - log(weight)
