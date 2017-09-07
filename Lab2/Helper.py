import socket, sys


class NetNinny:
    def __init__(self):
        self.proxyToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket.bind(('localhost', 8080))
        self.clientServerSocket.listen(5)

    def poll(self):
        try:
            while True:
                (clientSocket, client) = self.clientServerSocket.accept()
                clientData = clientSocket.recv(1024)

                self.proxyToServer.settimeout(15)

                self.proxyToServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.proxyToServer.connect(('www.ida.liu.se', 80))

                print(self.proxyToServer.send(clientData))

                recieved = self.proxyToServer.recv(1024)

                print(recieved)

                clientSocket.send(recieved)

                self.proxyToServer.close()
                self.clientServerSocket.close()

                break

        except socket.error as msg:
            print(msg)
            self.clientServerSocket.close()
            self.proxyToServer.close()


if __name__ == "__main__":
    proxy = NetNinny()
    proxy.poll()