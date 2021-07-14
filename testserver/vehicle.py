import socket
from socketclient import socketclient

class vehicle:
    def __init__(self, name, pos, ip, port):
        self.name = name
        self.pos = pos
        self.socketclient = socketclient(ip, port)
    
    def connect(self):
        self.socketclient.connect()
    
    def close(self):
        self.socketclient.close()

    def getpos(self):
        return self.pos

    def getname(self):
        return self.name

    def sendmovecmd(self, target):
        msg = "MOVE," + target
        # print(msg)
        self.socketclient.send(msg)
        while True:
            msg = self.socketclient.listen()
            print("received message: ", msg)
            if msg.endswith('|'):
                resp = msg[:-1].split(',')
                if resp[0] == 'ENTER' and resp[1] == target:
                    print("vehicle %s reach point %s" %(self.name, target))
                    self.pos = target
                    return True
                else:
                    continue
            else:
                continue


if __name__ == "__main__":
    ip = socket.gethostname()
    v = vehicle("vehicle_0", 'A', ip, 2048)
    v.connect()
    v.sendmovecmd('B')
    v.close()