

import sys
import os
sys.path.append(os.environ["PWD"])


import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

from src.common.fitting import *
from src.common.plot_with_residuum import *

from itertools import *

try:
    os.mkdir(os.environ["PWD"] + "/protocols/M21/Plots/Time/")
except:
    pass
print("check for folder")

plt.figure(figsize=(8,6), dpi=1200)

name_labels = list()
name_labels.extend([str(i+1) + ". Postionsmessung" for i in range(4)])
name_labels.append("Positionenkalibrierung")
names = ["TDS_1.log", "TDS_2.log", "TDS_3.log",
    "TDS_4.log", "TDS_Cal.log"]
TDS_Names = ["data/M21/Time/" + s for s in names]
print(TDS_Names)
td_mittelwert=list()
opts = list()
covs = list()
chi_sq = list()
timess=list()
countss=list()
for i, (path, name) in enumerate(zip(TDS_Names, map(lambda x: x.replace(". ", "_"), name_labels))):
    data = open(path, "r").read()
    def finish_split(x_str):
        return (float(x_str[0].strip()), float(x_str[1].strip()))
    tuple_x_y = [ finish_split(x_y.split(","))  for x_y in  data.split(";")[1:-1]]
    tuple_x_y = [ txy for txy in tuple_x_y if txy[1] != 0]
    times = np.array([txy[0] for txy in tuple_x_y])
    time_err = np.ones(len(times)) * 10 / np.sqrt(12)
    counts = np.array([txy[1] for txy in tuple_x_y])
    popt, pcov, chisq = do_normal_regression(times, counts, np.sqrt(np.array(counts)), xErr=None)

    mu = popt[0]
    sigma = popt[1]

    data = plt.subplot2grid((3,1), (0, 0), rowspan=2)
    res = plt.subplot2grid((3,1), (2, 0), rowspan=1)
    plot_with_residuum(times, time_err, counts, np.sqrt(counts), normal(times, *popt),
        "Koinzidenz " + name_labels[i]  , "zeitlicher Abstand ps", "Ereignisse", data, res );
    plt.savefig("protocols/M21/Plots/Time/" + name + ".png")
    plt.clf()
    plt.close('all')

    #
    # Take 3 sigma interval
    #
    #
    tuple_x_y = [(t, c, te) for (t, c, te) in zip(times, counts, time_err) if
                    t >= mu - 1.5* abs(sigma) and t <= mu + 1.5 * abs(sigma)]

    times = np.array([txy[0] for txy in tuple_x_y])
    time_err = np.array([txy[2] for txy in tuple_x_y])
    counts = np.array([txy[1] for txy in tuple_x_y])
    timess.append(times)
    countss.append(counts)
    popt, pcov, chisq = do_normal_regression(times, counts, np.sqrt(np.array(counts)), xErr=None)
    data = plt.subplot2grid((3,1), (0, 0), rowspan=2)
    res = plt.subplot2grid((3,1), (2, 0), rowspan=1)
    plot_with_residuum(times, time_err, counts, np.sqrt(counts), normal(times, *popt),
        "Koinzidenz " + name_labels[i] + " - 2 $\sigma$ Intervall", "zeitlicher Abstand ps", "Ereignisse", data, res );
    plt.savefig("protocols/M21/Plots/Time/Sel" + name + ".png")
    plt.clf()
    plt.close('all')
    opts.append(popt)
    covs.append(np.sqrt(np.diag(pcov)))
    chi_sq.append(chisq) #np.sum((normal(times, *popt) - counts)**2 / np.sqrt(counts) )/(len(counts) - 3))
    td_mittelwert.append(mu)
td_mittelwert=np.array(td_mittelwert)

#
# erstelle plot aller histogramme
#
#
plt.figure(figsize=(12,9), dpi=1200)
for (t, c, n) in zip(timess, countss, name_labels):
    mc = list()
    for (a, b) in  zip(t,c):
        for i in range(int(b)):
            mc.append(a)

    bins = list()
    i=0
    many = 5
    while i * many < len(t):
        bins.append(times[i*many])
        i = i + 1
    bins.append(t[-1])
    plt.hist(np.array(mc), t, label=n, histtype='step')
plt.legend()
plt.xlabel("Zeitdifferenzen ps")
plt.ylabel("Ereignisse")
plt.title("Alle Zeitkoinzidenzmessungen")
plt.savefig("protocols/M21/Plots/timeDiffAll.png")
plt.clf()


#
# Fitparameter ausgeben und fwhd angeben
#
#
#
fwhm = list()
for i in range(len(opts)):
    f = np.sqrt(2*np.log(2)) * opts[i][1]
    fe = np.sqrt(2*np.log(2)) * covs[i][1]
    print("mittelwert: {:10e} \pm {:10e} ps \t abweichung: {:10e} \pm {:10e} ps \t fwhd: {:10e} \pm {:10e} ps \t \chi^2: {:10e}".format(
            opts[i][0], covs[i][0], opts[i][1], covs[i][1], f, fe, chi_sq[i]))
    fwhm.append(f)

td_error = np.array(fwhm)
