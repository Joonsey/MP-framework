import socket
import uuid
from _thread import start_new_thread

decoder = 'utf-8'

class Network_server:
    def __init__(self) -> None:
        self.ip = "localhost"
        self.port = 5555
        self.addr = (self.ip, self.port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen()

    def handle_data(self, data) -> bytes:
        print("incomming data:", data)
        return b""

    def threaded_client(self, conn):
        identifier = uuid.uuid1().__str__()
        conn.send(identifier.encode(decoder))
        reply = b''
        while True:
            try:
                data = conn.recv(2048).decode(decoder)
                if not data:
                    print('Disconnected')
                    break
                else:
                    reply = self.handle_data(data)
                conn.sendall(reply)
            except socket.error as e:
                print(e)
                break

        print('Lost connection')
        conn.close()

    def run(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                print("connected! from :", addr)
                start_new_thread(self.threaded_client, (conn, ))
            except Exception as e:
                self.sock.close()
                print("error handled succesfully")
                print(e)
                exit(1)


if __name__ == "__main__":
    server = Network_server()
    try:
        server.run()
    except:
        server.sock.close()
