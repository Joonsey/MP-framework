import socket
from _thread import start_new_thread
decoder = 'utf-8'

def run_in_thread(func):
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
        self.responses = ['init']

    def connect(self):
        try:
            self.client.connect(self.addr)
            response = self.client.recv(2048).decode(decoder)
            self.identifier = response
            return response
        except:
            return False

    @run_in_thread
    def open_recieve_thread(self):
        try:
            response = self.client.recv(2048).decode(decoder)
            return response
        except:
            pass


    @run_in_thread
    def send(self, data):
        if self.identifier == "":
            print("ERROR: please connect to server first")
        else:
            try:
                self.client.send(str.encode(data))
                response = self.client.recv(2048).decode(decoder)
                prev = self.responses.pop()
                if response != prev:
                    self.responses.append(response)
                else:
                    self.responses.append(prev)

            except socket.error as e:
                print(e)

