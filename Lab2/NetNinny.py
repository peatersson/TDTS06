import socket
import sys
from Header import Header
from Connection import Connection


class NetNinny:
    def __init__(self, port):
        self.MAXSIZE = 4096#65565
        self.activeConnections = {}
        self.activeSockets = {}
        self.proxyToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket.bind(('localhost', port))
        self.clientServerSocket.listen(5)
        self.header = Header()

    def poll(self):
        try:
            while True:
                (clientSocket, client) = self.clientServerSocket.accept()
                client_data = clientSocket.recv(self.MAXSIZE)
                if not client_data:
                    continue

                self.header.split_header(False, client_data)

                connection = Connection(clientSocket, self.header, client_data, self.MAXSIZE)
                self.activeConnections[self.header.host] = connection
                connection.start()
                # print("START")
                key_list = []

                for key in self.activeConnections:
                    t = self.activeConnections.get(key)

                    if not t.isAlive():
                        key_list.append(key)
#
                for k in key_list:
                    del self.activeConnections[k]

        except socket.error as msg:
            print("From Main: ", msg)


if __name__ == "__main__":
    print("SYSARG: ", sys.argv[1])
    proxy = NetNinny(int(sys.argv[1]))
    proxy.poll()
