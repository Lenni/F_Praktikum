import matplotlib.pyplot as plt
import csv
import numpy as np
from itertools import *

inp = open("data/T20/discriminator.csv", "r")
alls = csv.DictReader(inp, delimiter=",")

cnt_1 = list()
cnt_2 = list()
cnt_ges = list()
vol = list()

all_data = list()

for row in alls:
    all_data.append((float(row['Discr_Voltage[mV]']), float(row['Count 1']),
        float(row['Count 2'])))


vol = [a[0] for a in all_data]
cnt_1 = [a[1] for a in all_data]
cnt_2 = [a[2] for a in all_data]

plt_1 = plt.plot(np.array(vol), (np.array(cnt_1)), label="Ergebnisse Röhre 1")
plt_2 = plt.errorbar(np.array(vol), (np.array(cnt_2)), label="Ergebnisse Röhre 2")
plt.legend()
plt.show()
