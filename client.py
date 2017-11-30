# Author: Jacob Cassity
import socket               # Import socket module
import getpass              # Imports getpass, used for hiding password
import os                   # Imports os, used for directory
import fnmatch
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

# Functions-----------------------------------------------
def get(filename):
    #opens a file with the given name
    f = open(filename, 'wb')
    data = s.recv(1024)
    # loops while there is something in data
    while data:
        print("Receiving data...")
        f.write(data)
        data = s.recv(1024)
    print("File received")
    # closes file
    f.close()

def put():
    filename = input("filename: ")
    # Sends name of file to server
    s.send(filename.encode())
    #if file is found then this code runs and sends 'File found' to server
    file = open((os.getcwd() + "\\" + filename), 'rb')
    data = file.read(1024)
    count = 1
    while (data):
        print("Sending data..." + str(count))
        s.send(data)
        count += 1
        data = file.read(1024)
    file.close()
    print("File Sent")
    # Error checking for file not found
    s.close()
def dir():
    # gets server's directory
    output = s.recv(1024).decode()
    return output

def localdir(pattern):
    # gets client directory
    fileList = os.listdir(os.getcwd())
    outputList = []
    output = ""
    if (pattern != " "):
        for file in fileList:
            if fnmatch.fnmatch(file, pattern):
                outputList.append(file)
    else:
        for file in fileList:
            outputList.append(file)
    for file in outputList:
        output += file + "\n"
    s.send(output.encode())
    return output
#----------------------------------------------------------------------
# checks id and password
while(authCheck == "0"):
    id = input("id: ")
    pw = getpass.getpass(prompt = "password: ")
    s.send(id.encode())
    s.send((pw.encode()))
    authCheck = s.recv(1024).decode()

choice = ""
while x:
    choice = input("Enter a command: ")
    # always checks choice as lower in case of capitalization errors from user.
    # Then it sends choice to server to act accordingly
    s.send(choice.lower().encode())
    if choice.lower() == "quit":
        x = False
    elif choice.lower() == "get":
        filename = input("filename: ")
        s.send(filename.encode())
        message = s.recv(1024).decode()
        # we close and reconnect when sending and receiving to avoid infinite loop problem
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
        # close and reconnect to avoid loop
        put()
        s = socket.socket()
        s.connect((host, port))
    elif choice.lower() == "cd":
        # Get's server's current working directory, changes it, and prints new one
        Jdirectory = s.recv(1024).decode()
        path = input(Jdirectory + "/")
        s.send(path.encode())
        print(s.recv(1024).decode())
    elif choice.lower() == "cd local":
        # Use os.getcwd to get the current working directory
        path = input(os.getcwd() + "\\")
        try:
            os.chdir(path)
            print(os.getcwd())
        except FileNotFoundError:
            # error checking in case the path is wrong
            print("Incorrect path")
    elif choice.lower() == "dir":
        # gets wild card (or lack thereof) and sends to server
        wildcard = input("")
        if wildcard == "":
            s.send(" ".encode())
        elif wildcard == "*" or "?":
            s.send(wildcard.encode())
        else:
            print("Invalid command")
        # server returns directory and prints it
        print(dir())
    elif choice.lower() == "mget":
        # initializes empty list for files
        fileList = []
        done = False
        while(not(done)):
            name = input("Enter command: ")
            if name.lower() == "done":
                done = True
            # checks for wild card
            elif name.__contains__("*") or name.__contains__("?"):
                s.send(name.encode())
                # creates temporary list from the directory recieved from server
                tempList = dir().splitlines()
                for file in tempList:
                    # Checks file matches given pattern. If so, add to fileList
                    if fnmatch.fnmatch(file, name):
                        fileList.append(file)
                for file in fileList:
                    # Loops through and receives files in fileList
                    get(file)
                    s.close()
                    s = socket.socket()
                    s.connect((host, port))
            else:
                print("Incorrect command")
            done = True
    elif choice.lower() == "mput":
        # Initializes fileList
        fileList = []
        done = False
        while(not(done)):
            name = input("Enter command or done: ")
            if name.lower() == "done":
                done = True
            # Checks for wild card
            elif name.__contains__("*") or name.__contains__("?"):
                #Makes list of files using the wild card and client directory
                fileList = localdir(name).splitlines()
                for file in fileList:
                    # sends each file in fileList
                    print(name)
                    f = open(file, "rb")
                    data = f.read(1024)
                    while(data):
                        print("Sending...")
                        s.send(data)
                        data = f.read(1024)
                    # closes connection then reopens it to avoid infinite loop
                    s.close()
                    s = socket.socket()
                    s.connect((host, port))
            else:
                print("Incorrect command")
            done = True
    else:
        print("Invalid command")
s.close()              # Close the socket when done