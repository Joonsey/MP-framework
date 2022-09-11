import socket
from _thread import start_new_thread
decoder = 'utf-8'

def run_in_thead(func):
    def run(*k, **kw):
        start_new_thread(func, k)
    return run

class Network_client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = "localhost"
        self.port = 5555
        self.addr = (self.ip, self.port)
        self.identifier = ""

    def connect(self):
        try:
            self.client.connect(self.addr)
            response = self.client.recv(2048).decode(decoder)
            self.identifier = response
            return response
        except:
            return False


    @run_in_thead
    def send(self, data):
        if self.identifier == "":
            print("ERROR: please connect to server first")
        else:
            try:
                self.client.send(str.encode(data))
                return self.client.recv(2048).decode(decoder)

            except socket.error as e:
                print(e)

