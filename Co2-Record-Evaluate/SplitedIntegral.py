
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

with open('variables.json', 'r') as openfile:
    # Reading from a JSON file
    variables = json.load(openfile)

interval = variables[1]
file = variables[0][4:]
path_to_load = os.path.join('Raw', file)
"""
UID_S1 = 'VYU' #the UID of CO2 Bricklet 2.0
UID_S2 = 'VYV' #the UID of  CO2 Bricklet 2.0
UID_S3 = 'VYS' #the UID of  CO2 Bricklet 2.0
UID_S4 = 'VZ2' #the UID of  CO2 Bricklet 2.0 

"""


def split_data_frame(point):
    integral = pd.read_csv(path_to_load, delimiter=';', lineterminator='\r', usecols=[point])

    # if there is no nan value at the end of a dataframe, we should add one row of nan

    integral.loc[len(integral.index)] = [np.nan]
    slice_data = []

    for column_name in integral:
        for i in range(0, len(integral) - 1):
            if pd.isnull(integral[column_name][i + 1]) and pd.notnull(integral[column_name][i]):
                (slice_data.append(i))

    periods = []
    odd_j = [0]
    for i in range(0, len(slice_data)):
        if i % 2:
            odd_j.append(slice_data[i])

    even_i = []
    for i in range(0, len(slice_data)):
        if i % 2:
            even_i.append(slice_data[i])

    for i, j in zip(even_i, odd_j):
        period = integral[j:i].dropna().reset_index(drop=True)
        period.insert(0, 'time', np.arange(0, period.shape[0] * interval, interval))
        periods.append(period)

    return periods


def periodic_integral(point, df, ymin):
    points = ['time', 'VYU', 'VYV', '21kv', 'VZ2']

    legends = [points[point], 'Step Down Started']

    sensor_name = ['dummy', 'VYU', 'VYV', '21kv', 'VZ2']

    columns_of_data_frame = ['Concentration [ppm] at ' + sensor_name[point]]

    df.plot('time', y=columns_of_data_frame)

    x = df['time'].to_numpy()
    y = df[columns_of_data_frame[0]].to_numpy()

    # if we should deduce min of each list

    ymin = y.min()

    x_min, x_max = df['time'].min(), df['time'].max()

    idx = np.where((np.array(x) >= x_min) & (np.array(x) <= x_max))[0]

    '''

    plt.xticks(np.arange(min(x), max(x)+1, 35))
    plt.yticks(np.arange(min(y), max(y)+1, 30),fontsize=12)
    plt.xticks(rotation = 90,fontsize=12)

   '''

    plt.yticks(np.arange(ymin, max(y) + 1, 150), fontsize=12)

    integral_value = np.trapz(x=np.array(x)[idx], y=np.array(y)[idx] - ymin)

    print(f"Integral under the curve for {points[point]} is: {integral_value}")

    plt.fill_between(x, y, ymin, color='lightgreen')

    plt.rcParams["figure.figsize"] = [10, 6]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.dpi"] = 100

    plt.xlabel('Time[s]')
    plt.ylabel('Concentration [ppm]')

    # mode="expand"
    plt.legend(legends, bbox_to_anchor=(0, 1, 1, 0), loc="lower left", ncol=3)
    print("Saving figure...")
    plt.savefig('figs.jpg')
    plt.show()
    plt.close()



eval_point = int(input('which point do you want to evaluate? \n'
                       'VYU: 1 \nVYV: 2 \n21kv: 3\nVZ2: 4\n'))

a = split_data_frame(eval_point)

'''
# For ymin constant
'''

ymin = a[0].min()
ymin = max(chain(ymin))

for i in a:
    periodic_integral(eval_point, i, ymin)

