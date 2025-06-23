# -*- coding: utf-8 -*-
"""
@author: Amin Darbandi
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

# if tinkerfirge is not available then use ~ pip install tinkerforge ~ and run it again
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_co2_v2 import BrickletCO2V2

# Connect to the sensors
HOST = "localhost"
PORT = 4223
UID_S1 = 'VYU'  # the UID of CO2 Bricklet 2.0
UID_S2 = 'VYV'  # the UID of  CO2 Bricklet 2.0
UID_S3 = '21kv'  # the UID of  CO2 Bricklet 2.0
UID_S4 = 'VZ2'  # the UID of  CO2 Bricklet 2.0

# Measurement Duration
duration = int(input('Measurement Duration in min: '))
interval = 1

# Connection protocol to sensors based on their fact sheet
if __name__ == "__main__":
    ipcon = IPConnection()  # Create IP connection
    co2_1 = BrickletCO2V2(UID_S1, ipcon)  # Create device object for UID_S1
    co2_2 = BrickletCO2V2(UID_S2, ipcon)  # Create device object for UID_S2
    co2_3 = BrickletCO2V2(UID_S3, ipcon)  # Create device object for UID_S3
    co2_4 = BrickletCO2V2(UID_S4, ipcon)  # Create device object for UID_S4

    ipcon.connect(HOST, PORT)  # Connect to The BrickID

# starting time
t_start = datetime.now()

# change the time format
t_start_str = t_start.strftime('%y%m%d_%H%M%S')  # string object

# Create a CSV file of concentration at each point(sensor) and change the name to measurement starting time
file = 'Raw/measure' + str(t_start_str) + '.csv'
with open(file, 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
    writer.writerow(['Time', 'Concentration [ppm] at ' + UID_S1, 'Concentration [ppm] at ' + UID_S2,
                     'Concentration [ppm] at ' + UID_S3,
                     'Concentration [ppm] at ' + UID_S4])

with open("variables.json", "w") as outfile:
    json.dump([file, interval], outfile)

# Empty lists for live visualisation
time_live = []
data = []

# Name of the columns for live visualisation
columns = ['Concentration [ppm] at ' + UID_S1, 'Concentration [ppm] at ' + UID_S2, 'Concentration [ppm] at ' + UID_S3,
           'Concentration [ppm] at ' + UID_S4, 'Temperature [C] at ' +
           UID_S1, 'Humidity [%] at ' + UID_S1]


# Function to record the sensor data and live plot
def record_and_show(duration, interval):
    MeasureTime = duration * 60 / interval
    c = 0
    data_live1 = []
    data_live2 = []
    data_live3 = []
    data_live4 = []

    plt.rcParams['figure.figsize'] = [8, 4]
    plt.rcParams['figure.dpi'] = 100

    while c <= MeasureTime:

        # Read co2 concentration from sensors
        co2_concentration1 = co2_1.get_co2_concentration()
        co2_concentration2 = co2_2.get_co2_concentration()
        co2_concentration3 = co2_3.get_co2_concentration()
        co2_concentration4 = co2_4.get_co2_concentration()

        # Read Temperature of sensor 1
        temperature1 = co2_1.get_temperature()

        # Read humidity of sensor 1
        humid1 = co2_1.get_humidity()

        # Adding sensors data to data=[] to save as CSV at the end of measurement
        data.append([co2_concentration1, co2_concentration2, co2_concentration3, co2_concentration4, temperature1 / 100,
                     humid1 / 100])

        # Add each sensor data to its list for live visualization
        data_live1.append(co2_concentration1)
        data_live2.append(co2_concentration2)
        data_live3.append(co2_concentration3)
        data_live4.append(co2_concentration4)

        # current time stamp
        t_now = datetime.now()

        # Adding the new time stamp to data set
        time_live.append(t_now)

        # Settings for plot
        plt.legend(['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4'], loc='center', bbox_to_anchor=(0.5, 0.5))
        plt.xticks(rotation=45)

        plt.plot(time_live, data_live1, color='red')  # ,label='co2_concentration1')
        plt.plot(time_live, data_live2, color='green')  # ,label='co2_concentration2')
        plt.plot(time_live, data_live3, color='blue')  # ,label='co2_concentration3')
        plt.plot(time_live, data_live4, color="y")  # ,label='co2_concentration4')
        plt.draw()
        plt.pause(1)
        c += 1
        # Create a data frame at the end of measurement period
        pd.DataFrame(data, columns=columns)

        # Add recorded and calculated data to csv file

        if keyboard.is_pressed('s'):
            print('Step Down Started'
                  '\n **************'
                  '\n **************')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow('\n')
                csv_file.close()

        elif keyboard.is_pressed('u'):
            print('Step Up Started'
                  '\n **************'
                  '\n **************')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow('\n')
                csv_file.close()
        else:
            print(f'Hold S for {interval} seconds to record Step Down and U for step up')
            with open(file, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\r')
                writer.writerow([t_now, co2_concentration1, co2_concentration2, co2_concentration3, co2_concentration4])
                csv_file.close()
        # t.sleep(1)


# run the visualization function

record_and_show(duration, interval)

ColumnsOfDataFrame = ['Concentration [ppm] at ' + UID_S1, 'Concentration [ppm] at ' + UID_S2,
                      'Concentration [ppm] at ' + UID_S3,
                      'Concentration [ppm] at ' + UID_S4]

# Create a data frame just for concentrations
df = pd.DataFrame(data, columns=columns)

# Create and add the time series in second to data frame
timeseries = np.arange(0, (duration * 60) + 1, interval)

df.insert(0, 'time', timeseries / 60)
