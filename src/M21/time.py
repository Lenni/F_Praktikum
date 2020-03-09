
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

names = ["TDS_1.log", "TDS_2.log", "TDS_3.log",
    "TDS_4.log", "TDS_Cal.log"]
TDS_Names = ["data/M21/Time/" + s for s in names]

opts = list()
covs = list()
chi_sq = list()
for path, name in zip(TDS_Names, names):
    data = open(path, "r").read()
    def finish_split(x_str):
        return (float(x_str[0].strip()), float(x_str[1].strip()))
    tuple_x_y = [ finish_split(x_y.split(","))  for x_y in  data.split(";")[1:-1]]
    tuple_x_y = [ txy for txy in tuple_x_y if txy[1] != 0]
    times = np.array([txy[0] for txy in tuple_x_y])
    counts = np.array([txy[1] for txy in tuple_x_y])
    popt, pcov = do_normal_regression(times, counts, np.sqrt(np.array(counts)))

    data = plt.subplot2grid((3,1), (0, 0), rowspan=2) 
    res = plt.subplot2grid((3,1), (2, 0), rowspan=1) 
    plot_with_residuum(times, None, counts, np.sqrt(counts), normal(times, *popt),
        "Coincidence " + path , "zeitlicher Abstand", "Ereignisse", data, res );
    plt.savefig("protocols/M21/Plots/Time/" + name + ".png")
    plt.clf()

    opts.append(popt)
    covs.append(pcov)
    chi_sq.append(np.sum((normal(times, *popt) - counts)**2 / np.sqrt(counts) )/(len(counts) - 3))

print("opts")
print(opts)
print("covs")
print(covs)
print("chi_sq")
print(chi_sq)

plt.legend()
plt.show()
