from src.common.fitting import *
from src.common.plot_with_residuum import *

from itertools import *

from tqdm import tqdm

import matplotlib.pyplot as plt

import csv

import numpy as np


def integrate(data, lower, upper):
    range = np.arange(0, upper-lower, 1)
    integrated = []
    for i in range:
        integrated.append(1000*0.001*np.sum(data[lower:lower+i]))
    integrated = np.array(integrated) / np.sum(data[lower:upper])
    return integrated

ppath = "protocols/T01/Plots/HalbleiterDetektor"
import os
if not os.path.exists(ppath):
    os.makedirs(ppath)

print("Stelle ein Spektrum da")
counts = np.array(list(map(lambda x: int(x.strip()), open("data/T01/Experiment 1/1/spectrum_central.TKA").read().split("\n")[2:-1])))
plt.figure(figsize=(8,6), dpi=1200)
plt.plot(np.array(list(range(len(counts)))) + 1, counts)
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("Sample in centered postion")
plt.savefig("{}/CenteredPosition.png".format(ppath))
plt.close('all')

print("Äquvalenzdicke")
linf = lambda x, m, c: m*x+c
abs_energy = np.array([4.78, 5.35, 6.0, 7.69])
abs_pos = 25.1 - np.array([25.15, 24.25, 23.45, 21.15])
opt, cov, chi_sq = regression(linf, abs_energy, abs_pos, 0.05 * np.ones(len(abs_pos)))

print("""Steigung:\t {} \pm {}
Abschn:\t {} \pm {}
chi_sq:\t {}""".format(opt[0], np.sqrt(cov[0][0]), opt[1], np.sqrt(cov[1][1]), chi_sq))

print("Äquivalenzdicke: {} \pm {}".format(-1.0 * opt[1], np.sqrt(cov[1][1])))

simple_figure(abs_energy, None, abs_pos, 0.05 * np.ones(len(abs_pos)), linf(abs_energy, *opt),
   "Lineary Shielding", "Energy MeV", "distance cm", "{}/liearyShielding.png".format(ppath))

print("Detektorkalibrierunng")
counts = list(map(lambda x: int(x.strip()), open("data/T01/Experiment 1/2/spectrum_closest.TKA").read().split("\n")[2:-1]))
plt.figure(figsize=(8,6), dpi=1200)
plt.plot(np.array(list(range(len(counts)))) + 1, counts)
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("Sample in closest postion")

peak_energies = np.array([4.78, 5.4, 6.0, 7.69])
channel_ranges = np.array([(250, 500), (600, 800), (900, 1050), (1600, 1800)])

for (ener, (start, stop), col) in zip(peak_energies, channel_ranges, ['r', 'g', 'b', 'orange']):
    plt.axvspan(start, stop, label="{} MeV Peak".format(ener), alpha=0.3, color=col)

mus = list()
sigmas = list()
print("Fitte gauskurve an peaks an")
print("mu\t sigma\t chi_sq")
for (energy, (start, end)) in zip(peak_energies, channel_ranges):
    opt, cov, chi_sq = do_normal_regression(np.arange(start, end, 1), counts[start:end], np.sqrt(counts[start:end]), xErr=np.ones(len(counts[start:end])))
    plt.axvline(opt[0])
    mus.append(opt[0])
    sigmas.append(opt[1])
    print("{:.3e}\t {:.3e}\t {:.3e}".format(mus[-1], sigmas[-1], chi_sq))
plt.savefig("{}/ClosestPostion.png".format(ppath))
plt.close('all')

linf = lambda x, m, c: m*x+c
mus = np.array(mus)
sigmas = np.array(sigmas)
kalib_opt, kalib_cov, chi_sq = regression(linf, peak_energies, mus, sigmas/3)
kalibMax = np.array([1.0/kalib_opt[0], -1.0 * kalib_opt[1]/kalib_opt[0]])
kalibMaxCov = np.array([1.0/kalib_opt[0] **2 *np.sqrt(kalib_cov[0][0]),
        (np.sqrt(kalib_cov[1][1])/kalib_opt[0])**2 + kalib_opt[1] /kalib_opt[0]**2 * np.sqrt(kalib_cov[0][0])])
print("Energie kalibrierung")
print(kalibMax)
print(np.sqrt(np.diag(kalibMaxCov)))
print(chi_sq)

simple_figure(mus, sigmas, peak_energies, np.zeros(len(mus)), linf(mus, *kalibMax), "Energy Calibration",
    "Channel", "Energy MeV", "{}/energyCalibrationClosest.png".format(ppath))

