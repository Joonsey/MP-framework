import socket
import ast
decoder = 'utf-8'
from tools import PACKET_SIZE, GLOBAL_SERVER_IP, BYTEORDER
from tools import run_in_thread




# NEW PACKET STRUCTURE BASED ON INDEXATION
"""
[0 : identifier | 1+2, 3+4 : location | 5-8: color | 9 : special]

i.e:
    - direction
    - event
"""
class Packet:
    def __init__(self, id, x, y, color, direction):
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction

class Network_client:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (ip, port)
        self.identifier = b"\x00"
        self.responses = {}

    def connect(self):
        """
        network now relies on UDP protocol.
        """
        try:
            self.client.sendto(self.identifier, self.addr)
            response = self.client.recv(PACKET_SIZE)
            self.identifier = response
            return response
        except:
            return False

    @run_in_thread
    def open_recieve_thread(self):
        try:
            response = self.client.recv(PACKET_SIZE).decode(decoder)
            return response
        except:
            pass


    @run_in_thread
    def send(self, data):
        try:
            self.client.sendto(data, self.addr)
            response = self.client.recv(PACKET_SIZE)
            self.responses = response
        except socket.error as e:
            print(e)

