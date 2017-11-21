import socket
import re
import os
commandSocket = socket.socket()
dataSocket = socket.socket()
directory = "/Users/jmartin/PycharmProjects/NetworkingFTP/FTP Dir/"
#host = '192.168.0.1'
host = '192.168.2.14'
#
port = 12345
commandSocket.bind((host, port))
commandSocket.listen(5)

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
            fileName = client.recv(1024).decode()
            try:
                file = open((directory + fileName), 'rb')
                client.send('File found'.encode())
                data = file.read(1024)
                count = 1
                while (data):
                    print("Sending data..."+str(count))
                    client.send(data)
                    count += 1
                    data = file.read(1024)
                client.shutdown(socket.SHUT_WR)
                client.close
                file.close()
                commmandSocket = socket.socket()
                commandSocket.bind((host, port))
                commandSocket.listen(5)
                client, addr = commandSocket.accept()
                print("File Sent")
            except FileNotFoundError:
                client.send('File not found'.encode())
        directory = "/Users/jmartin/PycharmProjects/NetworkingFTP/FTP Dir/"

    client.close()
