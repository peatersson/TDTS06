import socket
import threading

class Connection(threading.Thread):
    def __init__(self, cS, headers, data, size):
        threading.Thread.__init__(self)
        self.MAXSIZE = size
        self.clientSocket = cS
        self.header = headers
        self.data = data
        self.serverDisc = False
        self.clientDisc = False

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.serverSocket.settimeout(5)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.connect((self.header.host, self.header.port))

        self.serverSocket.setblocking(0)
        self.clientSocket.setblocking(0)

    def run(self):
        #print("Request: ", self.data)
        self.serverSocket.send(self.data)

        while True:
            try:
                fromServer = b''
                fromServer = self.serverSocket.recv(self.MAXSIZE)
                #print("fromServer: ", fromServer)
                self.clientSocket.send(fromServer)
                if fromServer == b'':
                    break

            except socket.error as msg:
                #print("FromServer: ", msg)
                x=1

            try:
                fromClient = b''
                fromClient = self.clientSocket.recv(self.MAXSIZE)
                #print("fromClient: ", fromServer)
                if fromClient == b'':
                    self.serverSocket.send(fromClient)
                    break
                else:
                    self.data = fromClient
                    self.header.splitHeader(self.data)
                    self.serverSocket.send(self.data)
            except socket.error as msg:
                #print("FromClient: ", msg)
                msg


        print("CLOSING")
        self.clientSocket.close()
        self.serverSocket.close()





