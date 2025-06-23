# -*- coding: utf-8 -*-
"""
@author: Amin Darbandi
aathome@duck.com
For HRI
"""

import serial
import minimalmodbus as minbus
import numpy as np
import pandas as pd
import time as t
import matplotlib.pyplot as plt
from datetime import date, time, datetime, timedelta
import csv
from sys import exit
import keyboard


mfc = minbus.Instrument('COM3', 11, 'rtu', True, False)
mfc.serial.baudrate = 9600
mfc.serial.parity = serial.PARITY_NONE
mfc.serial.timeout = 0.3
mfc.serial.stopbits = 2

# Read an integer from one 16-bit register in the slave, possibly scaling it.


if keyboard.is_pressed('q'):
    print("Gas Flow Controller is set to zero \n Gas Flow Stopped"
          "\n Step Down started")
    mfc.write_float(6, 0.0)
    exit()

columns = ['Gas Flow', 'temp']
data = []
t_start = datetime.now()
t_start_str = t_start.strftime('%y%m%d_%H%M%S')  # string object

file = 'Raw_MFC/MFC ' + str(t_start_str) + '.csv'
with open(file, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
    writer.writerow(['Time', 'Gas Flow', 'Temp'])

def record_and_show(duration, interval, set_point):

    set_point = float(set_point)
    if set_point > 9:
        print('Set point is over threshold. Try again')
        exit()
    else:
        mfc.write_float(6, set_point)

    time_live = []
    MeasureTime = duration * 60 / interval
    c = 0
    data_live1 = []
    data_live2 = []

    while c <= MeasureTime:
        current_gas_flow = mfc.read_float(0)
        temp = round(mfc.read_float(2), 4)
        data.append([current_gas_flow, temp])
        data_live1.append(current_gas_flow)
        data_live2.append(temp)
        # t.sleep(interval)
        t_now = datetime.now()  # current time stamp
        time_live.append(t_now)

        # Plot the gas flow
        # plt.legend(['Gas Flow'], loc='center', bbox_to_anchor=(0.8, 0.8))
        # plt.xticks(rotation=45)
        # plt.plot(time_live, data_live1, color='red')
        # plt.draw()
        # plt.pause(1)

        c += 1
        pd.DataFrame(data, columns=columns)
        # Add recorded and calculated data to csv file
        if keyboard.is_pressed('s'):
            print('Step Down Stated'
                  '\n **************'
                  '\n **************')
            mfc.write_float(6, 0.0)
            print(current_gas_flow)
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow('\n')
                csv_file.close()

        elif keyboard.is_pressed('u'):
            print('Step Up Stated'
                  '\n **************'
                  '\n **************')
            mfc.write_float(6, set_point)
            print(current_gas_flow)

        elif keyboard.is_pressed('q'):
            print('Process is terminated'
                  '\n **************'
                  '\n **************')
            mfc.write_float(6, 0.0)
            exit()

        else:
            print(f'Hold S for step Down, Hold U for step up and Q for quit')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow([t_now, current_gas_flow, temp])
                csv_file.close()


record_and_show(1150, 1, 2)
