import socket
import threading
import json


class Server:
    def __init__(self):
        # self.HOST, self.PORT = "localhost", 9999

        bind_ip = '0.0.0.0'
        bind_port = 9999

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((bind_ip, bind_port))
        server.listen(5)

        client_handler = threading.Thread(target=self.handle_clients(server))
        client_handler.start()

    def parse_bytes_to_json(self, data):
        data_str = data.decode('utf8').replace("'", '"')
        data_json = json.loads(data_str)
        out = json.dumps(data_json, indent=4, sort_keys=True)
        return data_json

    def handle_client_connection(self, client_socket, add):
        while True:
            request = client_socket.recv(1024).strip()
            print("{0} wrote: {1}".format(add, request))
            out = self.parse_bytes_to_json(request)
            if "login" in out.keys():
                login = out["login"]
                # TODO dane gry sa wysylane
                # if self.validate_user(login):
                # client_socket.sendall(bytearray(str(out), 'UTF-8'))

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
            single_client_handler = threading.Thread(target=self.handle_client_connection(client_sock, address))
            single_client_handler.start()


if __name__ == "__main__":
    server = Server()


