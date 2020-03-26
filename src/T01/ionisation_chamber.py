from src.common.fitting import *
from src.common.plot_with_residuum import *

import numpy as np

import matplotlib.pyplot as plt

import csv
import os

ppath = "protocols/T01/Plots/ionisation_chamber"
if not os.path.exists(ppath):
    os.makedirs(ppath)

distance = list()
distance_err = list()
current = list()
current_err = list()
for row in csv.reader(open("data/T01/ion_chamber.csv")):
    distance.append(float(row[0].strip()))
    distance_err.append(0.01)
    current.append(float(row[1].strip()))
    current_err.append(float(row[2].strip()))
distance =np.array(distance)
distance_err =np.array(distance_err)
current =np.array(current)
current_err =np.array(current_err)

plt.errorbar(max(distance) - distance, current, current_err, distance_err, capsize=1, linewidth=2,
    elinewidth=1, color="r")
plt.xlabel("Distance /cm")
plt.ylabel("Current /mA")
plt.title("Ionisation Chamber - Shielding in Air")
plt.axvspan(3.0, 4.1, color='r', alpha=0.3, label="Plateau")

x_0 = 5.0
plt.axvline(x_0, color='blue', label="max. range {} cm".format(x_0))

plt.legend()

plt.grid(True)
plt.savefig("{}/CurrentToDistance.png".format(ppath))
plt.close('all')

