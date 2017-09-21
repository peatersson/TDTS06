
class Header:

    def __init__(self):
        self.headers = 0
        self.host = 0
        self.port = 0
        self.connection = 0
        self.get = 0
        self.body = 0
        self.content_type = 0
        self.date = 0
        self.http_version = 0
        self.server = 0
        self.user_agent = 0
        self.accept = 0
        self.accept_encoding = 0
        self.accept_language = 0
        self.content_length = 0

    # Server is 1, client is 0
    def split_header(self, server, data):
        try:
            pos = data.find(b'\r\n\r\n')
            if pos == -1:
                self.body = data.decode("utf-8")
                return
            temp = data[0:pos]
            if server:
                self.body = data[pos+1:].decode("utf-8")
            else:
                self.body = 0
            split_lines = temp.decode("utf-8").split("\r\n")
        except UnicodeDecodeError as msg:
            print("Error:", msg)
            return
        # Loop through all objects and take Host

        for elem in split_lines:
            if "Host" in elem:
                self.host = elem.split(" ")[1]
                # Check if host contains port or should be default port 80
                if ":" in self.host:
                    split_string = self.host.split(":")
                    self.host = split_string[0]
                    self.port = int(split_string[1])
                else:
                    self.port = 80
            if "Connection" in elem:
                self.connection = elem.split(" ")[1]
            if "GET" in elem:
                self.get = elem.split(" ")[1]
            if "Content-Type" in elem:
                if server:
                    self.content_type = elem.split(" ")[1]
                else:
                    self.content_type = 0
            if "Date" in elem:
                self.date = str.replace(elem, elem.split(" ")[0], "", )
            if "HTTP/1." in elem:
                if server:
                    self.http_version = elem.split(" ")[0]
                else:
                    self.http_version = elem.split(" ")[2]
            if "Server" in elem:
                self.server = elem.split(" ")[1]
            if "User-Agent" in elem:
                self.user_agent = elem.split(" ")[1]
            if "Accept:" in elem:
                self.accept = elem.split(" ")[1]
            if "Accept-Encoding" in elem:
                self.accept_encoding = elem.split(" ")[1]
            if "Accept-Language" in elem:
                self.accept_language = elem.split(" ")[1]
            if "Content-Length" in elem:
                self.content_length = int(elem.split(" ")[1])

       # if server and len(split_lines) > 0:
        #    if split_lines[len(split_lines)-1]:
         #       self.body = split_lines[len(split_lines)-1]

    def clear_headers(self):
        self.headers = 0
        self.host = 0
        self.port = 0
        self.connection = 0
        self.get = 0
        self.body = 0
        self.content_type = 0
        self.date = 0
        self.http_version = 0
        self.server = 0
        self.user_agent = 0
        self.accept = 0
        self.accept_encoding = 0
        self.accept_language = 0
