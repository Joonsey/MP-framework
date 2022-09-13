import socket
import ast
import uuid
PACKET_SIZE = 16000


decoder = 'utf-8'

class Network_server:
    def __init__(self) -> None:
        self.ip = "localhost"
        self.port = 5555
        self.addr = (self.ip, self.port)
        self.all_locations = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.addr)
        #self.sock.listen()

    def handle_data(self, data, address):
        try:
            if data == b"":
                response = uuid.uuid1().__str__().encode(decoder)
            else:
                data = ast.literal_eval(data.decode(decoder))
                self.all_locations.update(data)
                locations = []
                for identifier in self.all_locations.keys():
                    info = self.all_locations[identifier]
                    locations.append(info)
                response = str(self.all_locations).encode(decoder)
            return response
        except Exception as e:
            print(e)
            print(address, "didn't parse packet as intended.")
            pass

    def run(self):
        print("server is listening...\n")
        while True:
            try:
                response = self.sock.recvfrom(PACKET_SIZE)
                data = response[0]
                address = response[1]
                response = self.handle_data(data, address)
                self.sock.sendto(response,address)
            except:
                self.sock.close()
                print("error handled succesfully")
                break
        exit(1)

if __name__ == "__main__":
    server = Network_server()
    server.run()
