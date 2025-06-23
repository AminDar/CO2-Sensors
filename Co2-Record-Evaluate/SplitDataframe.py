# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

import numpy as np
import pandas as pd
import json
import sys
import matplotlib.pyplot as plt
from colorama import Fore
from MFCstepupFunction import step_up_calculator
from MFCstepDownFunction import step_down_calculator

## ASK IF it is the pulse method

pulse = int(input('Do you want to evaluate a "Pulse Method"? 0 for No, 1 For Yes: '))

path = 'variables.json'

columns = ['time', 'Concentration [ppm] at VYU', 'Concentration [ppm] at VYV',
           'Concentration [ppm] at 21kv', 'Concentration [ppm] at VZ2']


def process_setup_data(df):
    first_timestamp = df['time'].dropna().iloc[0] if not df['time'].isnull().all() else None

    df['time'] = (df['time'] - first_timestamp).dt.total_seconds()
    df['time'] = df['time'].astype('float32')

    # set 0
    for col in df.columns[1:]:
        df.loc[:, col] = df[col] - df[col].iloc[0]

    # Calibration
    df = calibrate_data(df)

    return df


def process_setdown_data(df):
    # Calculate time differences and explicitly cast to float
    first_timestamp = df['time'].dropna().iloc[0] if not df['time'].isnull().all() else None

    df['time'] = (df['time'] - first_timestamp).dt.total_seconds()
    df['time'] = df['time'].astype('float32')

    # set 0
    for col in df.columns[1:]:
        df.loc[:, col] = df[col] - df[col].iloc[-1]

    # Calibration
    df = calibrate_data(df)

    return df


def calibrate_data(df):
    df.iloc[:, 1] = 1.153 * df.iloc[:, 1] + 34.763  # Calibration VYU
    df.iloc[:, 2] = 1 * df.iloc[:, 2] - 0  # VYV Original
    df.iloc[:, 3] = 1.118 * df.iloc[:, 3] + 41.575  # Calibration 21kv
    df.iloc[:, 4] = 0.935 * df.iloc[:, 4] + 0.59  # Calibration VZ2

    return df


def split_up_down_data(path, column_names):
    with open(path, 'r') as json_file:
        metadata = json.load(json_file)

    # Extract the file path, interval, and duration from the metadata
    csv_file_path = metadata[0]
    interval = metadata[1]
    df = pd.read_csv(csv_file_path, delimiter=';', skip_blank_lines=None)
    df.columns = column_names
    df['time'] = pd.to_datetime(df['time'], errors='coerce')

    blank_rows = df.isnull().all(axis=1)
    blank_indices = blank_rows[blank_rows].index
    split_index = blank_indices[0]
    for i in range(1, len(blank_indices)):
        if blank_indices[i] != blank_indices[i - 1] + 1:
            break
        split_index = blank_indices[i]

    df_up = df.iloc[:split_index].dropna(how='all')
    df_down = df.iloc[split_index + 1:] if split_index < len(df) else pd.DataFrame()

    if not df_up.empty:
        df_up = process_setup_data(df_up.copy())
    if not df_down.empty:
        df_down = process_setdown_data(df_down.copy())

    return df_up, df_down


def plot_data(df_up, df_down):
    plt.figure(figsize=(12, 6))

    # Plot Step Up Data
    if not df_up.empty:
        plt.plot(df_up['time'], df_up.iloc[:, 1], label='Sensor 1 (VYU) - Step Up', color='blue')
        plt.plot(df_up['time'], df_up.iloc[:, 2], label='Sensor 2 (VYV) - Step Up', color='orange')
        plt.plot(df_up['time'], df_up.iloc[:, 3], label='Sensor 3 (21kv) - Step Up', color='green')
        plt.plot(df_up['time'], df_up.iloc[:, 4], label='Sensor 4 (VZ2) - Step Up', color='red')

    # Plot Step Down Data with adjusted time axis
    if not df_down.empty:
        max_time_up = df_up['time'].max() if not df_up.empty else 0
        df_down['time'] = df_down['time'] + max_time_up

        plt.plot(df_down['time'], df_down.iloc[:, 1], label='Sensor 1 (VYU) - Step Down', linestyle='--', color='blue')
        plt.plot(df_down['time'], df_down.iloc[:, 2], label='Sensor 2 (VYV) - Step Down', linestyle='--', color='orange')
        plt.plot(df_down['time'], df_down.iloc[:, 3], label='Sensor 3 (21kv) - Step Down', linestyle='--', color='green')
        plt.plot(df_down['time'], df_down.iloc[:, 4], label='Sensor 4 (VZ2) - Step Down', linestyle='--', color='red')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Concentration [ppm]')
    plt.title('Sensor Data - Step Up and Step Down')
    plt.legend()
    plt.grid(True)
    plt.show()


df_stepUp, df_stepDown = split_up_down_data(path, columns)
print(df_stepUp.iloc[:, 0:3])

if pulse == 0:
    step_up_calculator(df_stepUp)
    step_down_calculator(df_stepDown)
    plot_data(df_stepUp, df_stepDown)

else:
    # import plot
    import Total_Integral
    import SplitedIntegral

    print(Fore.MAGENTA + '\nThis code is not ready to evaluate pluse method yet! Sorry!'
                         '\nThe figure is exported!')
    sys.exit()
