#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 10:13:08 2022

@author: AminDar @Github
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

def main():
    points = ['Top Left', 'Bottom Left', 'Top Middle', 'Middle Middle', 'Step Down started']

    try:
        with open('variables.json', 'r') as openfile:
            variables = json.load(openfile)
        interval = variables[1]
        file = variables[0]
    except (FileNotFoundError, json.JSONDecodeError, IndexError) as e:
        print(f"Error reading variables.json: {e}")
        return

    UID_S1 = 'VYU'
    UID_S2 = 'VYV'
    UID_S3 = '21kv'
    UID_S4 = 'VZ2'

    try:
        df = pd.read_csv(file, delimiter=';', lineterminator='\r')
    except FileNotFoundError:
        print(f"CSV file not found: {file}")
        return

    col_s1 = f'Concentration [ppm] at {UID_S1}'
    if col_s1 not in df.columns:
        print(f"Expected column '{col_s1}' not found in CSV.")
        return

    find_nan = np.where(pd.isnull(df[col_s1]))[0]

    ColumnsOfDataFrame = [
        f'Concentration [ppm] at {UID_S1}',
        f'Concentration [ppm] at {UID_S2}',
        f'Concentration [ppm] at {UID_S3}',
        f'Concentration [ppm] at {UID_S4}'
    ]

    df.insert(0, 'time', np.arange(0, df.shape[0] * interval, interval))
    df.plot('time', y=ColumnsOfDataFrame)

    if find_nan.size > 0:
        plt.vlines(x=find_nan, color='black', ymin=df[ColumnsOfDataFrame[2]].min(),
                   ymax=df[ColumnsOfDataFrame[1]].max(), linestyle='--', label='Step Down Started')

    plt.rcParams["figure.figsize"] = [10, 6]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.dpi"] = 300
    plt.xlabel('Time[s]')
    plt.ylabel('Concentration [ppm]')
    plt.legend(points, bbox_to_anchor=(0, 1, 1, 0), loc='lower left', ncol=3)

    output_file = Path(file).with_suffix('.jpg')
    plt.savefig(output_file, dpi=200)
    plt.show()

if __name__ == "__main__":
    main()