# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""
import matplotlib.pyplot as plt
import numpy as np

# Reaction time calculation
steps = np.arange(1, 13)  #  12 pulse

# Sensor Data
VYU = [
    [105, 74, 100, 42, 145, 45, 92, 56, 140, 128, 50, 71],
    [107, 49, 25, 36, 148, 23, 32, 19, 142, 85, 59, 57],
    [86, 32, 109, 42, 143, 49, 92, 50, 156, 75, 36, 3]
]
VYV = [
    [168, 204, 101, 106, 105, 167, 93, 181, 184, 189, 118, 197],
    [119, 223, 100, 162, 110, 202, 114, 165, 140, 211, 160, 151],
    [99, 205, 119, 225, 98, 123, 118, 155, 188, 214, 215, 129]
]
_21kv = [
    [7, 41, 43, 41, 53, 40, 38, 34, 57, 60, 46, 26],
    [19, 83, 42, 41, 15, 57, 119, 95, 46, 34, 100, 49],
    [41, 76, 47, 17, 62, 86, 61, 28, 44, 17, 58, 91]
]
VZ2 = [
    [123, 32, 127, 129, 112, 65, 128, 49, 65, 110, 92, 104],
    [48, 29, 124, 111, 70, 75, 41, 9, 50, 79, 78, 106],
    [47, 110, 31, 97, 63, 100, 53, 27, 58, 86, 56, 85]
]


# Find the average and Std
def std_finder(data, name):
    data = np.array(data)
    average = data.mean(axis=0)
    std = data.std(axis=0)

    # results
    print(f"Sensor: {name}")
    for i, (mw, s) in enumerate(zip(average, std)):
        print(f"Phase {i + 1}: {mw:.2f} {s:.2f}")
    print("-" * 50)

    return average, std


#  Find the average and Std
VYU_average, VYU_std = std_finder(VYU, "VYU")
VYV_average, VYV_std = std_finder(VYV, "VYV")
_21kv_average, _21kv_std = std_finder(_21kv, "21kv")
VZ2_average, VZ2_std = std_finder(VZ2, "VZ2")

# box plot setting
width = 0.2
fig, ax = plt.subplots(figsize=(12, 6))

# std and average
ax.bar(steps - width * 1.5, VYU_average, width, yerr=VYU_std, label="VYU", capsize=3)
ax.bar(steps - width / 2, _21kv_average, width, yerr=_21kv_std, label="21kv", capsize=3)
ax.bar(steps + width / 2, VZ2_average, width, yerr=VZ2_std, label="VZ2", capsize=3)
ax.bar(steps + width * 1.5, VYV_average, width, yerr=VYV_std, label="VYV", capsize=3)

ax.set_ylim([0, 30])
ax.set_xlabel('Step-up,  Step-down', fontsize=20)
ax.set_ylabel('Reaction time [s]', fontsize=20)
ax.set_title('Reaction time in different phases', fontsize=22)
ax.set_xticks(steps)
ax.set_xticklabels([f' {i}' for i in steps])
ax.legend(title="Sensors", fontsize=13, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tick_params(axis='both', which='major', labelsize=18)
plt.tick_params(axis='both', which='minor', labelsize=18)
#
plt.tight_layout()
plt.show()













