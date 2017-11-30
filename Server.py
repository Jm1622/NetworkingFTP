import socket
import re
import os
import fnmatch
#set up the commandSocket (the server) and the client socket
commandSocket = socket.socket()
client = socket.socket()
host = '192.168.0.1'

port = 12345
commandSocket.bind((host, port))
commandSocket.listen(5)

#a function used to get a file, download
def get(fileName):
    try:
        file = open((os.getcwd() + "/"+fileName), 'rb')
        client.send('File found'.encode())
        print("File "+fileName +" found")
        data = file.read(1024)
        count = 1
        while (data):
            print("Sending data..." + " Packet # "+str(count))
            client.send(data)
            count += 1
            data = file.read(1024)
        print("File "+fileName+" Sent")
        file.close()

    except FileNotFoundError:
        client.send('File not found'.encode())



#function for put, used to upload a file
def put(filename):
    f = open(filename, 'wb')
    data = client.recv(1024)
    count = 1
    while data:
        print("Receiving data..."+ " packet #"+str(count))
        f.write(data)
        count += 1
        data = client.recv(1024)
    print("File "+fileName+" received")
    f.close()

#returns the files at a certain location with support for searching for a type
#if they give us nothing we'll return all files, if they give us a pattern only add it if it matches the pattern
def dir(pattern):
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
    client.send(output.encode())
    return output
#receives info from the client's dir
def putDir():
    return client.recv(1024).decode()

while True:
    #build connection to client and set up code
    command = ""
    authenticationLoop = 1
    client, addr = commandSocket.accept()
    print("Connected to other machine!")
    #while they have not authenticated receive a username and password, let them know when they pass and repeat if they've failed
    while authenticationLoop == 1:
        id = client.recv(1024).decode()
        password = client.recv(1024).decode()
        print("Username: "+id + ' ' + "Password: "+password)
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', password)
        if match:
            client.send('1'.encode())
            authenticationLoop = 0
            print('User logged in')
        else:
            client.send('0'.encode())
            print('User failed to log in')
    #Once authenticated keep taking commands until quit
    while command != 'quit':
        command = client.recv(1024).decode()
        if command == 'get':
            #get the fileName and then call get, whenever we have a loop with recv we have to close and reopen the connection
            #The closing and reopening is transparent to the user
            fileName = client.recv(1024).decode()
            get(fileName)
            client.close()
            client, addr = commandSocket.accept()

        elif command == 'put':
            #if command is put get the fileName from user
            fileName = client.recv(1024).decode()
            #Call put if the file exists on his side
            put(fileName)
            #close and reopen the connection
            client.close()
            client, addr = commandSocket.accept()
        elif command == "cd":
            #for cd send the current path and receive the new path
            #then set the working directory to new path
            #if this fails we send the client that it failed and print failed to change
            try:
                client.send((os.getcwd()).encode())
                newPath = client.recv(1024).decode()
                os.chdir(newPath)
                print("New working path: "+os.getcwd())
                client.send(("Directory changed to "+os.getcwd()).encode())
            except FileNotFoundError:
                client.send("Path not changed".encode())
                print("Directory failed to change")

        elif command == "dir":
            #receive the pattern the user wants to search for in dir
            #call dir
            pattern = client.recv(1024).decode()
            print("The following directory info was sent: "+dir(pattern))

        elif command == "mget":
            #check that they give us a name with a wildcard then find all the files in this list
            name = ""
            name = client.recv(1024).decode()
            if (name.__contains__('*') or name.__contains__('?')):
                fileList = dir(name).splitlines()
                print(fileList)
                for file in fileList:
                    #send these files one at a time
                    print(file)
                    try:
                        f = open((os.getcwd() + "/" + file), 'rb')
                        print("File found: "+file)
                        data = f.read(1024)
                        count = 1
                        #loop until we stop receiving data
                        while (data):
                            print("Sending data..." + " packet #"+str(count))
                            client.send(data)
                            count += 1
                            data = f.read(1024)
                        print("File "+file+" Sent")
                        f.close()

                    except FileNotFoundError:
                        print("File "+ file + " not found")
                    client.close()
                    client, addr = commandSocket.accept()

        elif command == "mput":
            #receive the filenames from the client
            fileList = putDir().splitlines()
            for file in fileList:
                #open each file and then receive the data from client and recreate the file
                data = client.recv(1024)
                f = open(file, "wb")
                count = 1
                while(data):
                    print("Receiving... packet #"+str(count))
                    f.write(data)
                    data = client.recv(1024)
                    count += 1
                f.close()
                client.close()
                client, addr = commandSocket.accept()
                print("File "+file+" sent")



    #when the session ends write a message and close the client
    print("Session closed")
    client.close()
