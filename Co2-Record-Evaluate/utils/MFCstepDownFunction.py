# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
aathome@duck.com
For HRI

Step-down analysis: fits exponential decay, computes air change metrics, and plots results.
"""

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

O = '\033[36m'  # orange
W = '\033[0m'  # white (normal)
P = '\033[35m'  # purple

def step_down_calculator(df):
    n = len(df["time"])
    t = df['time'].values
    yFit = df.iloc[:, 1:5].values
    points = ['VYU', 'VYV', '21kv', 'VZ2']

    def regressor_model(t, c0, k):
        return c0 * np.exp(-k * t)

    c = []
    slopes = []
    for i in range(1, df.shape[1]):
        y_data = df.iloc[:, i].values
        initial_guess = [y_data[0], 0.001]
        try:
            popt, _ = curve_fit(regressor_model, t, y_data, initial_guess)
        except RuntimeError:
            popt = [y_data[0], 0.001]
        c.append(popt)
        slopes.append(-popt[1] if popt[1] != 0 else 1e-6)

    weighted_tail_sum, weighted_tail, tail_sum, D = [], [], [], []
    Tau, nTau, global_eff, local_eff, turn_over = [], [], [], [], []

    for j in range(4):
        conc = yFit[:, j]
        slope = slopes[j]

        h_wts = [abs(((conc[i + 1] + conc[i]) / 2)) * (t[i + 1] - t[i]) * ((t[i] + t[i + 1]) / 2)
                 for i in range(n - 1)]
        weighted_tail_sum.append(sum(h_wts))

        weighted_t = (conc[-1] / slope) * ((1 / slope) + t[-1])
        weighted_tail.append(weighted_t)

        h_ts = [abs(((conc[i + 1] + conc[i]) / 2)) * (t[i + 1] - t[i]) for i in range(n - 1)]
        tail_sum.append(sum(h_ts))

        d = conc[-2] / slope if slope != 0 else 0
        D.append(d)

        tau = (weighted_tail_sum[j] + weighted_tail[j]) / (tail_sum[j] + D[j])
        Tau.append(tau)
        print(f'Step Down Mean age of air at {points[j]}: {np.round(tau, 3)}')

        conc_start = conc[0] if conc[0] != 0 else 1e-6
        nominal_tau = (tail_sum[j] + D[j]) / conc_start
        nTau.append(nominal_tau)
        print(f'Step Down Nominal air change time at {points[j]}: {np.round(nominal_tau, 3)}')

    for j in range(4):
        eff_global = 100 * (nTau[2]) / (2 * Tau[2]) if Tau[2] != 0 else 0
        global_eff.append(eff_global)
        print(O + f'Step down global Air change efficiency at {points[j]}: {np.round(eff_global, 3)}%')

    for j in range(4):
        eff_local = 100 * (nTau[2]) / nTau[j] if nTau[j] != 0 else 0
        local_eff.append(eff_local)
        print(f'Step Down Air change efficiency at {points[j]}: {np.round(eff_local, 3)}%')

    for j in range(4):
        conc = yFit[:, j]
        h = [abs(((conc[i] + conc[i + 1]) / (2 * conc[0])) * (t[i + 1] - t[i])) for i in range(n - 2)]
        turn_over.append(sum(h))
        print(f'Step Down Turn over time at {points[j]}: {np.round(turn_over[j], 3)}')

    print('-------------')

    for j in range(4):
        plt.plot(df['time'], df.iloc[:, j + 1].values, label="Experimental")
        plt.plot(df['time'], regressor_model(t, *c[j]), label="Fitted")
        plt.xlabel('Time')
        plt.ylabel('Concentration [ppm]')
        plt.title(f'Step Down Measured at {points[j]}')
        plt.legend()
        plt.show()
