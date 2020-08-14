import socket
from _thread import *
import sys
import Network

decoder = 'utf-8'
globalip = '85.166.63.108'
localip = '192.168.1.115'
port = 5555
currentPlayers = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((localip, port))


s.listen(2)
print('Server is listening, server started')

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])
pos = [(0,0),(100,100)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ''
    while True:
        try:
            data = read_pos(conn.recv(2048).decode(decoder))
            pos[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos
                print('Received: ', reply)
                print('Sending: ',reply)
            
            conn.sendall(str.encode(reply))
        except: break

    print('Lost connection')
    conn.close()
    



while True:
    conn, addr = s.accept()
    print(f'{addr} connected!')

    start_new_thread(threaded_client, (conn, 1))
    currentPlayers += 1

