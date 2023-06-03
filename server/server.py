import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            broadcast(message, client_socket)
        except:
            remove(client_socket)
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                remove(client)

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(10)

    print('Server started. Waiting for clients...')

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print('Client connected:', client_address)
        client_socket.send('Welcome to the chat room!'.encode('utf-8'))
        client_socket.send('Type /quit to exit.'.encode('utf-8'))
        client_socket.send('Start chatting:'.encode('utf-8'))
        threading.Thread(target=handle_client, args=(client_socket,)).start()

clients = []

start_server()
