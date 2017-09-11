import socket
from Header import Header
from Connection import Connection
from threading import Thread

class NetNinny:
    def __init__(self):
        self.MAXSIZE = 65565
        self.activeConnections = {}
        self.activeSockets = {}
        self.proxyToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.proxyToServer.settimeout(15)

        self.clientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket.bind(('localhost', 8080))
        self.clientServerSocket.listen(5)

    def poll(self):
        try:
            while True:
                (clientSocket, client) = self.clientServerSocket.accept()
                clientData = clientSocket.recv(self.MAXSIZE)

                #print(client)

                #self.activeSockets[]

                if not clientData:
                    continue

                # possible new connection
                self.header = Header()
                self.header.splitHeader(clientData)

                #if self.header.host in self.activeConnections.keys():
                 #   print("samma tråd")
                    # new connection to same host
                  #  x = 0

                # create new thread for this connection
                #else:
                print("ny tråd: ", self.header.host)
                connection = Connection(clientSocket, self.header, clientData, self.MAXSIZE)
                self.activeConnections[self.header.host] = connection
                connection.start()
                print("START")
                keyList = []

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
    proxy = NetNinny()
    proxy.poll()