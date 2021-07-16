#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import uuid
import json
import time
import copy
import threading

from requests.models import parse_url

# HTTP TransportOrder
class HttpTpo:

    def __init__(self):
        """初始化"""

        self.vehicles = self.getvehicles()
        self.vehicles.sort()
        self.vehicleloaded = [0 for col in range(len(self.vehicles))]
        self.startpos = self.getvehiclesstartpos()
        self.storelist = [
            ["Store-0004", "Store-0003", "Store-0002", "Store-0001"],
            ["Store-0008", "Store-0007", "Store-0006", "Store-0005"],
            ["Store-0012", "Store-0011", "Store-0010", "Store-0009"]
        ]
        self.workpos = ["1", "2", "3", "4"]
        self.posmap = [
            ["38", "46", "45", "44", "43", "34"],
            ["37", "54", "53", "52", "51", "33"],
            ["36", "62", "61", "60", "59", "32"],
            ["35", "71", "70", "69", "68", "31"]
        ]
        self.loadlist = [[[0 for x in range(4)]for y in range(4)]for z in range(3)]
        for i in range(0, 2):
            for j in range(0, 4):
                self.loadlist[0][i][j] = 1

    def getuuid(self) -> str:
        """获取uuid"""
        return str(uuid.uuid4()).replace("-", "")

    def gethttpmsg(self, msg) -> dict:
        """发送get请求"""
        url = "http://127.0.0.1:55200/v1/" + msg
        r = requests.get(url)
        msg = str(r.content, 'utf-8')
        text = json.loads(msg)
        return text

    def gettransportOrders(self):
        """获取所有订单数据"""
        return self.gethttpmsg("transportOrders")

    def gettransportOrdersbyUUID(self, uuid):
        """通过uuid获取指定订单数据"""
        return self.gethttpmsg("transportOrders/" + uuid)

    def gettpostatusbyUUID(self, uuid):
        """获取指定订单的状态"""
        return self.gettransportOrdersbyUUID(uuid)['state']

    def canceltpobyUUID(self, uuid):
        """取消指定订单"""
        url = "http://127.0.0.1:55200/v1/transportOrders/" + uuid + "/withdrawal"
        headers = {'Content-Type': 'application/json'}
        # data = self.gettpo(vehicle, poslist)
        r = requests.post(url, headers = headers)
        print(r.status_code, r.content)
        return r

    def cancelalltpo(self):
        """取消所有订单"""
        orders = self.gettransportOrders()
        rlist = []
        for order in orders:
            if(order["state"] == "BEING_PROCESSED" or order["state"] == "DISPATCHABLE"):
                r = self.canceltpobyUUID(order["name"])
                print(r.status_code, r.content)
                rlist.append(r)
        return rlist
        
    def getvehiclesinfo(self):
        """获取所有车辆信息"""
        return self.gethttpmsg("vehicles")

    def getonevehicleinfo(self, vehicle):
        """获取指定车辆信息"""
        return self.gethttpmsg("vehicles/" + vehicle)
    
    def getonevehiclestartpos(self, vehicle):
        """获取指定车辆的起点"""
        msg = self.getonevehicleinfo(vehicle)
        return msg["properties"]["StartPos"]

    def getvehiclesstartpos(self):
        """获取所有车辆的起点"""
        startpos = []
        for vehicle in self.vehicles:
            startpos.append(self.getonevehiclestartpos(vehicle))
        return startpos

    def ifvehicleIDLE(self, vehicle):
        """判断车辆是否是闲置状态"""
        return self.getonevehicleinfo(vehicle)["state"] == "IDLE"

    def getvehicles(self):
        """获取车辆信息至本地"""
        msgs = self.getvehiclesinfo()
        vehicles = []
        for msg in msgs:
            vehicles.append(msg["name"])
        return vehicles
    
    def getcmd(self, pos, op, prop = []):
        """获取需要发送的任务信息"""
        return {
            "locationName": pos,
            "operation": op,
            "properties": prop
        }

    def getmovecmd(self, pos):
        """获取去指定地点的移动任务"""
        return self.getcmd(pos, "MOVE")

    def getmovecmdlist(self, poslist):
        """获取去指定地点的移动任务列表"""
        mvlist = []
        for pos in poslist:
            mvlist.append(self.getmovecmd(pos))
        return mvlist

    def getloadcmd(self, pos, j):
        """获取去指定地点的装货任务"""
        prop = [{
            "key" : "worklocationnum",
            "value" : j
        }]
        return self.getcmd(pos, "LOAD", prop)

    def getunloadcmd(self, pos, j):
        """获取去指定地点的卸货任务"""
        prop = [{
            "key" : "worklocationnum",
            "value" : j
        }]
        return self.getcmd(pos, "UNLOAD", prop)

    def gettpodata(self, vehicle, cmdlist):
        """获取运输订单数据"""
        data = {
            "deadline": "2022-05-17T06:42:40.396Z", #deadline需要修改
            "intendedVehicle": vehicle,
            "destinations": []
        }
        for cmd in cmdlist:
            data["destinations"].append(cmd)
        return data

    def sendtpo(self, vehicle, cmdlist):
        """发送运输订单"""
        uuid = self.getuuid()
        url = "http://127.0.0.1:55200/v1/transportOrders/" + uuid
        headers = {'Content-Type': 'application/json'}
        data = self.gettpodata(vehicle, cmdlist)
        print(data)
        r = requests.post(url, data = json.dumps(data), headers = headers)
        print(r.status_code, r.content)
        return (r, uuid)

    def sendallvehicletpo(self, cmdlist):
        """给所有车辆发送同一运输订单"""
        rlist = []
        for vehicle in self.vehicles:
            r = self.sendtpo(vehicle, cmdlist)
            rlist.append(r)
        return rlist

    def sendallvehiclepos(self, pos):
        """给所有车辆发送去同一点位的订单"""
        cmdlist = [self.getmovecmd(pos)]
        self.sendallvehicletpo(cmdlist)

    def sendallvehiclestartpos(self):
        """给所有车辆发送返回出发点的运输订单"""
        for i in range(len(self.vehicles)):
            self.sendtpo(self.vehicles[i], self.getmovecmdlist([self.startpos[i]]))

    def reset(self):
        """取消所有订单，并让车辆返回起点
        
        只能重置订单和车辆位置，不能重置车辆属性（loaded）
        """
        self.cancelalltpo()
        self.sendallvehiclestartpos()

    def getloadpos(self, row):
        """获取装货点位"""
        for i in range(0, 4):
            for j in range(0, 4):
                if(self.loadlist[row][i][j] == 1):
                    return (i ,j)
 
    def getunloadpos(self, row):
        """获取卸货点位"""
        for i in range(0, 4):
            for j in range(0, 4):
                if(self.loadlist[row][i][j] == 0):
                    return (i ,j)

    def sendvehicleloadtpoobo(self, row1, row2):
        """逐一对车辆发送装货订单
        
        前一辆车辆完成装货任务并到达outpos点，才对后一辆车辆发送订单

        row1 :  装货行号
        row2 :  后续卸货行号
        """
        for i in range(0, len(self.vehicles)):
            (j, k) = self.getloadpos(row1)
            cmdlist = []
            cmdlist.append(self.getloadcmd(self.storelist[row1][j], k))
            cmdlist.append(self.getmovecmd(self.posmap[row1][j]))

            while True:
                if(self.ifvehicleIDLE(self.vehicles[i]) and self.vehicleloaded[i] == 0):
                    break
                else:
                    time.sleep(1)

            (r, uuid) = self.sendtpo(self.vehicles[i], cmdlist)
            while True:
                status = self.gettpostatusbyUUID(uuid)
                print(uuid, status)
                if(status == "FINISHED"):
                    self.loadlist[row1][j][k] = 0
                    cmdlist = []
                    cmdlist.append(self.getmovecmd(self.posmap[row1][0]))
                    cmdlist.append(self.getmovecmd(self.posmap[row2][0]))
                     
                    # cmdlist.append(self.getmovecmd(self.startpos[i]))

                    self.sendtpo(self.vehicles[i], cmdlist)
                    self.vehicleloaded[i] = 1

                    break
                else:
                    time.sleep(1)

    def sendvehicleunloadtpoobo(self, row1):
        """逐一对车辆发送卸货订单
        
        只有当车辆空闲且装货了才会发送订单
        前一辆车辆完成卸货任务并到达outpos点，才对后一辆车辆发送订单

        outpos : 完成任务出来点位
        nextpos : 任务结束后的下一点位
        """
        for i in range(0, len(self.vehicles)):
            (j, k) = self.getunloadpos(row1)
            cmdlist = []
            cmdlist.append(self.getunloadcmd(self.storelist[row1][j], k))
            cmdlist.append(self.getmovecmd(self.posmap[row1 + 1][j + 2]))
            
            while True:
                if(self.ifvehicleIDLE(self.vehicles[i]) and self.vehicleloaded[i] == 1):
                    break
                else:
                    time.sleep(1)

            (r, uuid) = self.sendtpo(self.vehicles[i], cmdlist)

            while True:
                status = self.gettpostatusbyUUID(uuid)
                if(status == "FINISHED"):
                    self.loadlist[row1][j][k] = 1
                    self.vehicleloaded[i] = 0

                    cmdlist = []
                    cmdlist.append(self.getmovecmd(self.posmap[row1 + 1][-1]))
                    cmdlist.append(self.getmovecmd(self.startpos[i]))
                    self.sendtpo(self.vehicles[i], cmdlist)

                    break
                else:
                    time.sleep(1)

    def test(self):
        pass

