# Import socket module

import socket


class socky_boy:
    # Create a socket object
    def __init__(self) -> None:
        self.s = socket.socket()

        # Define the port on which you want to connect
        port = 12343
        # self.s.setblocking(0)
        # connect to the server on local computer
        self.s.connect(("10.5.108.240", port))

        # receive data from the server and decoding to get the string.
        print(self.s.recv(1024).decode())

    def sendTest(self):
        self.s.send("test".encode())

    def close(self):
        self.s.close()

    def sendMove(self, num):
        self.s.send((str(num[0] + ',' + str(num[1]))).encode())

    def awaitMove(self):
        return self.s.recv(1024).decode().split(',')
