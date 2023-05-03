# first of all import the socket library
import socket			



class server_boy:
    def __init__(self) -> None:
        # next create a socket object
        self.s = socket.socket()		

        # reserve a port on your computer in our
        port = 12343			

        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        self.s.bind(('', port))		
        print ("socket binded to %s" %(port))

        # put the socket into listening mode
        self.s.listen(5)	
        print ("socket is listening")	
    	
    def getConnection(self):
        self.c, addr = self.s.accept()	
        print ('Got connection from', addr )

    def sendHi(self):
        self.c.send('Thank you for connecting'.encode())

    def recvTest(self):
        print(self.c.recv(1024).decode())
        
    def close(self):
        self.s.close()
    # a forever loop until we interrupt it or
    # an error occurs
    # while True:

    #     # Establish connection with client.
        

    #     # send a thank you message to the client. encoding to send byte type.
    #     c.send('Thank you for connecting'.encode())

    #     # Close the connection with the client
    #     c.close()

    #     # Breaking once connection closed
    #  break
