import socket
import threading
import time
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.link_prediction import within_inter_cluster
from vehicle import vehicle

# nodes = ['A', 'B', 'C', 'D', 'E', 'F']
# edges = [('A', 'B', 1), ('B', 'C', 3), ('C', 'D', 1), ('D', 'A', 3),
#         ('D', 'E', 1), ('E', 'F', 3), ('F', 'A', 1)]
    

nodes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
        '25', '26', '27', '28']

edges = [('02', '01', 3), ('03', '02', 3), ('04', '03', 3), ('05', '04', 3), ('06', '05', 3),
        ('02', '18', 6), ('18', '09', 6), ('03', '19', 6), ('19', '10', 6), 
        ('20', '04', 6), ('11', '20', 6), ('21', '05', 6), ('12', '21', 6), ('22', '06', 6), ('13', '22', 6), 
        ('01', '26', 2.5), ('26', '27', 3.5), ('27', '28', 3.5), ('28', '08', 2.5), 
        ('08', '07', 2), ('09', '08', 3), ('10', '09', 3), ('11', '10', 3), ('12', '11', 3), ('13', '12', 3), ('14', '13', 2), 
        ('07', '15', 2), ('15', '16', 10), ('16', '17', 9), ('17', '14', 2),
        ('26', '23', 2.5), ('23', '26', 2.5), ('24', '27', 2.5), ('27', '24', 2.5), ('25', '28', 2.5), ('28', '25', 2.5)]
        
missions = {'mission_0': ['22'], 
            'mission_1': ['21'],
            'mission_2': ['20']}

class TCS:
    nodevalue = [1]*len(nodes)
    edgevalue = [1]*len(edges)

    nodereachable = dict(zip(nodes,nodevalue))
    edgereachable = dict(zip(edges,edgevalue))

    def __init__(self, nodes = nodes, edges = edges):
        self.G = nx.DiGraph()
        self.G.add_nodes_from(nodes)
        self.G.add_weighted_edges_from(edges)
        
    def addvehicle(self, vehicle):
        pos = vehicle.getpos()
        self.nodereachable[pos] = 0

    def getpath(self, source, target):
        return nx.dijkstra_path(self.G, source = source, target = target)

    def sendmvcmd(self, vehicle, nextpos):
        curpos = vehicle.getpos()
        print("vehicle %s current position: %s" %(vehicle.getname(),curpos))
        # self.testprint()
        # 目标点被占用
        while(self.nodereachable[nextpos] != 1):
            time.sleep(1)
            print("vehicle", vehicle.getname(), "is waiting...")
        
        # 目标点空闲
        self.nodereachable[nextpos] = 0
        print("vehicle %s movement: %s -> %s" %(vehicle.getname(), curpos, nextpos))
        self.testprint()

        if(vehicle.sendmovecmd(nextpos) == True):
            self.nodereachable[curpos] = 1
            return True
        else:
            return False
    
    def gotopos(self, vehicle, target):
        source = vehicle.getpos()
        path = self.getpath(source, target)
        print("vehicle %s path: %s" %(vehicle.getname(), path))
        for x in path:
            if(x == source):
                continue
            if(self.sendmvcmd(vehicle, x) == True):
                continue
            else:
                break

    def testprint(self):
        print(self.nodereachable)
        # print(self.edgereachable)
        # print("node A:",self.nodereachable['A'])
        # print("node 02:",self.nodereachable['02'])

    def showmap(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, alpha=0.5)
        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels = labels)
        plt.show()

    def gomission(self, vehicle, mission):
        pass

def connect(v):
    print("vehicle %s is connecting" %v.getname())
    v.connect()
    print("vehicle %s is connected" %v.getname())

def close(v):
    print("vehicle %s is closing" %v.getname())
    v.close()
    print("vehicle %s is closed" %v.getname())

def TCSvehicletomission(vehicle, mission):
    tcs = TCS()
    tcs.addvehicle(vehicle)
    sourcepos = vehicle.getpos()
    for pos in missions[mission]:
        tcs.gotopos(vehicle, pos)
    tcs.gotopos(vehicle, sourcepos)

def TCSvehicle0():
    tcs = TCS()
    v = vehicle("vehicle_0", '25', socket.gethostname(), 2048)
    v.connect()
    tcs.addvehicle(v)
    while True:
        tcs.gotopos(v,'22')
        tcs.gotopos(v,'06')

def TCSvehicle1():
    tcs = TCS()
    v = vehicle("vehicle_0", '01', '192.168.1.98', 2048)
    v.connect()
    tcs.addvehicle(v)
    while True:
        tcs.gotopos(v,'09')
        tcs.gotopos(v,'01')

def TCSvehicle2():
    tcs = TCS()
    v = vehicle("vehicle_1", '05', '192.168.1.98', 2049)
    v.connect()
    tcs.addvehicle(v)
    while True:
        tcs.gotopos(v,'12')
        tcs.gotopos(v,'05')

def TCSvehicle3():
    tcs = TCS()
    v = vehicle("vehicle_2", '04', '192.168.1.98', 2050)
    v.connect()
    tcs.addvehicle(v)
    while True:
        tcs.gotopos(v,'11')
        tcs.gotopos(v,'04')

def ThreadTest():
    thread1 = threading.Thread(target = TCSvehicle1)
    thread2 = threading.Thread(target = TCSvehicle2)
    thread3 = threading.Thread(target = TCSvehicle3)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

def TCSvehicletest():
    v = vehicle("vehicle_0", '25', socket.gethostname(), 2048)
    v.connect()
    TCSvehicletomission(v, 'mission_0')
    v.close()

if __name__ == "__main__":
    # TCSvehicletest()
    # tcs = TCS()
    # tcs.showmap()
    TCSvehicle0()