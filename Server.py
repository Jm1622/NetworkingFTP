import socket
import re
commandSocket = socket.socket()
dataSocket = socket.socket()
host = '192.168.0.1'
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
    client.close()
