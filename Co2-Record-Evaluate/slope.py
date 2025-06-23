# -*- coding: utf-8 -*-
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
import sys
from scipy.optimize import curve_fit

with open('variables.json', 'r') as openfile:
    # Reading from JSON file
    variables = json.load(openfile)

interval = variables[1]
file = variables[0][4:]
path_to_load = os.path.join('Raw', file)

def regressor_model(t, a, b):
    return a * np.exp(b * t)

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
        if not period.empty:
            period.iloc[:, 0] = period.iloc[:, 0] - first_row_value
            period.insert(0, 'time', np.arange(0, period.shape[0] * interval, interval))
            periods.append(period)

    return periods

def plot_with_regression(point, df):
    points = ['time', 'VYU', 'VYV', '21kv', 'VZ2']
    sensor_name = ['dummy', 'VYU', 'VYV', '21kv', 'VZ2']
    columns_of_data_frame = ['Concentration [ppm] at ' + sensor_name[point]]

    # Apply calibration to the data
    df = calibrate_data(df)

    if columns_of_data_frame[0] not in df.columns:
        return

    # Extract data for fitting (skip the first data point)
    x = df['time'].to_numpy()[1:]
    y = df[columns_of_data_frame[0]].to_numpy()[1:]

    if len(y) == 0:
        sys.exit()

    # Fit the data to the regressor model with initial guesses
    p0 = [y.max(), -0.01]  # Initial guesses for a and b
    try:
        popt, _ = curve_fit(regressor_model, x, y, p0=p0, maxfev=10000)
        a, b = popt

        # Print the regression equation
        equation_text = f"y = {a:.2f} * exp({b:.4f} * t)"
        print(f"Fitted equation: {equation_text}")

        # Generate fitted curve
        y_fitted = regressor_model(x, *popt)

        # Plot the data and fitted curve
        plt.figure(figsize=(10, 6))  # Set figure size explicitly for each plot
        plt.plot(x, y, label='Concentration')
        plt.plot(x, y_fitted, label=f'Regression Line: {equation_text}', linestyle='--')

        # Plot formatting
        plt.xlabel('Time [s]', fontsize=20)
        plt.ylabel('Concentration [ppm]', fontsize=20)
        plt.legend(loc='upper left', fontsize=16)
        plt.title('Slopes', fontsize=22)
        plt.tick_params(axis='both', which='major', labelsize=16)  # 主要刻度字体大小
        plt.tick_params(axis='both', which='minor', labelsize=16)

        plt.show()
        plt.close()
    except (RuntimeError, TypeError) as e:
        print(f"Error in fitting curve: {e}")

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

if not a:
    sys.exit()
for i in a:
    plot_with_regression(eval_point, i)

if __name__ == '__main__':
    calibrate_data()
