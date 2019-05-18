import socket
import threading
import json
from agar import model


class GameStateEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Server:
    def __init__(self):
        self.game_state = model.GameState()
        bind_ip = '0.0.0.0'
        bind_port = 9999
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
        while True:
            request = client_socket.recv(1024).strip()
            print("{0} wrote: {1}".format(add, request))
            out = self.parse_bytes_to_json(request)
            if "login" in out.keys():
                player = model.Player(out["login"], out.get("department", None))
                self.game_state.add_player(player)
                print(self.game_state)
                starting_state = json.loads((GameStateEncoder().encode(self.game_state)))
                client_socket.sendall(bytearray(str(starting_state), 'UTF-8'))

            client_socket.sendall(bytearray(str(out), 'UTF-8'))

    def validate_user(self, nick):
        pass
        # TODO zamienic na gamestate
        # for user in active_clients.keys():
        #    if nick == user:
        #        return False
        # return True

    def handle_clients(self, server):
        while True:
            client_sock, address = server.accept()
            print(client_sock)
            single_client_handler = threading.Thread(target=self.handle_client_connection, args=(client_sock, address,))
            single_client_handler.start()


def main():
    server = Server()
    print(json.loads((GameStateEncoder().encode(server.game_state))))


if __name__ == "__main__":
    main()
