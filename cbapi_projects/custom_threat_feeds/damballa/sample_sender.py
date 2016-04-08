#!/bin/env python
# Client program

from socket import *

# Set the socket parameters
host = "localhost"
port = 20514
buf = 1024
addr = (host,port)

# Create socket
UDPSock = socket(AF_INET,SOCK_DGRAM)

# Send messages
with open ('example.txt','r') as infile:
    for line in infile:
        UDPSock.sendto(line,addr)

# Close socket
UDPSock.close()
