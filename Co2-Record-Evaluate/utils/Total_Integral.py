"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

# Constants
SENSOR_NAMES = ['VYU', 'VYV', '21kv', 'VZ2']
CALIBRATION_FACTORS = {
    'VYU': (1.1579, 15.1083),
    'VYV': (1.0, 0),
    '21kv': (1.1273, 51.5207),
    'VZ2': (0.9399, -9.3664)
}

# Read variables from the JSON file
with open(Path('../variables.json'), 'r') as openfile:
    variables = json.load(openfile)

interval = variables[1]
file = variables[0][4:]
path_to_load = Path('../Raw') / file

def calibrate_data(df):
    for sensor in SENSOR_NAMES:
        factor, offset = CALIBRATION_FACTORS[sensor]
        df[f'Concentration [ppm] at {sensor}'] = factor * df[f'Concentration [ppm] at {sensor}'] + offset
    return df

def plot_all_sensors():
    df = pd.read_csv(path_to_load, delimiter=';', lineterminator='\r')
    df.insert(0, 'time', np.arange(0, df.shape[0] * interval, interval))

    for sensor in SENSOR_NAMES:
        df[f'Concentration [ppm] at {sensor}'] -= df[f'Concentration [ppm] at {sensor}'].iloc[0]

    df = calibrate_data(df)

    plt.figure(figsize=(10, 6))
    for i, sensor in enumerate(SENSOR_NAMES):
        plt.plot(df['time'], df[f'Concentration [ppm] at {sensor}'], label=f'Sensor {i + 1} ({sensor})')

    plt.xlabel('Time [s]')
    plt.ylabel('Concentration [ppm]')
    plt.title('Concentration Change of All Sensors Over Time')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.savefig('all_sensors_concentration.png', dpi=300)
    plt.show()

plot_all_sensors()
