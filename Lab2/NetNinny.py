import socket
import sys
from Header import Header
from Connection import Connection


class NetNinny:
    def __init__(self, port):
        self.MAXSIZE = 65565
        self.proxyToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientServerSocket.bind(('127.0.0.1', port))
        self.clientServerSocket.listen(5)
        self.header = Header()

    def poll(self):
        while True:
            try:

                (clientSocket, client) = self.clientServerSocket.accept()
                client_data = clientSocket.recv(self.MAXSIZE)

                if not client_data:
                    continue

                client_data_str = (client_data.decode()).replace("Proxy-Connection:", "Connection:", 1).encode()
                self.header.split_header(False, client_data)

                connection = Connection(clientSocket, self.header, client_data_str, self.MAXSIZE)
                connection.start()
                print("START: ", self.header.host)

            except socket.error as msg:
                print("From Main: ", msg)
                break


if __name__ == "__main__":
    print("Proxy open on port: ", sys.argv[1])
    proxy = NetNinny(int(sys.argv[1]))
    proxy.poll()
