import socketserver
import socket
import threading
import json


def parse_bytes_to_json(data):
    data_str = data.decode('utf8').replace("'", '"')
    data_json = json.loads(data_str)
    out = json.dumps(data_json, indent=4, sort_keys=True)
    return out


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        out = parse_bytes_to_json(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(bytearray(out, 'UTF-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

def handle_client_connection(client_socket, add):
    print("sds")
    request = client_socket.recv(1024).strip()
    print("{} wrote:".format(add))
    out = parse_bytes_to_json(request)
    client_sock.sendall(bytearray(out+'\n', 'UTF-8'))

while True:
    client_sock, address = server.accept()
    print(client_sock)
    handle_client_connection(client_sock, address)
    # client_handler = threading.Thread(
    #     target=handle_client_connection,
    #     args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    # )
client_handler.start()

    # with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    #     print("server started")
    #     server.serve_forever()
