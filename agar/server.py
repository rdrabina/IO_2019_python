import socketserver
import json


def parse_bytes_to_json(data):
    data_str = data.decode('utf8').replace("'", '"')
    data_json = json.loads(data_str)
    out = json.dumps(data_json, indent=4, sort_keys=True)
    return out


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self):
        self.data = None

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        out = parse_bytes_to_json(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(out)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("server started")
        server.serve_forever()
