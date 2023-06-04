import socket
import threading

class Server:
    def __init__(self):
        self.clients = []
        self.IP_ADDRESS = 'localhost'
        self.PORT = 3000

        

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                print(message)
            except:
                self.remove(client_socket)
                break

    def remove(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def prep(self):
        print('=Server Setup=')
        self.IP_ADDRESS = input('Enter ip address: ')
        self.PORT = input('Enter port: ')

    def start_server(self):
        self.prep()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.IP_ADDRESS, self.PORT))
        server_socket.listen(10)

        print('Server started. Waiting for clients...')

        while True:
            client_socket, client_address = server_socket.accept()
            self.clients.append(client_socket)
            print('Client connected:', client_address)
            client_socket.send('Type /quit to exit.'.encode('utf-8'))
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()


server = Server()
server.start_server()
