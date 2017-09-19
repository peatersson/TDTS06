import socket
import threading
from WebFilter import WebFilter


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

        self.filter = WebFilter()
        self.filter.add_forbidden_word("SpongeBob")
        self.filter.add_forbidden_word("Britney Spears")
        self.filter.add_forbidden_word("Paris Hilton")
        self.filter.add_forbidden_word("Norrkoping")

    def run(self):
        #print("Request: ", self.data)
        if self.header.get:
            if self.filter.contains_forbidden_word(self.header.get):
                self.data = self.filter.create_response(self.filter.forbidden_URL_response, self.header.date, \
                                                        self.header.http_version, self.header.server)

        self.serverSocket.send(self.data)

        while True:
            try:
                from_server = self.serverSocket.recv(self.MAXSIZE)
                #print("fromServer: ", fromServer)
                self.header.split_header(True, from_server)
                print("Body: ", self.header.body)
                if self.header.content_type == "text/html" and self.header.body:
                    if self.filter.contains_forbidden_word(self.header.body):
                        from_server = self.filter.create_response(self.filter.forbidden_content_response, \
                                                                  self.header.date, self.header.http_version, \
                                                                  self.header.server)

                self.clientSocket.send(from_server)
                if from_server == b'':
                    break

            except socket.error as msg:
                #print("FromServer: ", msg)
                x = 1

            try:
                from_client = self.clientSocket.recv(self.MAXSIZE)
                #print("fromClient: ", fromServer)
                if from_client == b'':
                    self.serverSocket.send(from_client)
                    break
                else:
                    self.data = from_client
                    self.header.split_header(False, self.data)
                    if self.header.get:
                        if self.filter.contains_forbidden_word(self.header.get):
                            self.data = self.filter.create_response(self.filter.forbidden_URL_response, \
                                                                    self.header.date, self.header.http_version, \
                                                                    self.header.server)
                    self.serverSocket.send(self.data)
            except socket.error as msg:
                msg
                #print("FromClient: ", msg)


        print("CLOSING")
        self.clientSocket.close()
        self.serverSocket.close()





