import socketserver
import json


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self):
        self.data = None

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        print(json.dumps(self.data))
        # just send back the same data, but upper-cased
        self.request.sendall(json.dumps(self.data))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("server started")
        server.serve_forever()
