# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

import csv
from datetime import datetime
import json
import keyboard
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_co2_v2 import BrickletCO2V2

HOST = "localhost"
PORT = 4223
UID_S1 = 'VYU'
UID_S2 = 'VYV'
UID_S3 = '21kv'
UID_S4 = 'VZ2'

def record_and_show(duration, interval, file, columns, data, time_live):
    MeasureTime = duration * 60 / interval
    c = 0
    data_live1, data_live2, data_live3, data_live4 = [], [], [], []

    plt.rcParams['figure.figsize'] = [8, 4]
    plt.rcParams['figure.dpi'] = 100

    while c <= MeasureTime:
        co2_concentration1 = co2_1.get_co2_concentration()
        co2_concentration2 = co2_2.get_co2_concentration()
        co2_concentration3 = co2_3.get_co2_concentration()
        co2_concentration4 = co2_4.get_co2_concentration()
        temperature1 = co2_1.get_temperature()
        humid1 = co2_1.get_humidity()

        data.append([co2_concentration1, co2_concentration2, co2_concentration3, co2_concentration4, temperature1 / 100, humid1 / 100])
        data_live1.append(co2_concentration1)
        data_live2.append(co2_concentration2)
        data_live3.append(co2_concentration3)
        data_live4.append(co2_concentration4)
        t_now = datetime.now()
        time_live.append(t_now)

        plt.legend(['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4'], loc='center', bbox_to_anchor=(0.5, 0.5))
        plt.xticks(rotation=45)
        plt.plot(time_live, data_live1, color='red')
        plt.plot(time_live, data_live2, color='green')
        plt.plot(time_live, data_live3, color='blue')
        plt.plot(time_live, data_live4, color="y")
        plt.draw()
        plt.pause(1)
        c += 1
        pd.DataFrame(data, columns=columns)

        if keyboard.is_pressed('s'):
            print('Step Down Started\n **************\n **************')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow([''])

        elif keyboard.is_pressed('u'):
            print('Step Up Started\n **************\n **************')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow([''])

        else:
            print(f'Hold S for {interval} seconds to record Step Down and U for step up')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow([t_now, co2_concentration1, co2_concentration2, co2_concentration3, co2_concentration4])

def main():
    duration = int(input('Measurement Duration in min: '))
    interval = 1

    ipcon = IPConnection()
    global co2_1, co2_2, co2_3, co2_4
    co2_1 = BrickletCO2V2(UID_S1, ipcon)
    co2_2 = BrickletCO2V2(UID_S2, ipcon)
    co2_3 = BrickletCO2V2(UID_S3, ipcon)
    co2_4 = BrickletCO2V2(UID_S4, ipcon)
    ipcon.connect(HOST, PORT)

    t_start = datetime.now()
    t_start_str = t_start.strftime('%y%m%d_%H%M%S')
    file = 'Raw/measure' + str(t_start_str) + '.csv'
    with open(file, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
        writer.writerow(['Time', 'Concentration [ppm] at ' + UID_S1, 'Concentration [ppm] at ' + UID_S2,
                         'Concentration [ppm] at ' + UID_S3, 'Concentration [ppm] at ' + UID_S4])

    with open("variables.json", "w") as outfile:
        json.dump([file, interval], outfile)

    time_live = []
    data = []
    columns = ['Concentration [ppm] at ' + UID_S1, 'Concentration [ppm] at ' + UID_S2, 'Concentration [ppm] at ' + UID_S3,
               'Concentration [ppm] at ' + UID_S4, 'Temperature [C] at ' + UID_S1, 'Humidity [%] at ' + UID_S1]

    record_and_show(duration, interval, file, columns, data, time_live)

    ColumnsOfDataFrame = ['Concentration [ppm] at ' + UID_S1, 'Concentration [ppm] at ' + UID_S2,
                          'Concentration [ppm] at ' + UID_S3, 'Concentration [ppm] at ' + UID_S4]
    df = pd.DataFrame(data, columns=columns)
    timeseries = np.arange(0, (duration * 60) + 1, interval)
    df.insert(0, 'time', timeseries / 60)

if __name__ == "__main__":
    main()
