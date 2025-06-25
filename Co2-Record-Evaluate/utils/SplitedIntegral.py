"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from itertools import chain
import os
from pathlib import Path

try:
    with open(Path('../variables.json'), 'r') as openfile:
        variables = json.load(openfile)
    interval = variables[1]
    file = variables[0][4:]
    path_to_load = Path('../Raw') / file
except (FileNotFoundError, json.JSONDecodeError, IndexError) as e:
    print(f"Error loading configuration: {e}")
    exit(1)

def split_data_frame(column_index):
    try:
        integral = pd.read_csv(path_to_load, delimiter=';', lineterminator='\r', usecols=[column_index])
    except Exception as e:
        print(f"Error reading CSV: {e}")
        exit(1)

    integral.loc[len(integral.index)] = [np.nan]
    split_indices = [i for i in range(len(integral) - 1)
                     if pd.isnull(integral.iloc[i + 1, 0]) and pd.notnull(integral.iloc[i, 0])]

    periods = []
    start_indices = [0] + [split_indices[i] for i in range(1, len(split_indices), 2)]
    end_indices = [split_indices[i] for i in range(1, len(split_indices), 2)]

    for start, end in zip(start_indices, end_indices):
        segment = integral.iloc[start:end].dropna().reset_index(drop=True)
        segment.insert(0, 'time', np.arange(0, segment.shape[0] * interval, interval))
        periods.append(segment)

    return periods

def periodic_integral(sensor_index, df, ymin):
    sensor_labels = ['VYU', 'VYV', '21kv', 'VZ2']
    column_name = f'Concentration [ppm] at {sensor_labels[sensor_index - 1]}'

    plt.rcParams.update({
        "figure.figsize": [10, 6],
        "figure.autolayout": True,
        "figure.dpi": 100
    })

    df.plot('time', y=column_name)

    x = df['time'].to_numpy()
    y = df[column_name].to_numpy()

    x_min, x_max = df['time'].min(), df['time'].max()
    idx = np.where((x >= x_min) & (x <= x_max))[0]
    ymin = y.min() if ymin is None else ymin

    integral_value = np.trapezoid(x=x[idx], y=y[idx] - ymin)
    print(f"Integral under the curve for {sensor_labels[sensor_index - 1]} is: {integral_value}")

    plt.fill_between(x, y, ymin, color='lightgreen')
    plt.yticks(np.arange(ymin, max(y) + 1, 150), fontsize=12)
    plt.xlabel('Time[s]')
    plt.ylabel('Concentration [ppm]')
    plt.legend([sensor_labels[sensor_index - 1], 'Step Down Started'], bbox_to_anchor=(0, 1, 1, 0), loc="lower left", ncol=3)
    print("Saving figure...")
    plt.savefig('figs.jpg')
    plt.show()
    plt.close()

try:
    eval_point = int(input('Which point do you want to evaluate?\nVYU: 1\nVYV: 2\n21kv: 3\nVZ2: 4\n'))
    if eval_point not in [1, 2, 3, 4]:
        raise ValueError("Invalid input. Please enter a number between 1 and 4.")
except ValueError as ve:
    print(f"Input error: {ve}")
    exit(1)

segments = split_data_frame(eval_point)
ymin = max(chain(segments[0].min())) if segments else 0
for segment in segments:
    periodic_integral(eval_point, segment, ymin)