if __name__ == '__main__':
    # 基础订单格式
    ###########################################################################
    
    url = "http://127.0.0.1:55200/v1/transportOrders/" + str(uuid.uuid4()).replace("-", "")

    data = {
        "deadline": "2022-05-17T06:42:40.396Z",
        "intendedVehicle": "Vehicle-0001",
        "destinations": [{
            "locationName": "34",
            "operation": "MOVE",
            "properties": []
        },{
            "locationName": "33",
            "operation": "MOVE",
            "properties": []
        }]
    }

    headers = {'Content-Type': 'application/json'}

    # 发送任务
    # r = requests.post(url, data = json.dumps(data), headers = headers)
    # print(r.status_code, r.content)

    ###########################################################################

    httptpo = HttpTpo()

    # httptpo.sendallvehiclepos("43")
    # httptpo.sendvehicleloadtpoobo(0, 3)

    # httptpo.sendallvehiclepos("42")
    # httptpo.sendallvehiclepos("35")
    # httptpo.sendvehicleunloadtpoobo(2)

    httptpo.sendallvehiclepos("34")

    thread1 = threading.Thread(target = httptpo.sendvehicleloadtpoobo, args = [0, 3])
    thread2 = threading.Thread(target = httptpo.sendvehicleunloadtpoobo, args = [2])
    
    thread1.start()
    thread2.start()

    # httptpo.sendallvehiclestartpos

    # httptpo.reset()

    # httptpo.test()
