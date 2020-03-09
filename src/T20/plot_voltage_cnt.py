import matplotlib.pyplot as plt
import csv
import numpy as np
from itertools import *

inp = open("data/T20/voltage.csv", "r")
alls = csv.DictReader(inp, delimiter=",")

cnt_1 = list()
cnt_2 = list()
cnt_ges = list()
vol = list()

all_data = list()

for row in alls:
    all_data.append((float(row['Voltage [V]']), float(row['Count_PMT_1 [1]']), 
        float(row['Count_PMT_2 [1]'])))

all_data.sort(key=lambda x: x[0])
for v, cnts in groupby(all_data, lambda x: x[0]):
    vol.append(v)
    a_min = min([c[1] for c in cnts])
    b_min = min([c[2] for c in cnts])
    cnt_1.append(a_min)
    cnt_2.append(b_min)
    cnt_ges.append(a_min + b_min)

plt_1 = plt.plot(np.array(vol), np.log(np.array(cnt_1)), label="Ergebnisse Röhre 1")
plt_2 = plt.errorbar(np.array(vol), np.log(np.array(cnt_2)), label="Ergebnisse Röhre 2")
plt_ges = plt.errorbar(np.array(vol), np.log(np.array(cnt_ges)), label="Ergebnisse beider Röhren")
plt.legend()
plt.show()
