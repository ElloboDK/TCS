# -*- coding: UTF-8 -*-

import socket
import time
import threading

class socketclient:

    def __init__(self, host = socket.gethostname(), port = 2048):
        self.s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        self.s.connect((self.host, self.port))
        
    def close(self):
        self.s.close()
            
    def send(self, msg):
        msg += "|"
        self.s.sendall(bytes(msg,'utf-8'))

    def keepsend(self, msg):
        while True:
            self.send(msg)
            time.sleep(1)

    def listen(self):
        return self.s.recv(1024).decode('utf-8')

    

if __name__ == "__main__":

    def keeplisten(socketclient):
        while True:
            print(socketclient.listen())
    

    s1 = socketclient('192.168.1.98', 2048)
    s1.connect()

    # t1 = threading.Thread(s1.keepsend("Hello world!"))
    # t1.start()
    # t2 = threading.Thread(target=keeplisten, args=s1)
    # t2.start()

    # while True:
        
    s1.send("TEST")

    print(s1.listen())

        
        