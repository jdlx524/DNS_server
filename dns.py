import socket
from dnsManager import dnsManager

port = 53
ip = "127.0.0.1"
# user will use that port to interpret DNS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))


while True:
    data, addr = sock.recvfrom(512)
    manager = dnsManager(data, "zones/")
    print(data)
    r = manager.build_response(data)
    print(r)
    sock.sendto(r, addr)
