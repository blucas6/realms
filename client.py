import socket
import threading
import pickle
import sys
from tmp import Poop
from commands import *

class Client:
    def __init__(self):
        self.client_socket = ""
        self.IP_ADDRESS = 'localhost'
        self.PORT = 3000
        self.MAX_BUFFER_SIZE = 4096
    
    def serialize(self, obj):
        return pickle.dumps(obj)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                print(message)
            except:
                print('An error occurred while receiving messages.')
                self.client_socket.close()
                break

    def send_message(self):
        while True:
            message = input()
            if message == '/send':
                tosend = self.serialize(Poop())
                o_size = len(tosend)
                print(f'Sending poop! (size:{o_size})')
                if o_size > self.MAX_BUFFER_SIZE:
                    num_chunks = (o_size + self.MAX_BUFFER_SIZE - 1) // self.MAX_BUFFER_SIZE
                    chunks = [tosend[i * self.MAX_BUFFER_SIZE:(i + 1) * self.MAX_BUFFER_SIZE] for i in range(num_chunks)]
                else:
                    chunks = [tosend]
                message += '-'+str(o_size)
                print(f'Sent command: {message}')
                self.client_socket.send(message.encode('utf-8'))
                for chunk in chunks:
                    print(f'Sending chunks... {len(chunk)}')
                    self.client_socket.send(chunk)
            # self.client_socket.send(message.encode('utf-8'))
            elif message == '/quit':
                self.client_socket.close()
                break
            elif message == '/die':
                self.client_socket.send(message.encode('utf-8'))
                self.client_socket.close()
                break

    def SendToServer(self, cmd_type, obj=''):
        if cmd_type == CMD_SEND_OBJ:
            tosend = self.serialize(obj)
            o_size = len(tosend)
            print(f'Sending object: (size:{o_size})')
            if o_size > self.MAX_BUFFER_SIZE:
                num_chunks = (o_size + self.MAX_BUFFER_SIZE - 1) // self.MAX_BUFFER_SIZE
                chunks = [tosend[i * self.MAX_BUFFER_SIZE:(i + 1) * self.MAX_BUFFER_SIZE] for i in range(num_chunks)]
            else:
                chunks = [tosend]
            message = '/send-'+str(o_size)
            print(f'Sent command: {message}')
            self.client_socket.send(message.encode('utf-8'))
            for chunk in chunks:
                print(f'  Sending chunks... {len(chunk)}')
                self.client_socket.send(chunk)
            print('Done sending!')

    def prep(self):
        print('=Setup Client=')
        self.IP_ADDRESS = input('Enter ip address: ')
        self.PORT = int(input('Enter port: '))

    def start_client(self):
        self.prep()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP_ADDRESS, self.PORT))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_message()

client = Client()
client.start_client()
