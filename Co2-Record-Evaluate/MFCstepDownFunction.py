# -*- coding: utf-8 -*-
"""
@author: Amin Darbandi
aathome@duck.com
For HRI
"""

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

O = '\033[36m'  # orange
W = '\033[0m'  # white (normal)
P = '\033[35m'  # purple


def step_down_calculator(df):
    # Initialization and parameters
    n = len(df["time"])

    t = df['time'].values
    yFit = df.iloc[:, 1:5].values
    points = ['VYU', 'VYV', '21kv', 'VZ2']  # Location points based on the data columns

    # Regression model for curve fitting
    def regressor_model(t, c0, k):
        """
        :param t: time
        :param c0: initial concentration
        :param k: decay constant
        :return: exponential decay model
        """
        return c0 * np.exp(-k * t)

    # Curve fitting to get decay constants
    c = []
    for i in range(1, df.shape[1]):
        y_data = df.iloc[:, i].values
        initial_guess = [y_data[0], 0.001]
        popt, _ = curve_fit(regressor_model, t, y_data, initial_guess)
        c.append(popt)

    # Getting not absolute value of decay constants
    slopes = []
    for i in range(4):
        slopes.append(c[i][1]*-1)

    # Weighted area under the curve | Calculating the A equation in (A+B)/(C+D)
    weighted_tail_sum = []
    for j in range(4):
        h = []
        for i in range(n - 1):
            concentration = yFit[:, j]
            f = abs(((concentration[i + 1] + concentration[i]) / 2)) * (t[i + 1] - t[i]) * ((t[i] + t[i + 1]) / 2)
            h.append(f)
        weighted_tail_sum.append(sum(h))

    # Calculating the B equation in (A+B)/(C+D)
    weighted_tail = []
    for j in range(0, 4):
        concentration = yFit[:, j]
        weighted_t = (concentration[-1] / slopes[j]) * ((1 / slopes[j]) + t[-1])
        weighted_tail.append(weighted_t)

    # Calculating the C equation in (A+B)/(C+D)
    tail_sum = []
    for j in range(0, 4):
        h = []
        concentration = yFit[:, j]
        for i in range(0, n - 1):
            f = abs(((concentration[i + 1] + concentration[i]) / 2)) * (t[i + 1] - t[i])
            h.append(f)
        tail_sum.append(sum(h))

    # Calculation of D
    D = []
    for j in range(4):
        concentration = yFit[:, j]
        d = concentration[-2] / slopes[j]
        D.append(d)

    # Mean age of air
    Tau = []
    for j in range(4):
        Taus = (weighted_tail_sum[j] + weighted_tail[j]) / (tail_sum[j] + D[j])
        Tau.append(Taus)
        print('Step Down Mean age of air at %s:' % points[j], np.round(Taus, 3))

    # Nominal air change time
    nTau = []
    for j in range(4):
        nTaus = (tail_sum[j] + D[j]) / concentration[0]
        nTau.append(nTaus)
        print('Step Down Nominal air change time at %s:' % points[j], np.round(nTaus, 3))

    # global Air change efficiency, %
    air_eff = []
    for j in range(0, 4):
        where = points[j]
        air_effs = 100 * (nTau[2]) / (2 * Tau[2])  # Tau[auslass]/2tau[j]
        air_eff.append(air_effs)
        print(O + 'Step down globale Air change efficiency at %s:' % where, np.round(air_effs, 3), '%')

    # local Air change efficiency, %
    air_eff = []
    for j in range(4):
        air_effs = 100 * (nTau[2]) / (nTau[j])  # Tau[outlet]/tau[p]
        air_eff.append(air_effs)
        print('Step Down Air change efficiency at %s:' % points[j], np.round(air_effs, 3), '%')

    # Turn Over Time, %
    turn_over = []
    time = df['time'].values
    for j in range(4):
        h = []
        for i in range(n - 2):
            concentration = yFit[:, j]
            # Check if concentration[n-1] is zero and handle it to avoid division by zero
            time_diff = time[i + 1] - time[i]
            f = abs(
                ((concentration[i] + concentration[i + 1]) / (2 * concentration[0])) * time_diff
            )
            h.append(f)
        turn_over.append(sum(h))
        print('Step Down Turn over time at %s:' % points[j], np.round(turn_over[j], 3))

    print('-------------')

    # Visualize fitted curves

    for j in range(4):
        plt.plot(df['time'], df.iloc[:, j + 1].values, label="Experimental")
        plt.plot(df['time'], regressor_model(t, *c[j]), label="Fitted")
        plt.xlabel('Time')
        plt.ylabel('Concentration [ppm]')
        plt.title('Step Down Measured at %s' % points[j])
        plt.legend()
        plt.show()



