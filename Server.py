import socket
s = socket.socket()
host = '192.168.2.8'
print(socket.gethostname())
port = 12345
x = "Got you babe"
s.bind((host, port))
s.listen(5)
while True:
    c, addr = s.accept()
    print("Connected to other machine!")
    c.send(x.encode())
    c.close()