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

points = ['Top Left', 'Bottom Left', 'Top Middle', 'Middle Middle', 'Step Down started']

with open('variables.json', 'r') as openfile:
    # Reading from json file
    variables = json.load(openfile)

interval = variables[1]
file = variables[0]

UID_S1 = 'VYU'  # the UID of CO2 Bricklet 2.0
UID_S2 = 'VYV'  # the UID of CO2 Bricklet 2.0
UID_S3 = '21kv'  # the UID of CO2 Bricklet 2.0
UID_S4 = 'VZ2'  # the UID of CO2 Bricklet 2.0

df = pd.read_csv(file, delimiter=';', lineterminator='\r')

find_nan = np.where(pd.isnull(df['Concentration [ppm] at ' + UID_S1]))

ColumnsOfDataFrame = ['Concentration [ppm] at ' + UID_S1, 'Concentration [ppm] at ' + UID_S2,
                      'Concentration [ppm] at ' + UID_S3,
                      'Concentration [ppm] at ' + UID_S4]

df.insert(0, 'time', np.arange(0, df.shape[0] * interval, interval))
df.plot('time', y=ColumnsOfDataFrame)

plt.vlines(x=find_nan, color='black', ymin=df[ColumnsOfDataFrame[2]].min(), ymax=df[ColumnsOfDataFrame[1]].max(),
           linestyle='--', label='Step Down Started')

plt.rcParams["figure.figsize"] = [10, 6]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.dpi"] = 300
plt.xlabel('Time[s]')
plt.ylabel('Concentration [ppm]')
plt.legend(points, bbox_to_anchor=(0, 1, 1, 0), loc='lower left', ncol=3)
plt.savefig(str(file[4:-4])+'.jpg', dpi=200)
plt.show()