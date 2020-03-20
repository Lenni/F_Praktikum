
from itertools import *
import csv
import os
import pdb

from src.common.fitting import *
from src.common.plot_with_residuum import *

if not os.path.exists("protocols/LAB/Plots/rectifier"):
    os.makedirs("protocols/LAB/Plots/rectifier")


import numpy as np
import matplotlib.pyplot as plt

data_reader = csv.DictReader(open("data/LAB/Rectifier/rectifier.txt"), delimiter='\t')

time = list()
u1 = list()
u2 = list()
for row in data_reader:
    time.append(float(row['Zeit [ms]'].strip()))
    u1.append(float(row['Uin B [V]'].strip()))
    u2.append(float(row['Uin A [V]'].strip()))
time = np.array(time)
u1 = np.array(u1)
u2 = np.array(u2)


plt.clf()
plt.figure(figsize=(8,6), dpi=1200)
plt.plot(time, u1, label="Eingangspannung")
plt.plot(time, u2, label="Ausgangspannung")
plt.legend()
plt.title("Rohdaten")
plt.xlabel("Zeit /s")
plt.ylabel("Spannung /V")
plt.savefig("protocols/LAB/Plots/rectifier/Rohdaten.png")
print(""" Um die Maximale Spannung herauszufinden werden einnzelne Sinusperioden an beide Signale angefittet
der statisische und systematische Fehler ist standardabweichung bzw. Mittelwert der nullbereiche""")


#
# get Frequency and phase to determine the actual error
#
zero_vals = np.array(list(map(lambda x: x[1], filter(lambda x: x[0] <= 0, zip(u1, u2)))))

vol_sys_err = np.sum(zero_vals) / len(zero_vals)
vol_stat_err = np.sqrt(np.sum((zero_vals - vol_sys_err)**2))/len(zero_vals) * np.ones(len(u1))

print("stat. Fehler\t:{:.3e}".format(vol_stat_err[0]))
print("sys. Fehler\t:{:.3e}".format(vol_sys_err))

#
# Rate Frequent
#
#
#
print("Rate Frequenz über Nullwerte der ausgangspannung")
threshd = 0.003
threshu = 0.02
intervals = list()
non_zero_cond = True
number = None
for (u, t) in iter(zip(u2, time)):
    if non_zero_cond:
        if u < threshd:
            print(u)
            number = t
            non_zero_cond = False
    else:
        if u > threshu:
            print(u)
            intervals.append((number, t))
            non_zero_cond = True
print(intervals)
freq = np.pi / (sum(map(lambda x: x[1] - x[0], intervals)) / len(intervals))
print(freq)

def sine_func(x, amp, phase):
    return np.sin(x*freq  + phase) * amp


#
#fitte den Sinus an
#
#
#
sopt, scov, schi_sq = regression(sine_func, time, u1, vol_stat_err, beta0=[2.0, 1.0])
print("""Eingangsspannungssinus
Amplitude\t: {:.3e} \pm {:.3e} Volt
Frequenz\t: {:.3e} \pm {:.3e} Hz
Phase\t\t: {:.3e} \pm {:.3e} eins
\chi^2/ndf\t: {:.3e} \n\n""".format(sopt[0], np.sqrt(scov[0][0]), sopt[1], np.sqrt(scov[1][1]), sopt[2], np.sqrt(scov[2][2]), schi_sq))

simple_figure(time, None, u1, vol_stat_err, sine_func(time, *sopt), "Eingangspannung Regression", "Zeit /s", "Spannung /V", "protocols/LAB/Plots/Rectifier/eingang.png")



print("Für die Ausgangsspannung werden werte kleiner als ein Threshold ignoriert. Auch hier wird ein Sinus angefittet")
thresh = 0.1
filtered_u2_time = list(filter(lambda x:x[1] > 0.1, zip(time, u2)))
fil_u2 = np.array(list(map(lambda x: x[1], filtered_u2_time)))
fil_time = np.array(list(map(lambda x: x[0], filtered_u2_time)))

ropt, rcov, rchi_sq = regression(sine_func, fil_time, fil_u2, vol_stat_err[0] * np.ones(len(fil_time)),  beta0=[2.0/1.2, 1.0])
print("""Eingangsspannungssinus
Amplitude\t: {:.3e} \pm {:.3e} Volt
Frequenz\t: {:.3e} \pm {:.3e} Hz
Phase\t\t: {:.3e} \pm {:.3e} eins
\chi^2/ndf\t: {:.3e} \n\n""".format(ropt[0], np.sqrt(rcov[0][0]), ropt[1], np.sqrt(rcov[1][1]), ropt[2], np.sqrt(rcov[2][2]), rchi_sq))

simple_figure(fil_time, None, fil_u2, vol_stat_err[0] *np.ones(len(fil_time)), sine_func(fil_time, *ropt), "Ausgangsspannung Regression", "Zeit /s", "Spannung /V", "protocols/LAB/Plots/Rectifier/ausgang.png")

print("Bereichnete Effektivspannung: {:.3e} \pm {:.3e}".format(sopt[0]/np.sqrt(2), np.sqrt(scov[0][0])/np.sqrt(2)))
print("Abweichung: {:.3e} \sigma".format(np.abs(ropt[0] - sopt[0])/np.sqrt(np.sqrt(scov[0][0])/2 + rcov[0][0])))
