import socket
import ast
import uuid
from _thread import start_new_thread

decoder = 'utf-8'


class Network_server:
    def __init__(self) -> None:
        self.ip = "localhost"
        self.port = 5555
        self.addr = (self.ip, self.port)
        self.all_locations = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen()

    def handle_data(self, identifier, data) -> bytes:
        data = ast.literal_eval(data)
        self.all_locations.update(data)

        locations = []
        for identifier in self.all_locations.keys():
            info = self.all_locations[identifier]
            locations.append(info)
        response = str(self.all_locations).encode(decoder)
        return response

    def threaded_client(self, conn):
        identifier = uuid.uuid1().__str__()
        conn.send(identifier.encode(decoder))
        reply = b''
        while True:
            try:
                data = conn.recv(2048).decode(decoder)
                if not data:
                    self.all_locations.pop(identifier)
                    print('Disconnected')
                    break
                else:
                    reply = self.handle_data(identifier, data)
                conn.sendall(reply)
            except socket.error as e:
                print("error occured")
                print(e)
                break


        print('Lost connection width:',identifier)
        conn.close()

    def run(self):
        print("server is listening...\n")
        while True:
            try:
                conn, addr = self.sock.accept()
                print("connected! from :", addr)
                start_new_thread(self.threaded_client, (conn, ))
            except:
                self.sock.close()
                print("error handled succesfully")
                break
        exit(1)

if __name__ == "__main__":
    server = Network_server()
    server.run()
