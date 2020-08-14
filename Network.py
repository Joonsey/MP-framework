import socket
decoder = 'utf-8'


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.localip = '192.168.1.115'
        self.globalip = "85.166.63.108"
        self.port = 5555
        self.addr = (self.localip, self.port)
        self.pos = self.connect()
        
        

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode(decoder)
        except:
            pass


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode(decoder)
        
        except socket.error as e:
            print(e)

n = Network().send('15,25')
