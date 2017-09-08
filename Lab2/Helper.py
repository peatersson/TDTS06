import socket, sys


class NetNinny:
    def __init__(self):
        self.proxyToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientServerSocket.bind(('localhost', 8080))
        self.clientServerSocket.listen(5)

    def poll(self):
        try:
            while True:
                print("Before accept")
                (clientSocket, client) = self.clientServerSocket.accept()
                while True:
                    clientData = clientSocket.recv(1024)
                    if not clientData:
                        break
                    print(clientData)
                    self.proxyToServer.settimeout(15)

                    print(clientData.decode("utf-8"))

                    #Get host and port from GET message
                    splittedLines = clientData.decode("utf-8").splitlines();

                    #Loop through all objects and take Host
                    for elem in splittedLines:
                        if "Host" in elem:
                            host = splittedLines[1].split(" ")[1]
                            break

                    #Check if host contains port or should be default port 80
                    if ":" in host:
                        splitstring = host.split(":")
                        host = splitstring[0]
                        port = int(splitstring[1])
                    else:
                        port = 80
                    print("Host: ", host, "Port: ", port)
                    try:
                        self.proxyToServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        print("hello")
                        self.proxyToServer.connect((host, port))
                        print("din")
                    except socket.error as msg:
                        print("cant reconnect or connect to proxyToServer")

                    self.proxyToServer.send(clientData)
                    print("mamma")
                    recieved = self.proxyToServer.recv(1024)
                    clientSocket.send(recieved)

                self.proxyToServer.close()
                clientSocket.close()

        except socket.error as msg:
            print(msg)
            clientSocket.close()
            print("hej")
            self.proxyToServer.close()
            print("då")


if __name__ == "__main__":
    proxy = NetNinny()
    proxy.poll()