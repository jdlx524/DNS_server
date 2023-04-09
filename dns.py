import sys
import socket
from dnsManager import dnsManager

port = 53
ip = "127.0.0.1"
# user will use that port to interpret DNS
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

if __name__ == "__main__":
    while True:  # can be improved by adding another thread to control the socket
        data, addr = sock.recvfrom(512)
        manager = dnsManager(data, "zones/")
        sys.stdout.buffer.write(data)  # use this to output like in wireshark
        r = manager.build_response()
        sys.stdout.buffer.write(r)
        # exit()
        sock.sendto(r, addr)
