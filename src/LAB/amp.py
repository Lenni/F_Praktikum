import numpy as np
import matplotlib.pyplot as plt

import os
import csv


ppath = "protocols/LAB/Plots/amp"
if not os.path.exists(ppath):
    os.makedirs(ppath)

data_set = list()
for i in [1, 2]:
    u1 = list()
    u2 = list()
    time = list()
    for row in csv.DictReader(open("data/LAB/Amplifier/amplifier_{}.txt".format(i)), delimiter='\t'):
        u1.append(float(row['Uin B [V]'].strip()))
        u2.append(float(row['Uin A [V]'].strip()))
        time.append(float(row["Zeit [ms]"].strip()))
    u1 = np.array(u1)
    u2 = np.array(u2)
    time = np.array(time)
    data_set.append((time, u1, u2))


descr = ["Ohne C3", "Mit C3"]
#
# Spannungs-Zeit Kurven
#
for ds,l in zip(data_set, descr):
    plt.figure(figsize=(8,6), dpi=1200)
    plt.plot(ds[0], ds[1], label="Eingangsspannung")
    plt.plot(ds[0], ds[2], label="Ausgangsspannung")
    plt.grid(True)
    plt.legend()
    plt.title("Spannung zur Zeit {}".format(l))
    plt.xlabel("Zeit /s")
    plt.ylabel("Spannung /V")
    plt.savefig("{}/SpannungGegZeit{}.png".format(ppath, l))
    plt.clf()
#
# Spannung-Spannung Kurve
#
plt.figure(figsize=(8,6), dpi=1200)
for ds,l in zip(data_set, descr):
    plt.plot(ds[1], ds[2], label=l)
plt.grid(True)
plt.legend()
plt.title("Eingangs- gegen Ausgansspannung".format(l))
plt.xlabel("Eingangsspannung /V")
plt.ylabel("Ausgangsspannung /V")
plt.savefig("{}/SpannungGegSpannung{}.png".format(ppath, l))
plt.clf()
