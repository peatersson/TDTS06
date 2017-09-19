import socket
import sys
from Header import Header
from Connection import Connection


class NetNinny:
    def __init__(self, port):
        self.MAXSIZE = 100000#65565
        self.activeConnections = {}
        self.activeSockets = {}
        self.proxyToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.proxyToServer.settimeout(15)

        self.clientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket.bind(('localhost', port))
        self.clientServerSocket.listen(5)
        self.header = Header()

    def poll(self):
        try:
            while True:
                (clientSocket, client) = self.clientServerSocket.accept()
                client_data = clientSocket.recv(self.MAXSIZE)

                #print(client)

                #self.activeSockets[]

                if not client_data:
                    continue

                # possible new connection
                self.header.split_header(False, client_data)
                #if self.header.host in self.activeConnections.keys():
                 #   print("samma tråd")
                    # new connection to same host
                  #  x = 0

                # create new thread for this connection
                #else:
                print("ny tråd: ", self.header.host)
                connection = Connection(clientSocket, self.header, client_data, self.MAXSIZE)
                self.activeConnections[self.header.host] = connection
                connection.start()
                print("START")
                #keyList = []

                #for key in self.activeConnections:
                 #   t = self.activeConnections.get(key)

                  #  if not t.isAlive():
                   #     keyList.append(key)
#
                #for k in keyList:
               #     del self.activeConnections[k]

        except socket.error as msg:
            print("From Main: ", msg)


if __name__ == "__main__":
    print("SYSARG: ", sys.argv[1])
    proxy = NetNinny(int(sys.argv[1]))
    proxy.poll()
