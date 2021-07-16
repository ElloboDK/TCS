#!/usr/bin/python3
# server.py

import socket
import time

serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

host = "127.0.0.1"
port = 2055

serversocket.bind((host, port))
serversocket.listen(5)

operationlist = ["LOAD", "UNLOAD"]

while True:
	clientsocket,addr = serversocket.accept()      
	print("connected: ",clientsocket)

	while True:
		msg = clientsocket.recv(1024).decode('utf-8')
		print ("receive: ", msg)
		msg = msg[:-1]
		if(msg == ""):
			break
		else:
			msg1 = msg.split(',')
			msg2 = ""
			if(msg1[0] == "MOVE"):
				msg2 = "ENTER," + msg1[-1] + "|"
			elif(msg1[0] == "ASK"):
				msg2 = "ENTER,23|"	
			elif(msg1[0] in operationlist):
				msg2 = "DONE|"

			time.sleep(1)
			clientsocket.sendall(bytes(msg2.encode('utf-8')))
			print ("send: ", msg2)


# while True:
# 	msg = "Hello world!" + "|"
# 	clientsocket.sendall(msg.encode('utf-8'))
# 	time.sleep(1)

# while True:
# 	msg = clientsocket.recv(1024).decode('utf-8')
# 	print (msg)