#!/usr/bin/python3
# client.py

import socket
import sys
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

host = socket.gethostname() 
port = 2048

s.connect((host, port))

while True:
	msg = "Hello world!" + "|"
	s.sendall(msg.encode('utf-8'))
	time.sleep(1)

# while True:
# 	msg = s.recv(1024).decode('utf-8')
# 	print(msg)