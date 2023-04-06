import socket

port = 53
ip = "127.0.0.1"
# user will use that port to interpret DNS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

while True:
    data, addr = sock.recvfrom(512)
    print('Transaction ID:', data[0:2])
    sock.sendto(data[:2], addr)
