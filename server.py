import socket
from sys import argv
import ast
import uuid
PACKET_SIZE = 16000
IP = "0.0.0.0"
PORT = 5555

decoder = 'utf-8'

index = 0

def IOTA(force=False):
    """
    ENUMERATOR
    """
    global index
    if force:
        index = 0
    index += 1
    return index.to_bytes(1,'big')

class Network_server:
    def __init__(self, ip, port) -> None:
        self.ip = IP
        self.port = PORT
        self.addr = (self.ip, self.port)
        self.all_players = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.addr)
        #self.sock.listen()

    def handle_data(self, data: bytes) -> bytes:
        identification = data[0].to_bytes(1, 'little')
        if identification == b'\x00':
            identification = IOTA()
            return identification
        else:
            location = data[1:3]
            color = data[3:6]
            direction = data[6]
            self.all_players[identification] = data[1:]
            return self.format_all_players()

    def format_all_players(self) -> bytes:
        players = self.all_players
        response = b''
        for id in players.keys():
            response += id
            response += players[id]
        return response

    def run(self):
        print("server is listening...\n")
        while True:
            try:
                response = self.sock.recvfrom(PACKET_SIZE)
                data = response[0]
                address = response[1]
                response = self.handle_data(data)
                self.sock.sendto(response, address)
            except Exception as e:
                self.sock.close()
                print("error handled succesfully")
                print(e)
                break
        exit(1)

if __name__ == "__main__":
    args = len(argv) > 1
    if args:
        if argv[1] == '-l':
            IP = "localhost"
    server = Network_server(IP, PORT)
    server.run()
