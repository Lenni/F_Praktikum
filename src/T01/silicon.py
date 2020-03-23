from src.common.fitting import *
from src.common.plot_with_residuum import *

import matplotlib.pyplot as plt

import numpy as np

ppath = "protocols/T01/Plots/HalbleiterDetektor"
import os
if not os.path.exists(ppath):
    os.makedirs(ppath)

print("Stelle ein Spektrum da")
counts = np.array(list(map(lambda x: int(x.strip()), open("data/T01/Experiment 1/1/spectrum_central.TKA").read().split("\n")[:-1])))
plt.figure(figsize=(8,6), dpi=1200)
plt.plot(np.array(list(range(len(counts)))) + 1, counts)
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("Sample in centered postion")
plt.savefig("{}/CenteredPostion.png".format(ppath))
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
   "Lineary Shilding", "Energy MeV", "distance cm", "{}/liearyShielding.png".format(ppath))

print("Detektorkalibrierunng")
counts = list(map(lambda x: int(x.strip()), open("data/T01/Experiment 1/2/spectrum_closest.TKA").read().split("\n")[:-1]))
plt.figure(figsize=(8,6), dpi=1200)
plt.plot(np.array(list(range(len(counts)))) + 1, counts)
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("Sample in closest postion")

peak_energies = np.array([4.78, 5.4, 6.0, 7.69])
channel_ranges = np.array([(250, 500), (600, 800), (950, 1050), (1600, 1800)])

for (ener, (start, stop), col) in zip(peak_energies, channel_ranges, ['r', 'g', 'b', 'orange']):
    plt.axvspan(start, stop, label="{} MeV Peak".format(ener), alpha=0.3, color=col)

for (energy, (start, end)) in zip(peak_energies, channel_ranges):
    opt, cov, chi_sq = do_normal_regression(np.arange(start, end, 1), counts[start:end])

plt.savefig("{}/ClosestPostion.png".format(ppath))
plt.close('all')
