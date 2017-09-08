import socket, sys
from Header import Header


class NetNinny:
    def __init__(self):
        self.proxyToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket.bind(('localhost', 8080))
        self.clientServerSocket.listen(5)

    def poll(self):
        try:
            while True:
                print("Before accept")
                (clientSocket, client) = self.clientServerSocket.accept()
                while True:
                    clientData = clientSocket.recv(1024)
                    if not clientData:
                        break
                    print(clientData)
                    self.proxyToServer.settimeout(15)

                    print(clientData.decode("utf-8"))

                    self.headers = Header()
                    self.headers.splitHeader(clientData)

                    try:
                        self.proxyToServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        print("hello")
                        self.proxyToServer.connect((self.headers.host, self.headers.port))
                        print("din")
                    except socket.error as msg:
                        print("cant reconnect or connect to proxyToServer")

                    self.proxyToServer.send(clientData)
                    print("mamma")
                    recieved = self.proxyToServer.recv(1024)
                    clientSocket.send(recieved)

                self.proxyToServer.close()
                clientSocket.close()

        except socket.error as msg:
            print(msg)
            clientSocket.close()
            print("hej")
            self.proxyToServer.close()
            print("då")


if __name__ == "__main__":
    proxy = NetNinny()
    proxy.poll()