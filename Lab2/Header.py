
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


    # Server is 1, client is 0
    def split_header(self, server, data):
        #print("Decode: ", data)
        try:
            split_lines = data.decode("utf-8").split("\r\n")
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
            elif "Connection" in elem:
                if str(elem.split(" ")[1]).lower() == 'keep-alive':
                    self.connection = True
                else:
                    self.connection = False
            elif "GET" in elem:
                self.get = elem.split(" ")[1]
            elif "Content-Type" in elem:
                if server:
                    self.content_type = elem.split(" ")[1]
                else:
                    self.content_type = 0
            elif "Date" in elem:
                self.date = str.replace(elem, elem.split(" ")[0], "", )
            elif "HTTP/1." in elem:
                self.http_version = elem.split(".")[1]
            elif "Server" in elem:
                self.server = elem.split(" ")[1]

        if server and len(split_lines) > 0:
            if split_lines[len(split_lines)-1]:
                self.body = split_lines[len(split_lines)-1]
