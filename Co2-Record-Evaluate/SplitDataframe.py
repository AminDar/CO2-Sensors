# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:02:24 2022

@author: Amin Darbandi
"""

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import json
import sys
from colorama import Fore
## ASK IF  it is pluse method

pluse = int(input('Do you want to evaluate a "Pluse Method"? 0 for No, 1 For Yes: '))

with open('variables.json', 'r') as openfile:
  
    # Reading from json file
    variables= json.load(openfile)

interval = variables [1]
file = variables [0]

df= pd.read_csv(file,delimiter=';',lineterminator='\r')

nan = np.where(pd.isnull(df))

start, end = nan[0].min(), nan[0].max()+1

stepup = df.iloc[:start,:]
stepdown = df.iloc[end:,:].reset_index()


UID_S1 = 'VYU' #the UID of CO2 Bricklet 2.0
UID_S2 = 'VYV' #the UID of  CO2 Bricklet 2.0
UID_S3 = 'VYS' #the UID of  CO2 Bricklet 2.0
UID_S4 = 'VZ2' #the UID of  CO2 Bricklet 2.0 

ColumnsOfDataFrame = ['Concentration [ppm] at '+ UID_S1,'Concentration [ppm] at '+ UID_S2,'Concentration [ppm] at '+ UID_S3,
                     'Concentration [ppm] at '+ UID_S4]

df_StepDown=pd.DataFrame(stepdown,columns=ColumnsOfDataFrame)

df_StepUp= pd.DataFrame(stepup,columns=ColumnsOfDataFrame)

df_StepUp.insert(0,'time',np.arange(0,df_StepUp.shape[0]*interval,interval))

df_StepDown.insert(0,'time',np.arange(0,df_StepDown.shape[0]*interval,interval))


if pluse == 0 :
    from MFCstepupFunction import StepUp
    StepUp(df_StepUp)

    from MFCstepDownFunction import StepDown
    StepDown(df_StepDown)
    
    import plot

else:
    import plot
    import Total_Integral
    import SplitedIntegral
    print(Fore.MAGENTA +'\nThis code is not ready to evaluate pluse method yet! Sorry!' 
          '\nThe figure is exported!')
    sys.exit()
