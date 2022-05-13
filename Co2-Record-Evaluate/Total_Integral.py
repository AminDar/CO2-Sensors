#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:26:58 2022

@author: aminmasterthesis
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json




with open('variables.json', 'r') as openfile:
  
    # Reading from json file
    variables= json.load(openfile)

interval = variables [1]
file = variables [0]

"""
UID_S1 = 'VYU' #the UID of CO2 Bricklet 2.0
UID_S2 = 'VYV' #the UID of  CO2 Bricklet 2.0
UID_S3 = 'VYS' #the UID of  CO2 Bricklet 2.0
UID_S4 = 'VZ2' #the UID of  CO2 Bricklet 2.0 

"""

def integral_Total(point):
    
    points = ['time','Top Left', 'Bottom Left','Top Middle', 'Middle Middle']
    
    legends = [points[point],'Step Down Started']
    
    sensor_name = ['dummy','VYU','VYV','VYS','VZ2']

    df= pd.read_csv(file,delimiter=';',lineterminator='\r')
    
    integral = pd.read_csv(file,delimiter=';',lineterminator='\r', usecols=[point])
    integral.insert(0,'time',np.arange(0,integral.shape[0]*interval,interval))
    integral=integral.dropna()
    
    find_nan = np.where(pd.isnull(df['Concentration [ppm] at '+ sensor_name[point]]))


    ColumnsOfDataFrame = ['Concentration [ppm] at '+ sensor_name[point]]

    df.insert(0,'time',np.arange(0,df.shape[0]*interval,interval))

    integral.plot('time',y=ColumnsOfDataFrame)

    plt.vlines(x=find_nan,color='black', ymin= df[ColumnsOfDataFrame[0]].min(), ymax=df[ColumnsOfDataFrame[0]].max(),
           linestyle='--', label='Step Down Started')
    

    x = integral['time'].to_numpy()
    y = integral[ColumnsOfDataFrame[0]].to_numpy()
    ymin = y.min()
    x_min, x_max = integral['time'].min(), integral['time'].max()

    idx = np.where((np.array(x)>=x_min) & (np.array(x)<=x_max))[0]
    
    

    
    '''
    plt.hlines(y=np.linspace(486, 1030,5),color='black', xmin= 0, xmax= 300,linestyle='--')
    plt.xticks(np.arange(min(x), max(x)+1, 35))
    plt.yticks(np.arange(min(y), max(y)+1, 30),fontsize=12)
    plt.xticks(rotation = 90,fontsize=12)
    '''
   

    plt.yticks(np.arange(min(y), max(y)+1, 30),fontsize=12)
    
    integsum = np.trapz(x=np.array(x)[idx],y=np.array(y)[idx]-ymin)
    
    print(f"Integral under the curve for {points[point]} is: {integsum}")
    
    plt.fill_between(x ,y, ymin ,color = 'lightgreen')


    plt.rcParams["figure.figsize"] = [10,6]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["figure.dpi"] = 300

    plt.xlabel('Time[s]')
    plt.ylabel('Concentration [ppm]')

    ### mode="expand"
    plt.legend(legends,bbox_to_anchor=(0, 1, 1, 0), loc="lower left", ncol=3)
    


integral_Total(3)

