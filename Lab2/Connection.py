import socket


class Connection:
    def __init__(self, cS, headers, data, size):
        self.MAXSIZE = size
        self.clientSocket = cS
        self.header = headers
        self.data = data
        self.serverDisc = False
        self.clientDisc = False

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.serverSocket.settimeout(15)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.connect((self.header.host, self.header.port))

        self.serverSocket.setblocking(0)
        self.clientSocket.setblocking(0)

    def poll(self):
        self.serverSocket.send(self.data)

        while True:
            try:
                fromServer = self.serverSocket.recv(self.MAXSIZE)

                if fromServer == b'':
                    if self.clientDisc:
                        break
                    else:
                        self.serverDisc = True
                else:
                    self.serverDisc = False
                    self.clientSocket.send(fromServer)

            except socket.error as msg:
                x = 0

            try:
                fromClient = self.clientSocket.recv(self.MAXSIZE)

                if fromClient == b'':
                    if self.serverDisc:
                        break
                    else:
                        self.clientDisc = True
                else:
                    self.clientDisc = False
                    self.data = fromClient
                    temphost = self.header.host
                    self.header.splitHeader(self.data)
                    self.serverSocket.send(self.data)
                    print("temp: ", temphost, "header: ", self.header.host)

            except socket.error as msg:
                if socket.error.errno == socket.errno.ENODATA:
                    print("no data")

        self.clientSocket.close()
        self.serverSocket.close()





