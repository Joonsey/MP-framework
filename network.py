import socket
decoder = 'utf-8'


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
            pass


    def send(self, data):
        if self.identifier == "":
            print("ERROR: please connect to server first")
        else:
            try:
                data = self.identifier + "," + data
                self.client.send(str.encode(data))
                return self.client.recv(2048).decode(decoder)

            except socket.error as e:
                print(e)

