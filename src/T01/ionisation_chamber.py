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
distance = max(distance) - distance
plt.figure(figsize=(8,6), dpi=1200)
plt.errorbar(distance, current, current_err, distance_err, capsize=1, linewidth=2,
    elinewidth=1, color="r")
plt.xlabel("Distance /cm")
plt.ylabel("Current /mA")
plt.title("Ionisation Chamber - Shielding in Air")
plt.axvspan(3.0, 4.1, color='r', alpha=0.3, label="Plateau")

x_0 = 5.0
plt.axvline(x_0, color='blue', label="max. range {} cm".format(x_0))


plt.grid(True)


print("Maximale Höhe aus y Mittelwert der Plateaus")
filter_ys = np.array([y for (x, y) in zip(distance, current) if 3.0 <= x and x<=4.1])
y_max = sum(filter_ys)/len(filter_ys)
print(filter_ys)
y_max_err = sum(np.sqrt((filter_ys - y_max)**2 / (len(filter_ys)-1)))
y_searched = y_max/2
y_searched_err = 0

m_tan = (current[-2] - current[-3])/(distance[-2] - distance[-3])
m_tan_err= np.sqrt(((current_err[-3])**2 + (current_err[-2]**2))/(distance[-2] - distance[-3])**2 +((current[-2] - current[-3])/(distance[-2] - distance[-3])**2 * distance_err[-2])**2)
print("m_tan : {} \pm {}".format(m_tan, m_tan_err))
c = current[-3] - m_tan*distance[-3]
c_err = 0

avr_rng = (y_searched - c)/m_tan
avr_rng_err = np.sqrt((c/m_tan * y_searched_err)**2 + (y_searched/m_tan*c_err) **2+ ((y_searched - c)/m_tan**2 * m_tan_err)**2)

plt.axhline(y_max, color='cyan', label="plateau level")
plt.axhline(y_searched, color='orange', label="half of plateau")
plt.axvline(avr_rng, color='orange', label="averange range")
plt.plot(distance[-6:], m_tan*distance[-6:] + c, label="tangent line", alpha=0.6)

plt.legend()
plt.savefig("{}/CurrentToDistance.png".format(ppath))
plt.close('all')

print(avr_rng)
print(avr_rng_err)
print("mess max range: {:.3e} \pm {:.3e} cm".format(avr_rng, avr_rng_err))
