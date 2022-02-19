import socket
import threading


class Server():

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 4444))

def handle_clients(client_socket1, client_socket2):
    
    ##  Notify player1 to start
    start_message = "start".encode('utf-8')
    client_socket1.send(start_message)

    ## Pass messages between the clients
    while True:
        request = client_socket1.recv(1024)
        print("[*]  Received: %s from client1" % request)

        client_socket2.send(request)
        print("[*]  Sent %s to client2" % request)

        request = client_socket2.recv(1024)
        print("[*]  Received: %s from client2" % request)

        client_socket1.send(request)
        print("[*]  Send %s to client1" % request)

if __name__ == "__main__":

    gameserver = Server()
    gameserver.server.listen(2)

    while True:

        client1, addr1 = gameserver.server.accept()

        print("[*]  Accepted connection from: %s%d" % (addr1[0], addr1[1]))

        client2, addr2 = gameserver.server.accept()

        print("[*]  Accepted connection from: %s%d" % (addr2[0], addr2[1]))

        client_handler = threading.Thread(target=handle_clients, args=(client1, client2))
        client_handler.start()