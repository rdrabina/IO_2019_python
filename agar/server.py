import socket
import threading
import json
import time
from agar import model
from agar.engine.plankton_generator import PlanktonGenerator


class GameStateEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Server:
    def __init__(self):
        print("Server start")
        self.game_state = model.GameState()
        self.player_to_socket_map = {}
        self.plankton_generator = PlanktonGenerator()
        self.plankton_generator.start()
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
            print("{0} wrote: {1}".format(add, request))
            if request is not None:
                try:
                    out = self.parse_bytes_to_json(request)
                except json.JSONDecodeError:
                    pass
                    # TODO only happens when client disconnects
                if "login" in out.keys():
                    print("New client")
                    player_name = out.get("login")
                    self.player_to_socket_map.update({player_name: client_socket})
                    player = model.Player(out.get("login"), out.get("department", None))
                    self.game_state.add_player(player)
                    print(self.game_state)
                    starting_state = json.loads((GameStateEncoder().encode(self.game_state)))
                    client_socket.sendall(bytearray(str(starting_state), 'UTF-8'))

                if "update" in out.keys():
                    print("Client position update")
                    player = self.game_state.get_player(player_name)
                    current_coordinates = out.get("coordinates", None)
                    direction = out.get("direction", None)
                    player.coordinates = current_coordinates
                    player.direction = direction
                    player.calculate_velocity()

    def handle_clients(self, server):
        while True:
            client_sock, address = server.accept()
            print(client_sock)
            single_client_handler = threading.Thread(target=self.handle_client_connection, args=(client_sock, address,))
            single_client_handler.start()

    def broadcast_game_state(self):
        game_state_json = json.loads(GameStateEncoder().encode(self.game_state))
        self.check_clients_connection(game_state_json)
        #TODO check collision with plankton
        self.acquire_fresh_plankton()

    def check_clients_connection(self, game_state_json):
        disconnected_clients = []
        for player in self.player_to_socket_map.keys():
            try:
                player_socket = self.player_to_socket_map.get(player)
                player_socket.sendall(bytearray(str(game_state_json), 'UTF-8'))
            except BrokenPipeError:
                disconnected_clients.append(player)
        for client in disconnected_clients:
            self.player_to_socket_map.pop(client)

    def acquire_fresh_plankton(self):
        new_plankton = self.plankton_generator.get_new_plankton()
        for plankton in new_plankton:
            #TODO create command ADD PLANKTON
            self.game_state.add_plankton(plankton)


def run():
    server = Server()
    while True:
        time.sleep(1)
        server.broadcast_game_state()

