# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 16:20:48 2022

@author: P278601
"""

import time
import pyvisa
import pandas as pd
from pylablib.devices import Thorlabs, Andor  # import the device libraries
import numpy as np  # import numpy for saving
import serial
import matplotlib.pyplot as plt


stage = Thorlabs.ElliptecMotor("COM6")
# print(stage.get_default_addr())
stage.move_to(0)
time_start = time.time()

for i in range(2):
    stage.move_to((10*i)%360)
stage.move_to(355)
stage.move_to(0)
# stage.close()

plt.ion()
fig=plt.figure()

i=0
ser = serial.Serial('COM5',115200)
ser.close()
ser.open()
data = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
plotdatax = []
plotdatay = []

angle = []
avarage_intensity = []
try:
    for j in range(358):    #change to 355      
        stage.move_by(1)
        #time.sleep(1)
        angle.append((j))
        intensity = 0
        for i in range(10):
            
            data = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
            plotdatay.append(data)
            # i += 1
            plotdatax.append(time.time()-time_start)
            #time.sleep(0.5)
            
            intensity = intensity + data
            plt.pause(0.0001)
        avint= intensity /10
        avarage_intensity.append(intensity)
        plt.title('serial reader: ' + str(data), loc='left')
        plt.plot(plotdatax,plotdatay, 'og') # pyplot will add this data
            # plt.show() # update plot
        plt.pause(0.0001) # pause
        #time.sleep(0.5)
        plt.show() # update plot
    ser.close()
    print("loop finished")
    dict = {"Angle":angle, "avarage_intensity":avarage_intensity}
    df = pd.DataFrame(dict)
    df.to_csv("RF336_Rcell_4_980nm.csv")
    stage.close()
    plt.close()
except KeyboardInterrupt:
    ser.close()
    print("serial connection closed")
    stage.close()
    plt.close()       
  
