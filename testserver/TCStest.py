from TCS import TCS
from vehicle import vehicle
import socket
import threading

def v1():
    tcs = TCS()
    v1 = vehicle("vehicle_0", '01', socket.gethostname(), 2048)
    v1.connect()
    tcs.addvehicle(v1)
    tcs.gotopos(v1,'02')


def v2():
    tcs = TCS()
    v1 = vehicle("vehicle_1", '02', socket.gethostname(), 2048)
    v1.connect()
    tcs.addvehicle(v1)
    tcs.gotopos(v1,'03')

if __name__ == "__main__":

    thread1 = threading.Thread(target = v1)
    thread2 = threading.Thread(target = v2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()