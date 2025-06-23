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
from itertools import chain

with open('variables.json', 'r') as openfile:
    # Reading from json file
    variables = json.load(openfile)

interval = variables[1]
file = variables[0][4:]
path_to_load = os.path.join('Raw', file)
"""
UID_S1 = 'VYU' #the UID of CO2 Bricklet 2.0
UID_S2 = 'VYV' #the UID of  CO2 Bricklet 2.0
UID_S3 = '21kv' #the UID of  CO2 Bricklet 2.0
UID_S4 = 'VZ2' #the UID of  CO2 Bricklet 2.0 

"""

def calibrate_data(df):
    # Calibration factors and offsets for each sensor
    calibration_factors = [1.1579, 1.0, 1.1273, 0.9399]
    calibration_offsets = [15.1083, 0, 51.5207, -9.3664]

    for i, sensor in enumerate(['VYU', 'VYV', '21kv', 'VZ2']):
        column_name = 'Concentration [ppm] at ' + sensor
        if column_name in df.columns:
            df[column_name] = df[column_name] * calibration_factors[i] + calibration_offsets[i]

    return df

def split_data_frame(point):
    integral = pd.read_csv(path_to_load, delimiter=';', lineterminator='\r', usecols=[point])

    # If there is no NaN value at the end of dataframe, add one row of NaN
    integral.loc[len(integral.index)] = [np.nan]
    slice_data = []

    first_row_value = integral.iloc[0, 0]

    for column_name in integral:
        for i in range(0, len(integral) - 1):
            if pd.isnull(integral[column_name][i + 1]) and pd.notnull(integral[column_name][i]):
                slice_data.append(i)

    periods = []
    for start, end in zip([0] + slice_data, slice_data + [len(integral) - 1]):
        period = integral[start:end].dropna().reset_index(drop=True)
        period.iloc[:, 0] = period.iloc[:, 0] - first_row_value
        period.insert(0, 'time', np.arange(0, period.shape[0] * interval, interval))
        periods.append(period)

    return periods

def periodic_integral(point, df, segment_index):
    points = ['time', 'VYU', 'VYV', '21kv', 'VZ2']
    legends = [points[point], 'Step Down Started']
    sensor_name = ['dummy', 'VYU', 'VYV', '21kv', 'VZ2']
    columns_of_data_frame = ['Concentration [ppm] at ' + sensor_name[point]]

    # Apply calibration to the data
    df = calibrate_data(df)

    if columns_of_data_frame[0] not in df.columns:
        print(f"Column {columns_of_data_frame[0]} not found in the dataframe.")
        return

    df.plot('time', y=columns_of_data_frame)

    x = df['time'].to_numpy()
    y = df[columns_of_data_frame[0]].to_numpy()

    # Determine ymin based on segment index
    if segment_index % 2 != 0:
        ymin = 0  # For odd segments, integrate with respect to the x-axis
    else:
        ymin = y.max()  # For even segments, integrate with respect to the maximum concentration in the segment

    x_min, x_max = df['time'].min(), df['time'].max()
    idx = np.where((np.array(x) >= x_min) & (np.array(x) <= x_max))[0]

    plt.yticks(np.arange(0, max(y) + 1, 100), fontsize=12)  # Set y-axis ticks with 100 as interval

    integral_value = np.trapz(x=np.array(x)[idx], y=np.array(y)[idx] - ymin)
    print(f"Integral under the curve for {points[point]} in segment {segment_index + 1} is: {integral_value}")

    plt.fill_between(x, y, ymin, color='lightgreen')

    plt.rcParams["figure.figsize"] = [10, 6]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.dpi"] = 100

    plt.xlabel('Time[s]')
    plt.ylabel('Concentration [ppm]')
    plt.ylim(bottom=0, top=max(y) * 1.1)  # Set y-axis to start from 0 and adjust to a suitable range

    # mode="expand"
    plt.legend(legends, bbox_to_anchor=(0, 1, 1, 0), loc="lower left", ncol=3)
    plt.show()
    plt.close()

eval_point = int(input('which point do you want to evaluate? \nVYU: 1 \nVYV: 2 \n21kv: 3\nVZ2: 4\n'))

# Load data and apply zero adjustment once
full_data = pd.read_csv(path_to_load, delimiter=';', lineterminator='\r')
full_data.insert(0, 'time', np.arange(0, full_data.shape[0] * interval, interval))
for sensor in ['VYU', 'VYV', '21kv', 'VZ2']:
    column_name = 'Concentration [ppm] at ' + sensor
    if column_name in full_data.columns:
        full_data[column_name] -= full_data[column_name].iloc[0]

# Split data into segments
a = split_data_frame(eval_point)

# For ymin constant
ymin = min([df.iloc[:, 1].min() for df in a])

for index, segment in enumerate(a):
    periodic_integral(eval_point, segment, index)
