import socket
import re
import os
commandSocket = socket.socket()
client = socket.socket()
host = '192.168.0.1'
#host = '192.168.2.14'

port = 12345
commandSocket.bind((host, port))
commandSocket.listen(5)

def get():
    fileName = client.recv(1024).decode()
    try:
        file = open((os.getcwd() + "/"+fileName), 'rb')
        client.send('File found'.encode())
        data = file.read(1024)
        count = 1
        while (data):
            print("Sending data..." + str(count))
            client.send(data)
            count += 1
            data = file.read(1024)
        print("File Sent")
        file.close()
    except FileNotFoundError:
        client.send('File not found'.encode())


def put(filename):
    f = open(filename, 'wb')
    data = client.recv(1024)
    while data:
        print("Receiving data...")
        f.write(data)
        data = client.recv(1024)
    print("File received")
    f.close()



while True:
    command = ""
    authenticationLoop = 1
    client, addr = commandSocket.accept()
    print("Connected to other machine!")
    while authenticationLoop == 1:
        id = client.recv(1024).decode()
        password = client.recv(1024).decode()
        print(id + ' ' + password)
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', password)
        if match:
            client.send('1'.encode())
            authenticationLoop = 0
            print('Passed')
        else:
            client.send('0'.encode())
            print('Failed')
    while command != 'quit':
        command = client.recv(1024).decode()
        if command == 'get':
            get()
            client.close()
            client, addr = commandSocket.accept()
        if command == 'put':
            fileName = client.recv(1024).decode()
            message = client.recv(1024).decode()
            if message == "File found":
                put(fileName)
            else:
                print("File not found")
            client.close()
            client, addr = commandSocket.accept()
        if command == "cd":
            try:
                client.send((os.getcwd()).encode())
                newPath = client.recv(1024).decode()
                os.chdir(newPath)
                print("New working path: "+os.getcwd())
                client.send(("Directory changed to "+os.getcwd()).encode())
            except FileNotFoundError:
                client.send("Path not changed".encode())
                print("Directory failed to change")
    print("Session closed")
    client.close()