#
# highest peak energy per peak
#
#
#load data
plt.close('all')


eventsl = []

threshold = 2
shield_data = [list() for i in range(4)]
for mes_dist in tqdm(chain(range(2150, 2400, 40), [2475])):
    events = np.array(list(map(lambda x: float(x.strip()), open("data/T01/Experiment 1/4/spectrum_{}.TKA".format(mes_dist)).read().split("\n")[2:-1])))
    eventsl.append(events)
    plt.figure(figsize=(8, 6), dpi=1200)
    plt.plot(list(range(len(events))), events)
    upper_idx = 4093
    while events[upper_idx] < 10 * threshold:
        upper_idx = upper_idx - 1
    lower_idx = upper_idx
    while events[lower_idx] > threshold:
        lower_idx = lower_idx - 1

    integd = integrate(events, lower_idx, upper_idx)

    print("Distance in cm:", integd[-1])

    local_opt, local_cov, local_chi_sq = do_normal_regression(np.array(list(range(lower_idx, upper_idx))),
        np.array(events[lower_idx:upper_idx]), np.array(np.sqrt(events[lower_idx:upper_idx])))
    print("mittelwert: {} \pm {}, Fehler: {} \pm {}, chi_sq: {}".format(local_opt[0], local_opt[1],
        np.sqrt(local_cov[0][0]), np.sqrt(local_cov[1][1]), chi_sq))
    shield_data[0].append(25.1 - (mes_dist / 100.0))
    shield_data[1].append(np.sqrt(0.01 ** 2 + 0.1 ** 2))
    shield_data[2].append(local_opt[0])
    shield_data[3].append(local_opt[1])
    plt.axvspan(lower_idx, upper_idx, alpha=0.6)
    #plt.show()
    plt.close('all')



distance = np.array(shield_data[0])
distance_err = np.array(shield_data[1])
channel = np.array(shield_data[2])
channel_err = np.array(shield_data[3])


distance = distance[0:-2]
distance_err = distance_err[0:-2]
channel =  channel[0:-2]
channel_err = channel_err[0:-2]

mod_func = lambda x, m, b: m*x + b
kalibDis, kalibDisErr, chi_sq = regression(mod_func, distance, channel, channel_err, xErr = distance_err)
simple_figure(distance, distance_err, channel, channel_err, mod_func(distance, *kalibDis), "Distance Calibration, 7.69 MeV",
    "Distance /cm", "Channel", "{}/dis_calib.png".format(ppath))

print(kalibDis)

distance_left = (channel - kalibDis[1])/kalibDis[0]

nist_table = []

#Now find energy values for this distance

with open("data/T01/nist_table") as csvfile:
    reader = csv.reader(csvfile, delimiter = " ")
    for row in tqdm(reader):
        nist_table.append(np.array([float(row[0]), float(row[1]), float(row[2])]))

nist_table = np.array(nist_table)

energy_left_ind = []

for distances in distance_left:
    energy_left_ind.append(min(nist_table[:,2], key=lambda x:abs(x-distances*0.001)))#Auf Luftdichte normalisieren

energy_left_ind = np.array(energy_left_ind)

properties_energy = []
for element in energy_left_ind:
    for row in tqdm(nist_table):
        if row[2] == element:
            properties_energy.append(row)

properties_energy = np.array(properties_energy)

distance = np.flip(distance)
channel = np.flip(channel)
channel_err = np.flip(channel_err)

kalibEn, kalibEnErr, chi_sq = regression(mod_func, channel, properties_energy[:,0], 0.5*np.ones(len(properties_energy)), xErr = channel_err)
simple_figure(channel, channel_err, properties_energy[:,0], 0.5*np.ones(len(properties_energy)), mod_func(channel, *kalibEn), "Energy Calibration, 7.69 MeV",
    "Channel", "Energy MeV", "{}/dis_energy_calib.png".format(ppath))

print(kalibEn)
print(kalibEnErr)

j = 0
for events in eventsl:
    lower = int(shield_data[2][j] - 2*shield_data[3][j])
    upper = int(shield_data[2][j]+ 2*shield_data[3][j])

    sum = [0]
    sum_en = [0]

    for channel in np.arange(0, upper):
        energy = mod_func(channel, *kalibEn)

        match = min(nist_table[:, 0], key=lambda x: abs(x - energy))

        for row in nist_table:
            if row[0] == match:
                stopping_power = float(row[1])*0.001

        sum.append(sum[-1] + kalibEn[0]/stopping_power)
        sum_en.append(sum_en[-1] + kalibEn[0])

        print(sum[-1])

    j = j+1