import socket
s = socket.socket()
host = '192.168.0.1'
print(socket.gethostname())
port = 12345
x = "Got you babe"
potato = True
s.bind((host, port))
s.listen(5)
command = ""
while True:
    c, addr = s.accept()
    print("Connected to other machine!")
    c.send(x.encode())
    while command != "4":
        command = c.recv(1024).decode()
        print(command)
    c.close()
    command = ""