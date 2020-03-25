
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

from src.common.fitting import *
from src.common.plot_with_residuum import *

import csv
import os

rc("text", usetex=True)

ticks_many = 9

path = "protocols/LAB/Plots/zener"
if not os.path.exists(path):
    os.makedirs(path)

resistors = [47, 100, 4700, 10000]
arbeitspunkte = [(-3, -2.9), (-3.3, -3.25), (-2.8, -2.75), (-2.5, -2.45)]

print("Systematiken der Widerstandbestimmungsplots sind egal, weil es sich um eine Tangentensteigung als Näherung handelt. Es ist klar, dass das Modell und die Daten nicht zusammenpassen.")

for r, (low_a, high_a) in zip(resistors, arbeitspunkte):
    uin = list()
    uout = list()
    ir = list()

    for row in csv.reader(open("data/LAB/Zener/zener_{}.txt".format(r)), delimiter="\t"):
        uin.append(float(row[1].strip()))
        uout.append(float(row[0].strip()))
        ir.append(float(row[2].strip()))

    uin = np.array(uin)
    uout = np.array(uout)
    ir = np.array(ir)

    plt.figure(figsize=(8,6), dpi=1200)
    plt.plot(uin, uout)
    plt.xticks(np.arange(uin[0], uin[-1], (uin[-1] - uin[0])/ticks_many))
    plt.yticks(np.arange(uout[0], uout[-1], (uout[-1] - uout[0])/ticks_many))
    plt.ylabel("Eingangsspannung /V")
    plt.xlabel("Ausgangsspannung /V")
    plt.grid(True)
    plt.axvspan(low_a, high_a, label="Arbeitsbereich", alpha=0.4)
    plt.title("Z-Dioden mit Widerstand {} $\Omega$, Kennlinie".format(r))
    plt.tight_layout()
    plt.legend()
    plt.savefig(path + "/spannungenZener_{}.png".format(r))
    plt.clf()

    xs = list()
    ys = list()
    xs_err = list()
    ys_err = list()

    for (x, y) in filter(lambda x: x[0] >= low_a and x[0] <= high_a, zip(uin, uout)):
        xs.append(x)
        ys.append(y)
        xs_err.append(0.001 / np.sqrt(12))
        ys_err.append(0.001 / np.sqrt(12))

    xs = np.array(xs)
    ys = np.array(ys)
    xs_err = np.array(xs_err)
    ys_err = np.array(ys_err)

    lin_func = lambda x, m, c: m*x+c
    opt, cov, chi_sq = regression(lin_func, xs, ys, ys_err, xErr=xs_err)
    glaett = opt[0] * lin_func(xs[int(len(xs)/2)], *opt) / xs[int(len(xs)/2)]
    glaett_err = np.sqrt(cov[0][0]) * lin_func(xs[int(len(xs)/2)], *opt) / xs[int(len(xs)/2)]
    print("""Differentieller Widerstand, Zener Diode mit Widerstand {}
Widerstand\t: {:.3e} \pm {:.3e} Ohm
Achsenabschnitt\t: {:.3e} \pm {:.3e} Ampere
chi_sq\t\t: {:.3e}
Glättungsfaktor\t: {:.3e} \pm {:.3e} \n\n""".format(r, opt[0], np.sqrt(cov[0][0]), opt[1], np.sqrt(cov[1][1]), chi_sq, glaett, glaett_err))
    simple_figure(xs, xs_err, ys, ys_err, lin_func(xs, *opt), "Glättungsfaktor bei {} $\Omega$".format(r),
        "Ausgangsspannung /V", "Eingangsspannung /V", path + "/diff_res_{}.png".format(r))
