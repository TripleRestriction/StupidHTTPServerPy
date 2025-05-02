import socket
import sys

s = socket.socket()

if len(sys.argv) != 3:
    print("Usage webclient <hostname> <port>")
    exit(1)
s.connect((sys.argv[1], int(sys.argv[2])))
request = f"GET / HTTP/1.1\r\nHost:{sys.argv[1]}\r\nConnection: close\r\n\r\n"
s.sendall(request.encode('UTF-8'))
while True:
    d = s.recv(4096)
    if len(d) == 0:
        break
        s.close()
    print(d.decode())
