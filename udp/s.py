#!/usr/bin/env python 
# -*- coding:UTF-8 -*-
# UDP广播发送
from socket import *

HOST = '192.168.3.255'
PORT = 6681
BUFSIZE = 1024
 
ADDR = (HOST, PORT)

broadcast = socket(AF_INET, SOCK_DGRAM)
broadcast.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    data = raw_input('>')
    if not data:
        break
    print("send: %s"%data)
    broadcast.sendto(data, ADDR)
 
broadcast.close()
