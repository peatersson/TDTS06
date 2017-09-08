

class Header:

    def __init__(self):
        self.headers = 0
        self.host = 0
        self.port = 0
        self.connection = 0

    def splitHeader(self, data):
        splittedLines = data.decode("utf-8").splitlines();

        #Loop through all objects and take Host

        for elem in splittedLines:
            if "Host" in elem:
                self.host = elem.split(" ")[1]
            elif "Connection" in elem:
                if str(elem.split(" ")[1]).lower() == 'keep-alive':
                    self.connection = True
                else:
                    self.connection = False

        #Check if host contains port or should be default port 80
        if ":" in self.host:
            splitstring = self.host.split(":")
            self.host = splitstring[0]
            self.port = int(splitstring[1])
        else:
            self.port = 80
        #print("Host: ", self.host, "Port: ", self.port)