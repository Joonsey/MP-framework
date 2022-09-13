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

class Network_client:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)
        self.identifier = ""
        self.responses = {}

    def connect(self):
        try:
            self.client.connect(self.addr)
            response = self.client.recv(PACKET_SIZE).decode(decoder)
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
        if self.identifier == "":
            print("ERROR: please connect to server first")
        else:
            try:
                packet = {}
                packet[self.identifier] = data
                self.client.send(str(packet).encode(decoder))
                response = self.client.recv(2048).decode(decoder)
                prev = self.responses
                if response != prev:
                    try:
                        self.responses = ast.literal_eval(response)
                    except:
                        print("server lag causing buffer to be filled twice!")
                        print(response)
                else:
                    self.responses = prev

            except socket.error as e:
                print(e)

