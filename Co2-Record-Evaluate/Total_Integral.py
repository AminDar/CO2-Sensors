"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Read variables from the JSON file
with open('variables.json', 'r') as openfile:
    variables = json.load(openfile)

interval = variables[1]
file = variables[0][4:]
path_to_load = os.path.join('Raw', file)

def calibrate_data(df):
    # Assume these are the calibration factors and offsets
    calibration_factors = [1.1579, 1.0, 1.1273, 0.9399]
    calibration_offsets = [15.1083, 0, 51.5207, -9.3664]

    for i, sensor in enumerate(['VYU', 'VYV', '21kv', 'VZ2']):
        df['Concentration [ppm] at ' + sensor] = (
            calibration_factors[i] * df['Concentration [ppm] at ' + sensor] + calibration_offsets[i]
        )

    return df

def plot_all_sensors():
    sensor_name = ['VYU', 'VYV', '21kv', 'VZ2']
    df = pd.read_csv(path_to_load, delimiter=';', lineterminator='\r')
    df.insert(0, 'time', np.arange(0, df.shape[0] * interval, interval))

    # Zero adjustment
    for i, sensor in enumerate(sensor_name):
        df['Concentration [ppm] at ' + sensor] = df['Concentration [ppm] at ' + sensor] - \
                                                 df['Concentration [ppm] at ' + sensor].iloc[0]

    # Add calibration
    df = calibrate_data(df)

    plt.figure(figsize=(10, 6))
    for i, sensor in enumerate(sensor_name):
        plt.plot(df['time'], df['Concentration [ppm] at ' + sensor], label=f'Sensor {i + 1} ({sensor})')

    plt.xlabel('Time [s]')
    plt.ylabel('Concentration [ppm]')
    plt.title('Concentration Change of All Sensors Over Time')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

# Directly plot the concentration changes of all sensors
plot_all_sensors()