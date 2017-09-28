# Author: Jacob Cassity
import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '192.168.0.1'        # ethernet ip address
#host = '192.168.2.8' # Jeremy's ip at dorm
#host = socket.gethostname() #Testing on my own machine.
port = 12345         # Reserve a port
x = True
choice = 0
s.connect((host, port))
print (s.recv(1024).decode())
while x:
    choice = input(
        "Choose an option:" + "\n" +
        "1: blah" + "\n" +
        "2: blah" + "\n" +
        "3: blah" + "\n" +
        "4: quit" + "\n" +
        "Enter:  "
    )
    s.send(choice.encode())
    if choice == '1':
        print("placeholder 1")
    elif choice == '2':
        print("Placeholder 2")
    elif choice == '3':
        print("placeholder 3")
    elif choice == '4':
        print("Quitting")
        x = False
    else:
        print("Invalid option, please try again")

s.close              # Close the socket when done