# -*- coding: utf-8 -*-
import struct
import time
import socket

ip = '225.0.0.37'
port = 7776
 
def receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))
    mreq = struct.pack("=4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq)
    while True:
        try:
            message, addr = sock.recvfrom(1024)
            print(message)
        except :
            print("error")

if __name__ == "__main__":
    receiver()
