# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 11:40:17 2021

@author: Amin Darbandi
"""

import serial
import minimalmodbus as minbus
import numpy as np
import pandas as pd

import os
import time as t
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import datetime
from datetime import date, time, datetime, timedelta
import csv 
from sys import exit
import keyboard

mfc = minbus.Instrument('COM4',11,'rtu',True,False)
mfc.serial.baudrate =9600
mfc.serial.parity   = serial.PARITY_NONE
mfc.serial.timeout  = 0.3
mfc.serial.stopbits  = 2

#Read an integer from one 16-bit register in the slave, possibly scaling it.

duration = float(input('Measuremnt Duration in min: '))
#Measure every 10s
interval = 10
# Create array of measuremnet time including stop
MeasureArray = np.arange(0,duration*60+interval,interval)

# Set point of gas flow 
setpoint =  float(input('Gas flow in l/min (max 25l/min): '))
if setpoint >60:
   print ('Set point is over treshhold. Try again')
   exit()
else:
    mfc.write_float(6, setpoint)

data = []
c = 0
# while c <= duration*60:
#     current_gas_flow = mfc.read_float(0)
#     temp = mfc.read_float(2)
#     data.append([current_gas_flow,temp])
#     c += 1
#     t.sleep(interval)
# else:
#     # Set the setpoint to 0
#     mfc.write_float(6, 0)
      
columns=['Gas Flow','temp']
# df = pd.DataFrame(data,columns=columns)

t_start = datetime.now()
t_start_str = t_start.strftime('%y%m%d_%H%M%S') # string object

file = 'MFC '+str(t_start_str)+'.csv'
with open(file,'w') as csv_file: 
    writer=csv.writer(csv_file, delimiter=';',lineterminator='\r')
    writer.writerow(['Time','Gas Flow', 'Temp'])

# Empty lists for live visualisation
time_live = []

def record_and_show(duration, interval): 
    
    MeasureTime = duration*60/interval
    c = 0
    data_live1 =[]
    data_live2 =[]
    while c <= MeasureTime:
        
            current_gas_flow = mfc.read_float(0)
            temp = round(mfc.read_float(2),4)
            data.append([current_gas_flow,temp])
            data_live1.append(current_gas_flow)
            data_live2.append(temp)
            t.sleep(interval)
            t_now = datetime.now() # current time stamp
            time_live.append(t_now)
            # Settings for plot
            plt.cla() # clear current figure
            plt.rcParams['figure.figsize'] = [10, 8]
            plt.rcParams['figure.dpi'] = 300
            plt.plot(time_live,data_live1 , label = 'Gas Flow' )
            # plt.plot(time_live,data_live2 , label = 'Temp' )
           
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.show()
            c +=1
            pd.DataFrame(data,columns=columns)
            # Add recorded and calculated data to csv file
            if keyboard.is_pressed('q'):
                print ("Gas Flow Controller is set to zero \n Gas Flow Stopped"
                       "\n Step Down started")
                mfc.write_float(6, 0.0)
                exit()
            
            else:
                with open(file,'a') as csv_file: 
                    writer=csv.writer(csv_file, delimiter=';',lineterminator='\r')
                    writer.writerow([t_now,current_gas_flow,temp])

    
fig = plt.figure()
from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, record_and_show, frames = 6000, repeat = False)
record_and_show(duration,interval)

df=pd.DataFrame(data,columns=columns)
