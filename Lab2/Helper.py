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
                #Set default port in case no other is declared
                port = 80
                print("Before accept")
                (clientSocket, client) = self.clientServerSocket.accept()
                clientData = clientSocket.recv(1024)
                print(clientData)
                self.proxyToServer.settimeout(15)

                print(clientData.decode("utf-8"))

                #Get host and port from GET message
                splittedLines = clientData.decode("utf-8").splitlines();

                #Loop thorugh all objects and take Host
                for elem in splittedLines:
                    if "Host" in elem:
                        host = splittedLines[1].split(" ")[1]
                        break

                #Check if host contains port
                if ":" in host:
                    splitstring = host.split(":")
                    host = splitstring[0]
                    port = splitstring[1]

                print("Host: ", host, "Port: ", port)
                self.proxyToServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.proxyToServer.connect((host, int(port)))

                self.proxyToServer.send(clientData)

                recieved = self.proxyToServer.recv(1024)
                clientSocket.send(recieved)

                self.proxyToServer.close()
                #clientSocket.close()

        except socket.error as msg:
            print(msg)
            self.clientServerSocket.close()
            self.proxyToServer.close()


if __name__ == "__main__":
    proxy = NetNinny()
    proxy.poll()