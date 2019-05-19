import abc
import json
from threading import Lock


class Invoker:
    """
    Ask the command to carry out the request.
    """

    def __init__(self):
        self.commands = []
        self.command_types = ["addPlankton", "removePlankton", "addPlayer", "updatePlayer", "removePlayer"]
        self.lock = Lock()

    def store_command(self, command):
        self.lock.acquire()
        self.commands.append(command)
        self.lock.release()

    def store_commands(self, commands):
        self.lock.acquire()
        self.commands += commands
        self.lock.release()

    def execute_commands(self, game_state):
        self.lock.acquire()
        for command in self.commands:
            command.execute(game_state)
        self.lock.release()

    def clear_commands(self):
        self.lock.acquire()
        self.commands.clear()
        self.lock.release()

    def to_json(self):
        self.lock.acquire()
        obj_dict = {}
        for command_type in self.command_types:
            commands_with_type = self.get_commands_with_type(command_type)
            commands_json_list = []
            for command in commands_with_type:
                commands_json_list.append(command.to_json())
            obj_dict[command_type] = commands_json_list
        self.lock.release()
        return json.dumps(str(obj_dict))

    def get_commands_with_type(self, command_type):
        return filter(lambda c: c.command_type == command_type, self.commands)


class Command(metaclass=abc.ABCMeta):
    """
    Declare an interface for executing an operation.
    """

    def __init__(self, command_type):
        self.command_type = command_type

    @abc.abstractmethod
    def execute(self, game_state):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass


class AddPlankton(Command):
    def __init__(self, plankton):
        super().__init__("addPlankton")
        self.plankton = plankton

    def execute(self, game_state):
        game_state.add_plankton(self.plankton)

    def to_json(self):
        return self.plankton.to_dict()


class RemovePlankton(Command):
    def __init__(self, plankton):
        super().__init__("removePlankton")
        self.plankton = plankton

    def execute(self, game_state):
        game_state.delete_plankton(self.plankton.coordinates)

    def to_json(self):
        return self.plankton.to_dict()


class AddPlayer(Command):
    def __init__(self, player):
        super().__init__("addPlayer")
        self.player = player

    def execute(self, game_state):
        game_state.add_player(self.player)

    def to_json(self):
        return self.player.to_full_dict()


class UpdatePlayer(Command):
    def __init__(self, player):
        super().__init__("updatePlayer")
        self.player = player

    def execute(self, game_state):
        game_state.update_player(self.player)

    def to_json(self):
        return self.player.to_dict()


class RemovePlayer(Command):
    def __init__(self, player):
        super().__init__("removePlayer")
        self.player = player

    def execute(self, game_state):
        game_state.delete_player(self.player.login)

    def to_json(self):
        return self.player.to_dict()
