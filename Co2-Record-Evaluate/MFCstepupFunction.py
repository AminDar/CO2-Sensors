# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

import numpy as np
from colorama import Fore
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

O = '\033[36m'  # orange
W = '\033[0m'  # white (normal)
P = '\033[35m'  # purple

Measure_Position = ['Concentration [ppm] at VYU', 'Concentration [ppm] at VYV',
                    'Concentration [ppm] at 21kv', 'Concentration [ppm] at VZ2']

points = ['VYU', 'VYV', '21kv', 'VZ2']


def step_up_calculator(df):
    n = len(df.time)
    c_inf_all = df.iloc[-1, 1:]

    c = []
    yFit = df.iloc[:, 1:5].values
    t = df.iloc[:, 0].values

    # Fitting model to each dataset
    for j in range(1, df.shape[1]):
        y_data = df.iloc[:, j].values
        c_inf = c_inf_all.iloc[j - 1]

        # Define the model function for curve fitting
        def regressor_model(t, c0, k):
            return c_inf - (c_inf - c0) * np.exp(-k * t)

        initial_guess = [y_data[0], 0.001]  # c0 - initial concentration, k - growth rate
        popt, _ = curve_fit(regressor_model, t, y_data, p0=initial_guess)
        c.append(popt)

    # Getting growth rate values as slopes
    slopes = []
    for i in range(0, 4):
        slopes.append(c[i][1])
    time = df['time']

    # Calculating the C equation in (A+B)/(C+D)
    tail_sum = []
    for j in range(0, 4):
        h = []
        for i in range(n - 1):
            concentration = yFit[:, j]
            f = (abs(1 - (concentration[i] + concentration[i + 1]) / (2 * c_inf_all.iloc[j])) * (
                        time[i + 1] - time[i])) * \
                c_inf_all.iloc[j]
            h.append(f)
        tail_sum.append(sum(h))

    # Weighted area under the curve | Calculating the A equation in (A+B)/(C+D)
    weighted_tail_sum = []
    for j in range(0, 4):
        h = []
        for i in range(0, n - 1):
            concentration = yFit[:, j]
            f = abs(
                (1 - (concentration[i] + concentration[i + 1]) / (2 * c_inf_all.iloc[j])) * (time[i] - time[i + 1]) * (
                        time[i] + time[i + 1]) / 2) * c_inf_all.iloc[j]
            h.append(f)
        weighted_tail_sum.append(sum(h))

    # Calculating the B equation in (A+B)/(C+D)
    weighted_tail = []
    for j in range(4):
        for i in range(n - 1):
            concentration = yFit[:, j]
            weight_t = (1 - (concentration[n - 1] / c_inf_all.iloc[j])) * (
                    (time[n - 1] / slopes[j]) + 1 / (pow(slopes[j], 2)))
        weighted_tail.append(weight_t)

    # Calculation of D
    D = []
    for j in range(0, 4):
        concentration = yFit[:, j]
        d = (1 - (concentration[n - 1] / c_inf_all.iloc[j])) / slopes[j]
        D.append(d)

    # Mean age of air
    Tau = []
    for j in range(0, 4):
        Taus = (weighted_tail_sum[j] + weighted_tail[j]) / (tail_sum[j] + D[j])
        where = points[j]
        Tau.append(Taus)
        print(P + 'Step Up Mean age of air at %s:' % where, np.round(Taus, 3))

    # Nominal air change time
    nTau = []
    for j in range(0, 4):
        where = points[j]
        nTaus = (tail_sum[j] + D[j]) / concentration[-1]
        nTau.append(nTaus)
        print(W + 'Step Up Nominal air change time at %s:' % where, np.round(nTaus, 3))

     # global Air change efficiency, %
    air_eff = []
    for j in range(0, 4):
        where = points[j]
        air_effs = 100 * (nTau[2]) / (2 * Tau[2])  # Tau[outlet]/2tau[j]
        air_eff.append(air_effs)
        print(O + 'Step Up globale Air change efficiency at %s:' % where, np.round(air_effs, 3), '%')

    # local Air change efficiency, %
    air_eff = []
    for j in range(0, 4):
        where = points[j]
        air_effs = 100 * (nTau[2]) / (nTau[j]) # Tau[outlet]/tau[j]
        air_eff.append(air_effs)
        print(O + 'Step Up local Air change efficiency at %s:' % where, np.round(air_effs, 3), '%')

    # Turn Over Time, %
    turn_over = []
    for j in range(0, 4):
        h = []
        for i in range(0, n - 1):
            where = points[j]
            concentration = yFit[:, j]
            f = abs((1 - (concentration[i] + concentration[i + 1]) / (2 * concentration[n - 1])) * (
                    time[i + 1] - time[i]))
            h.append(f)
        turn_over.append(sum(h))
        print(Fore.YELLOW + 'Step Up Turn over time at %s:' % where, np.round(turn_over[j], 3))
    print('-------------')

    # Plotting each dataset with its fitted model and equation
    for j in range(0, 4):
        where = points[j]
        c_inf = c_inf_all.iloc[j]
        plt.plot(df['time'], df.iloc[:, j + 1].values, 'r', label="Experimented")
        plt.plot(df['time'], regressor_model(t, *c[j]), label="Fitted")
        plt.xlabel('Time[s]')
        plt.ylabel('Concentration [ppm]')
        plt.title('Step Up Measured at %s' % where)
        plt.legend()

        # Displaying the fitted equation
        # fitted_eq = r'$c(t) = %.3f + (%.3f - %.3f) \cdot e^{-%.3f t}$' % (c[j][0], c_inf, c[j][0], c[j][1])
        # plt.text(0.05, 0.95, fitted_eq, transform=plt.gca().transAxes, fontsize=10,
        #         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

        plt.show()

# data = pd.read_csv("up.csv")
# step_up_calculator(data)

