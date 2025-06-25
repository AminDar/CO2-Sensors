# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
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


def initialize_mfc(port='COM3', slave_id=11):
    mfc = minbus.Instrument(port, slave_id, 'rtu', True, False)
    mfc.serial.baudrate = 9600
    mfc.serial.parity = serial.PARITY_NONE
    mfc.serial.timeout = 0.3
    mfc.serial.stopbits = 2
    return mfc

# Read an integer from one 16-bit register in the slave, possibly scaling it.

def create_csv_logger():
    t_start = datetime.now()
    t_start_str = t_start.strftime('%y%m%d_%H%M%S')
    file_path = f'Raw/MFC{t_start_str}.csv'
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
        writer.writerow(['Time', 'Gas Flow', 'Temp'])
    return file_path

def record_and_show(mfc, file, duration, interval, set_point):
    columns = ['Gas Flow', 'temp']
    data = []
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
        t_now = datetime.now()
        time_live.append(t_now)

        c += 1
        pd.DataFrame(data, columns=columns)

        if keyboard.is_pressed('s'):
            print('Step Down Started\n**************\n**************')
            mfc.write_float(6, 0.0)
            print(current_gas_flow)
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow([''] * 3)

        elif keyboard.is_pressed('u'):
            print('Step Up Started\n**************\n**************')
            mfc.write_float(6, set_point)
            print(current_gas_flow)

        elif keyboard.is_pressed('q'):
            print('Process is terminated\n**************\n**************')
            mfc.write_float(6, 0.0)
            exit()

        else:
            print('Hold S for step Down, U for step up, and Q for quit')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow([t_now, current_gas_flow, temp])

if __name__ == "__main__":
    if keyboard.is_pressed('q'):
        mfc = initialize_mfc()
        print("Gas Flow Controller is set to zero \nGas Flow Stopped\nStep Down started")
        mfc.write_float(6, 0.0)
        exit()

    mfc = initialize_mfc()
    file = create_csv_logger()
    record_and_show(mfc, file, 1150, 1, 2)