import socket
import threading
import pickle
import sys
from tmp import Poop
from gameserver import GameServer
from commands import *

class Server:
    def __init__(self):
        self.clients = []
        self.IP_ADDRESS = 'localhost'
        self.PORT = 3000
        self.MAX_BUFFER_SIZE = 4096

        self.GameServer = GameServer()

    def SendToClient(self, client_socket, cmd_type, objtosend=''):
        # send stuff to clients
        if cmd_type == CMD_SEND_OBJ:
            tosend = pickle.dumps(objtosend)
            o_size = len(tosend)
            print(f'Sending object (size:{o_size})')
            if o_size > self.MAX_BUFFER_SIZE:
                num_chunks = (o_size + self.MAX_BUFFER_SIZE - 1) // self.MAX_BUFFER_SIZE
                chunks = [tosend[i * self.MAX_BUFFER_SIZE:(i + 1) * self.MAX_BUFFER_SIZE] for i in range(num_chunks)]
            else:
                chunks = [tosend]
            message = CMD_SEND_OBJ+'-'+str(o_size)
            print(f'Sent command: {message}')
            client_socket.send(message.encode('utf-8'))
            for chunk in chunks:
                print(f'Sending chunks... {len(chunk)}')
                client_socket.send(chunk)
        elif cmd_type == CMD_SEND_MSG:
            message = CMD_SEND_MSG + 'Hello nerd'
            client_socket.send(message.encode('utf-8'))

    def handle_client(self, client_socket):
        # constantly listening for client events
        while True:
            try:
                # print('Waiting for messages...')
                message = client_socket.recv(1024).decode('utf-8')
                if message[0:len(CMD_SEND_OBJ)] == CMD_SEND_OBJ:
                    for c in range(len(message)):
                        if message[c] == '-':
                            total_size = int(message[c+1::])
                    serialized_obj = b''
                    print(f'Receiving object (size:{total_size})')
                    while total_size > 0:
                        print('Total size: ', total_size)
                        chunk = client_socket.recv(min(total_size, self.MAX_BUFFER_SIZE))
                        serialized_obj += chunk
                        total_size -= len(chunk)
                        print(f'recv chunk {len(chunk)} bytes left {total_size}')
                    original_obj = pickle.loads(serialized_obj)
                    print(f'Object Message: {original_obj.msg}')
                elif message == '/die':
                    self.ServerShutdown()
            except Exception as e:
                print(f'Failed: {e}')
                self.remove(client_socket)
                break
    
    def ServerShutdown(self):
        print('\nServer is exiting...')
        self.server_socket.close()
        sys.exit(0)

    def remove(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def prep(self):
        # server start up
        print('=Server Setup=')
        self.IP_ADDRESS = input('Enter ip address: ')
        self.PORT = int(input('Enter port: '))

    def start_server(self):
        # main function: starts server, accepts connections
        self.prep()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP_ADDRESS, self.PORT))
        self.server_socket.listen(10)

        print('Server started. Waiting for clients...')

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                print('Client connected:', client_address)
                client_socket.send('Type /quit to exit.'.encode('utf-8'))
                siteindex = len(self.clients)-1
                objtosend = self.GameServer.sites[siteindex]
                self.SendToClient(client_socket, CMD_SEND_OBJ, objtosend)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except:
                self.ServerShutdown()
serv = Server()
serv.start_server()

server = Server()
server.start_server()