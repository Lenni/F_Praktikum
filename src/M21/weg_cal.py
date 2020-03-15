
import sys
sys.path.append("/Users/philipp/Workspace/F_Praktikum")


import sys
from sys import platform

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

from src.common.fitting import *
from src.common.plot_with_residuum import *

from itertools import *

import csv

def linf(x,m,c):
    return m * x + c

reader = csv.reader(open("data/M21/length_calibration.csv", "r"),
    delimiter = ",")

print("Weg Kalibrierung")
print("Kein Systematischer Fehler auf Länge, weil nicht bekannt")

motor_calib = list()
length = list()
for row in reader:
    motor_calib.append(float(row[0]))
    length.append(float(row[1]))
motor_calib = np.array(motor_calib)
length=np.array(length)
length_err = np.ones(len(length)) * 0.05 / np.sqrt(3)

opt, cov, chi_2 = regression(linf, motor_calib, length, yErr=length_err)

plt.figure(figsize=(8,6), dpi=1200)
dp = plt.subplot2grid((3,1), (0,0), rowspan=2)
rp = plt.subplot2grid((3,1), (2,0), rowspan=1)
plot_with_residuum(motor_calib, None, length, length_err, linf(motor_calib, *opt),
   "Motorkalibrierung", "Servoposition", "Länge am Lineal cm", dp, rp)
plt.savefig("protocols/M21/Plots/WegKalib.png")
plt.clf()

weg_m = opt[0]
weg_m_err = np.sqrt(cov[0][0])

weg_c = opt[1]
weg_c_err = np.sqrt(cov[1][1])

print("Wegkalibrierung: ({} \pm {} cm ) * x + ({} \pm {} cm) chi_sq: {}".format(
        weg_m, weg_m_err, weg_c, weg_c_err, chi_2))
