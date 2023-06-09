import socket
import threading

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print('An error occurred while receiving messages.')
            client_socket.close()
            break

def send_message():
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message == '/quit':
            client_socket.close()
            break

def start_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_message()

start_client()
