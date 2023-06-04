import socket
import threading
import pickle
import sys
from tmp import Poop

class Server:
    def __init__(self):
        self.clients = []
        self.IP_ADDRESS = 'localhost'
        self.PORT = 3000
        self.MAX_BUFFER_SIZE = 4096

    def handle_client(self, client_socket):
        while True:
            try:
                print('Waiting for messages...')
                message = client_socket.recv(1024).decode('utf-8')
                print('Received:',message)
                if message[0:6] == '/send-':
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
        print('=Server Setup=')
        self.IP_ADDRESS = input('Enter ip address: ')
        self.PORT = int(input('Enter port: '))

    def start_server(self):
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
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except:
                self.ServerShutdown()
