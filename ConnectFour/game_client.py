import socket
import sys

class Client():
    def __init__(self, target_host, target_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((target_host, target_port))
    

if __name__ == "__main__":
    
    target_host = "192.168.1.169"
    target_port = 4444

    client = Client(target_host, target_port)
    client_socket = client.client

    received = client_socket.recv(1024).decode('utf-8')

    if "start" in received:
        message = input("Message to server: ")
        client_socket.send(message.encode('utf-8'))
        print("Sent message to server")
        received = client_socket.recv(1024).decode('utf-8')
        print("[*] Received: %s from server" % received)
    else:
        print("[*] Received: %s from server" % received)

    while True:

        message = input("Message to server: ")
        client_socket.send(message.encode('utf-8'))
        print("Sent message to server")

        received = client_socket.recv(1024)
        print("[*]  Received: %s from server" % received)
