# Author: Jacob Cassity
import socket               # Import socket module
import getpass              # inports getpass, used for hiding password

s = socket.socket()         # Create a socket object
t = socket.socket()
#host = '192.168.0.1'        # ethernet ip address
#host = '192.168.2.8' # Jeremy's ip at dorm
#host = socket.gethostname() #Testing on my own machine.
port = 12345         # Reserve a port
x = True
host = input("Enter ip address: ")     # sets host to ip address
s.connect((host, port))
authCheck = "0"               # Server will check user name and password and return 0 if incorrect.
while(authCheck == "0"):
    id = input("id: ")
    pw = getpass.getpass(prompt = "password: ")
    s.send(id.encode())
    s.send((pw.encode()))
    authCheck = s.recv(1024).decode()

choice = ""
while x:
    choice = input("Enter a command: ")
    s.send(choice.lower().encode())
    if choice.lower() == "quit":
        x = False
    else:
        print("Invalid command")
s.close              # Close the socket when done