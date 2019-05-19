import abc
from enum import Enum


class Invoker:
    """
    Ask the command to carry out the request.
    """

    def __init__(self):
        self.commands = []

    def store_command(self, command):
        self.commands.append(command)

    def execute_commands(self, game_state):
        for command in self.commands:
            command.execute(game_state)

    def clear_commands(self):
        self.commands.clear()

    def get_commands(self):
        return self.commands


class Command(metaclass=abc.ABCMeta):
    """
    Declare an interface for executing an operation.
    """

    def __init__(self, command_type):
        self.command_type = command_type

    @abc.abstractmethod
    def execute(self, game_state):
        pass


class AddPlankton(Command):
    def __init__(self, plankton):
        super().__init__("AddPlankton")
        self.plankton = plankton

    def execute(self, game_state):
        game_state.add_plankton(self.plankton)


class AddPowerup(Command):
    def __init__(self, powerup):
        super().__init__("AddPowerup")
        self.powerup = powerup

    def execute(self, game_state):
        game_state.add_powerup(self.powerup)
