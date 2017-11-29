# Author: Jacob Cassity
import socket               # Import socket module
import getpass              # Imports getpass, used for hiding password
import os                   # Imports os, used for directory

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

# Functions
def get(filename):
    f = open(filename, 'wb')
    data = s.recv(1024)
    while data:
        print("Receiving data...")
        f.write(data)
        data = s.recv(1024)
    print("File received")
    f.close()

def put():
    filename = input("filename: ")
    s.send(filename.encode())
    try:
        file = open((os.getcwd() + "\\" + filename), 'rb')
        s.send('File found'.encode())
        data = file.read(1024)
        count = 1
        while (data):
            print("Sending data..." + str(count))
            s.send(data)
            count += 1
            data = file.read(1024)
        s.close()
        file.close()
        print("File Sent")
    except FileNotFoundError:
        print("File not found")
        s.send('File not found'.encode())

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
    elif choice.lower() == "get":
        filename = input("filename: ")
        s.send(filename.encode())
        message = s.recv(1024).decode()
        if message == "File found":
            get(filename)
            s.close()
            s = socket.socket()
            s.connect((host, port))
        else:
            print("File not found.")
            s.close()
            s = socket.socket()
            s.connect((host, port))
    elif choice.lower() == "put":
        put()
        s.close()
        s = socket.socket()
        s.connect((host, port))
    elif choice.lower() == "cd":
        Jdirectory = s.recv(1024).decode()
        path = input(Jdirectory + "/")
        s.send(path.encode())
        print(s.recv(1024).decode())
    elif choice.lower() == "cd local":
        path = input(os.getcwd() + "\\")
        try:
            os.chdir(path)
            print(os.getcwd())
        except FileNotFoundError:
            print("Incorrect path")

    else:
        print("Invalid command")
s.close              # Close the socket when done