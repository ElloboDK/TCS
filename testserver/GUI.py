#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import threading
import tkinter as tk
from tkinter import ttk
from TCS import *

v0 = vehicle("vehicle_test", '25', socket.gethostname(), 2048)
v1 = vehicle("vehicle_0", '23', '192.168.1.98', 2048)
v2 = vehicle("vehicle_1", '24', '192.168.1.98', 2049)
v3 = vehicle("vehicle_2", '25', '192.168.1.98', 2050)
vt0 = vehicle("vehicle_test0", '23', "127.0.0.1", 2048)
vt1 = vehicle("vehicle_test1", '24', "127.0.0.1", 2049)
vt2 = vehicle("vehicle_test2", '25', "127.0.0.1", 2050)

# v0.connect()
# v1.connect()
# v2.connect()
# v3.connect()
vt0.connect()
vt1.connect()
vt2.connect()

GUI = tk.Tk()
GUI.title("Transport Control Center")
GUI.geometry("440x320")

Missionlist = ['mission_0', 'mission_1', 'mission_2']

def Vehicle1_button_onclick():
    # TCSvehicletomission(vt0, vehicle1_mission.get())
    # print(vehicle1_mission.get())
    thread1 = threading.Thread(target = TCSvehicletomission, args = (v1, vehicle1_mission.get()))
    thread1.start()

def Vehicle2_button_onclick():
    # TCSvehicletomission(vt1, vehicle2_mission.get())
    # print(vehicle2_mission.get())
    thread1 = threading.Thread(target = TCSvehicletomission, args = (v2, vehicle2_mission.get()))
    thread1.start()

def Vehicle3_button_onclick():
    # TCSvehicletomission(vt2, vehicle3_mission.get())
    # print(vehicle3_mission.get())
    thread1 = threading.Thread(target = TCSvehicletomission, args = (v3, vehicle3_mission.get()))
    thread1.start()

def test():
    pass

#车辆-1
# 任务选择
vehicle1 = tk.LabelFrame( GUI, text = "车辆-1", padx = 10, pady = 10 )  
vehicle1.place(x = 20, y = 20, width = 200)  

vehicle1_label = ttk.Label( vehicle1, text = "选择任务:" )
vehicle1_label.grid(column = 0, row = 0 )
 
# Vehiclelist = ['vehicle_0', 'vehicle_1', 'vehicle_2']

vehicle1_mission = tk.StringVar()
mission_list = ttk.Combobox(vehicle1, width = 12, textvariable = vehicle1_mission, state = 'readonly')
mission_list['values'] = [i for i in Missionlist]
mission_list.current(0)
mission_list.grid(column=1, row=0)

vehicle1_send = tk.LabelFrame( GUI, text = "", padx = 10, pady = 10 )  # 水平，垂直方向上的边距均为 10
vehicle1_send.place(x = 220, y = 30, width = 150)  # 定位坐标

Vehicle1_button = tk.Button( vehicle1_send, text = "发送任务", command = Vehicle1_button_onclick)
Vehicle1_button.pack(side='top', padx=10)

# 车辆-2
vehicle2 = tk.LabelFrame( GUI, text = "车辆-2", padx = 10, pady = 10 )  
vehicle2.place(x = 20, y = 120, width = 200)  

vehicle2_label = ttk.Label( vehicle2, text = "选择任务:" )
vehicle2_label.grid(column = 0, row = 0 )
 
vehicle2_mission = tk.StringVar()
mission_list = ttk.Combobox(vehicle2, width = 12, textvariable = vehicle2_mission, state = 'readonly')
mission_list['values'] = [i for i in Missionlist]
mission_list.current(0)
mission_list.grid(column=1, row=0)

vehicle2_send = tk.LabelFrame( GUI, text = "", padx = 10, pady = 10 )  # 水平，垂直方向上的边距均为 10
vehicle2_send.place(x = 220, y = 130, width = 150)  # 定位坐标

Vehicle2_button = tk.Button( vehicle2_send, text = "发送任务", command = Vehicle2_button_onclick)
Vehicle2_button.pack(side='top', padx=10)

# 车辆-3
vehicle3 = tk.LabelFrame( GUI, text = "车辆-3", padx = 10, pady = 10 )  
vehicle3.place(x = 20, y = 220, width = 200)  

vehicle3_label = ttk.Label( vehicle3, text = "选择任务:" )
vehicle3_label.grid(column = 0, row = 0 )
 
vehicle3_mission = tk.StringVar()
mission_list = ttk.Combobox(vehicle3, width = 12, textvariable = vehicle3_mission, state = 'readonly')
mission_list['values'] = [i for i in Missionlist]
mission_list.current(0)
mission_list.grid(column=1, row=0)

vehicle3_send = tk.LabelFrame( GUI, text = "", padx = 10, pady = 10 )  # 水平，垂直方向上的边距均为 10
vehicle3_send.place(x = 220, y = 230, width = 150)  # 定位坐标

Vehicle3_button = tk.Button( vehicle3_send, text = "发送任务", command = Vehicle3_button_onclick)
Vehicle3_button.pack(side='top', padx=10)



GUI.mainloop()