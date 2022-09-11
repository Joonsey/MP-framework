import socket
import uuid
from _thread import start_new_thread

decoder = 'utf-8'

def move_rect(data: list):
    current_loc = (data[0],data[1])
    return str((int(current_loc[0]) +10, int(current_loc[1])))

net_codes = {
    # expected structure of data:
    # op_code / op_identifier : function call
    "op_move": move_rect
}

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
        parsed_data = data.split(",")
        print(parsed_data)

        unit = parsed_data[0]
        operation = net_codes[parsed_data[1]]
        arguments = parsed_data[2:]
        response = operation(arguments)

        return response.encode(decoder)

    def threaded_client(self, conn):
        identifier = uuid.uuid1().__str__()
        conn.send(identifier.encode(decoder))
        reply = b''
        while True:
            try:
                data = conn.recv(2048).decode(decoder)
                print("incomming data:", data)
                if not data:
                    print('Disconnected')
                    break
                else:
                    #reply = self.handle_data(data)
                    pass
                conn.sendall(reply)
            except socket.error as e:
                print("error occured")
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
            except:
                self.sock.close()
                print("error handled succesfully")
                break
        exit(1)

if __name__ == "__main__":
    server = Network_server()
    server.run()
