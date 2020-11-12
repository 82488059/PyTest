# -*- coding: utf-8 -*-

import time
import socket
 

ip = '225.0.0.37'
port = 7776
 
def sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    while True:
        message = "{'type':'rdp'}"
        sock.sendto(message.encode(), (ip, port))
        print(message)
        time.sleep(1)
 
if __name__ == "__main__":
    sender()
