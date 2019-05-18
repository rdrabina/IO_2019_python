import threading
import socketserver


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall("hello")


def run():
    print("server started")
    HOST, PORT = "localhost", "9999"
    server = socketserver.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()

