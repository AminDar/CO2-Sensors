import numpy as np
import pandas as pd

O  = '\033[36m' # orange
W  = '\033[0m'  # white (normal)
P  = '\033[35m' # purple
from colorama import Fore
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json
with open('variables.json', 'r') as openfile:
  
    # Reading from json file
    variables= json.load(openfile)

file = variables [0]


MessStelle =['Concentration [ppm] at VYU', 'Concentration [ppm] at VYV',
       'Concentration [ppm] at VYS', 'Concentration [ppm] at VZ2']

points = ['Top Left', 'Bottom Left','Top Middle', 'Middle Middle' ]

Columns =['time','Concentration [ppm] at VYU', 'Concentration [ppm] at VYV',
       'Concentration [ppm] at VYS', 'Concentration [ppm] at VZ2']

def StepUp (df):
    
    dfAll= pd.concat([df.time, df[MessStelle[0]],df[MessStelle[1]],df[MessStelle[2]],df[MessStelle[3]]],
                     axis=1,keys = Columns)

#loding the backgrund concentration

    n = len(dfAll.time) 
    g= [2000,0.003]
    c_infAll = dfAll.iloc[n-1,1:]

    tn= dfAll['time'][n-1]
    c =[]
    t=dfAll['time'].values
    yFit = dfAll.iloc[:,1:5].values
    
    def consModel (t1,cn,c0):
            return c_inf+(cn-c_inf)*np.exp((-c0)*(t1-tn))
        
    #curve fitting
    

    for i in range(4):
       c_inf = c_infAll[i]
       c.append (curve_fit(consModel,t,yFit[:,i],g)[0]) 
    # print ('Constans for the model are %s' %c)

#getting not abslute value
    slopes =[]
    for i in range(4):
        slopes.append(c[i][1])

    time = dfAll['time']
    
    
    # Calculating the C equation in (A+B)/(C+D)
    tailSum = []
    for j in range (4): 
       h =[]
       for i in range(n - 1):
           c_inf = c_infAll[j]
           concentration = yFit[:,j]
           f = abs(1-(concentration[i] + concentration[i+1])/ (2*c_inf)) * (time[i+1] - time[i])
           h.append(f)
       tailSum.append(sum(h))
    
# Weigthed area under the curve | Calculating the A equation in (A+B)/(C+D) 
    WeigthedtailSum = []
    for j in range (4):
        h = []
        for i in range(n - 1):
            
            c_inf = c_infAll[j]
            concentration = yFit[:,j]    
            f = abs ((1-(concentration[i] + concentration[i+1]) / (2*c_inf)) * (time[i] - time[i + 1]) * (time[i] + time[i + 1]) / 2)
            h.append(f)
        WeigthedtailSum.append(sum(h))

# Calculating the B equation in (A+B)/(C+D) 

    Weigthedtail = []
    for j in range (4): 
        for i in range(n - 1):
            c_inf = c_infAll[j]
            concentration = yFit[:,j]    
            WeigthT = (1-(concentration[n-1] / c_inf))*((time[n-1]/ slopes[j])+ 1/(pow(slopes[j],2)))
        Weigthedtail.append(WeigthT)
 

#Calculation of D
    D = []
    for j in range(4):
     c_inf = c_infAll[j]
     concentration = yFit[:,j]
     d = (1-(concentration[n-1] / c_inf))/slopes[j]
     D.append(d)
     
     
#Mean age of air
    Tau = []
    for j in range (4):
        Taus= (WeigthedtailSum [j] + Weigthedtail[j]) / (tailSum[j] + D[j])
        where = points[j]
        Tau.append(Taus)
        print (P+'Step Up Mean age of air at %s:' %where, np.round(Taus,3) )
    
#Nominal air change time
    nTau =[]
    for j in range (4):
        where = points[j]
        nTaus= (tailSum [j] + D[j])
        nTau.append(nTaus)
        print (W+'Step Up  Nominal air change time at %s:' %where, np.round(nTaus,3) )

#Air change efficiency, %
    airEff =[]
    for j in range (4):
        where = points[j]
        airEffs= 100*(nTau[j])/(2*Tau[j])
        airEff.append(airEffs)
        print (O+'Step Up  Air change efficiency at %s:' %where, np.round(airEffs,3), '%')
    
#Turn Over Time, %    
    TurnOver =[]
    for j in range (4):
        h = []
        for i in range (n-1):
            where = points[j]
            concentration = yFit[:,j]    
            f = abs(((1-(concentration[i]+concentration[i+1]) / (2*concentration[n-1]))) * (time[i+1] - time[i]))
            h.append(f)
        TurnOver.append(sum(h))
        print (Fore.YELLOW+'Step Up Turn over time at %s:' %where, np.round(TurnOver[j],3))
    print('-------------')
    
    for j in range (4):
        where = points[j]
        plt.plot (dfAll['time'],dfAll.iloc[:,j+1].values,'r', label = "Expriemental")
        plt.xlabel('Time[s]')
        plt.ylabel ('Concentration [ppm]')
        plt.title ('Step Up Mesuared at %s' %where)
        plt.show()
    with open("StepUp " + str(file[:-4])+ ".json", "w") as outfile:
        json.dump([Tau, nTau, airEff,TurnOver],outfile)




