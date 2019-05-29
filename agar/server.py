import socket
import threading
import json
import time
import copy
from agar import model
from agar.engine.plankton_generator import PlanktonGenerator
from agar.engine.powerup_generator import PowerupGenerator
import agar.command as command
from agar.engine.collision_detector import Detector


class Server:
    def __init__(self):
        print("Server start")
        self.game_state = model.GameState()
        self.player_to_socket_map = {}
        self.plankton_generator = PlanktonGenerator()
        self.plankton_generator.start()
        self.powerup_generator = PowerupGenerator()
        self.powerup_generator.start()
        self.command_invoker = command.Invoker()
        self.collision_detector = Detector()
        bind_ip = '0.0.0.0'
        bind_port = 9998
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((bind_ip, bind_port))
        server.listen(5)
        client_handler = threading.Thread(target=self.handle_clients, args=(server,))
        client_handler.start()

    def parse_bytes_to_json(self, data):
        data_str = data.decode('utf8').replace("'", '"')
        data_json = json.loads(data_str)
        return data_json

    def handle_client_connection(self, client_socket, add):
        player_name = None
        while True:
            request = client_socket.recv(1024).strip()
            # print("{0} wrote: {1}".format(add, request))
            if request is not None:
                try:
                    out = self.parse_bytes_to_json(request)
                except json.JSONDecodeError:
                    pass
                    # TODO only happens when client disconnects
                if "login" in out.keys():
                    player_name = out.get("login")
                    print("New client {0}".format(player_name))
                    self.player_to_socket_map.update({player_name: client_socket})

                    player = model.Player(out.get("login"), out.get("department", None))

                    new_state_invoker = command.Invoker()
                    add_player_command = command.AddPlayer(player)
                    new_state_invoker.store_command(add_player_command)
                    commands = self.game_state.get_commands_creating_current_state()
                    new_state_invoker.store_commands(commands)
                    commands_json = new_state_invoker.to_json()
                    add_player_command.execute(self.game_state)
                    # self.game_state.add_player(player)

                    client_socket.sendall(bytearray(str(commands_json), 'UTF-8'))

                if "update" in out.keys():
                    # print("Client position update: {0}".format(player_name))
                    player = self.game_state.get_player(player_name)
                    current_coordinates = out.get("coordinates", None)
                    # print("Player {0} coords: {1}".format(player_name, current_coordinates))
                    direction = out.get("direction", None)
                    player_copy = copy.deepcopy(player)
                    player_copy.coordinates = (current_coordinates[0], current_coordinates[1])
                    player_copy.direction = direction
                    player_copy.calculate_velocity()
                    update_player_command = command.UpdatePlayer(player_copy)
                    # update_player_command.execute(self.game_state)
                    self.command_invoker.store_command(update_player_command)

    def handle_clients(self, server):
        while True:
            client_sock, address = server.accept()
            print(client_sock)
            single_client_handler = threading.Thread(target=self.handle_client_connection, args=(client_sock, address,))
            single_client_handler.start()

    def broadcast_game_state(self):
        # check collisions and prepare commands to update state
        commands = self.collision_detector.detect_collisions(self.game_state)
        self.command_invoker.store_commands(commands)

        # execution stage
        self.command_invoker.execute_commands(self.game_state)
        self.send_commands_to_clients()
        self.command_invoker.clear_commands()

        self.acquire_fresh_plankton()
        self.acquire_new_powerup()

    def send_commands_to_clients(self):
        commands_json = self.command_invoker.to_json()
        disconnected_clients = []
        for player in self.player_to_socket_map.keys():
            try:
                player_socket = self.player_to_socket_map.get(player)
                player_socket.sendall(bytearray(str(commands_json), 'UTF-8'))
            except BrokenPipeError:
                disconnected_clients.append(player)
        for client in disconnected_clients:
            self.player_to_socket_map.pop(client)

    def acquire_fresh_plankton(self):
        new_plankton = self.plankton_generator.get_new_plankton()
        for plankton in new_plankton:
            add_plankton_command = command.AddPlankton(plankton)
            self.command_invoker.store_command(add_plankton_command)

    def acquire_new_powerup(self):
        new_powerup = self.powerup_generator.get_new_powerup()
        for powerup in new_powerup:
            add_powerup_command = command.AddPowerup(powerup)
            self.command_invoker.store_command(add_powerup_command)


def run():
    server = Server()
    while True:
        server.broadcast_game_state()

run()
