import numpy as np
import matplotlib.pyplot as plt

import csv
import os

ppath = "protocols/LAB/Plots/schmitt"
if not os.path.exists(ppath):
    os.makedirs(ppath)

plt.figure(figsize=(8, 5), dpi=1200)
ein_ax = plt.subplot2grid((1,2), (0,0))
aus_ax = plt.subplot2grid((1,2), (0,1))

for file_n, title, vline_pos, ax in zip(["data/LAB/Schmitt/schmitt_{}.txt".format(a) for a in ["ein", "aus"]],
        ["Einschaltvorgang", "Ausschaltvorgang"], [2.73, 1.64], [ein_ax, aus_ax]):
    v_ein = list()
    v_aus = list()
    for row in csv.DictReader(open(file_n, "r"), delimiter='\t'):
        v_ein.append(float(row['v_ein'].strip()))
        v_aus.append(float(row['v_aus'].strip()))
    v_ein = np.array(v_ein)
    v_aus = np.array(v_aus)
    if ax is ein_ax:
        ax.plot(v_ein, v_aus)
        ax.axvline(vline_pos - 0.05, label="Schaltpunkt bei {:.2} V".format(vline_pos), alpha=0.5)
    else:
        ax.plot(-1.0 * v_ein + np.max(v_ein), v_aus)
        ax.set_xticks([0,2,4,6,8,10])
        ax.set_xticklabels([10, 8, 6, 4, 2, 0])
        ax.axvline(np.max(v_ein)-(vline_pos - 0.05), label="Schaltpunkt bei {:.2} V".format(vline_pos), alpha=0.5)
    ax.set_xlabel("Eingangsspannung /V")
    ax.set_ylabel("Ausgangsspannung /V")
    ax.set_title(title)
    ax.axhline(10.672, label="10.6 V, Hohes Niveau", color='r', alpha=0.3)
    ax.axhline(1.519, label="1.6 V, Tiefes Niveau", color='y', alpha=0.3)
    ax.set_yticks([0,2,4,6,8,10, 12])
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.savefig("{}/schmitt_trigger.png".format(ppath))
