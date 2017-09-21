import socket
import threading
from WebFilter import WebFilter



class Connection(threading.Thread):
    def __init__(self, cs, headers, data, size):
        threading.Thread.__init__(self)
        self.MAXSIZE = size
        self.clientSocket = cs
        self.header = headers
        self.data = data
        self.serverDisc = False
        self.clientDisc = False

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.connect((self.header.host, self.header.port))
        self.serverSocket.settimeout(0.5)

        #self.serverSocket.setblocking(0)
        #self.clientSocket.setblocking(0)

        self.filter = WebFilter()
        self.filter.add_forbidden_word("SpongeBob")
        self.filter.add_forbidden_word("Britney Spears")
        self.filter.add_forbidden_word("Paris Hilton")
        self.filter.add_forbidden_word("Norrkoping")

    def run(self):
        try:
            if self.header.get:
                if self.filter.contains_forbidden_word(self.header.get):
                    self.data = self.filter.create_response(True, self.header)
                    self.clientSocket.send(self.data)
                    self.header.clear_headers()
                    self.clientSocket.close()
                    self.serverSocket.close()
                    return

            self.serverSocket.send(self.data)

            from_server = b''
            buffer = b''
            while True:
                try:
                    buffer = self.serverSocket.recv(self.MAXSIZE)
                    if len(buffer) == 0:
                        break
                except :
                    break
                from_server = b''.join([from_server, buffer])

            self.header.split_header(True, from_server)

            if self.header.content_type == "text/html" and self.header.body:
                if self.filter.contains_forbidden_word(self.header.body):
                    from_server = self.filter.create_response(False, self.header)
                    self.clientSocket.send(from_server)
                    self.header.clear_headers()
                    self.clientSocket.close()
                    self.serverSocket.close()
                    return

            self.clientSocket.send(from_server)
                #Insert multiline comment here
                #self.header.clear_headers()
            self.clientSocket.close()
            self.serverSocket.close()

        except socket.error as msg:
            print("MESSAGE:", msg)
