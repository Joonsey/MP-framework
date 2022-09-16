import socket
import ast
decoder = 'utf-8'
from tools import PACKET_SIZE, GLOBAL_SERVER_IP
from tools import run_in_thread


# NETWORK PACKET FORMAT
# OBJECT LOCATION
"""
{IDENTIFIER:
    {
        location: [x,y],
        color: (r,g,b),
        state: ?,
    }
}
"""

#TODO: NEW PACKET STRUCTURE BASED ON INDEXATION
"""
[0 : identifier | 1-3: location | 7: color | 8+ : special]

special: kwargs**
i.e:
    - direction
    - event
"""
#NB subject to change

class Network_client:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (ip, port)
        self.identifier = b"\x00"
        self.responses = {}

    def connect(self):
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

