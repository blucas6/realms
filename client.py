import socket
import threading

class Client:
    def __init__(self):
        self.client_socket = ""
        self.IP_ADDRESS = 'localhost'
        self.PORT = 3000

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
            self.client_socket.send(message.encode('utf-8'))
            if message == '/quit':
                self.client_socket.close()
                break

    def prep(self):
        print('=Setup Client=')
        self.IP_ADDRESS = input('Enter ip addres: ')
        self.PORT = input('Enter port: ')

    def start_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP_ADDRESS, self.PORT))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_message()

client = Client()
client.start_client()
