import socketserver
import socket
import threading
import json


def parse_bytes_to_json(data):
    data_str = data.decode('utf8').replace("'", '"')
    data_json = json.loads(data_str)
    out = json.dumps(data_json, indent=4, sort_keys=True)
    return out


def handle_client_connection(client_socket, add):
    while True:
        request = client_socket.recv(1024).strip()
        print("{} wrote:".format(add))
        out = parse_bytes_to_json(request)
        print(out)
        client_socket.sendall(bytearray(out+'\n', 'UTF-8'))


def handle_clients(server):
    while True:
        client_sock, address = server.accept()
        print(client_sock)
        single_client_handler = threading.Thread(target=handle_client_connection(client_sock, address))
        single_client_handler.start()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    bind_ip = '0.0.0.0'
    bind_port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections

    client_handler = threading.Thread(target=handle_clients(server))
    client_handler.start()
