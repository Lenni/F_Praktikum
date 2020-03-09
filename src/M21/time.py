
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

TDS_Names = ["data/M21/Time/" + s for s in ["TDS_1.log", "TDS_2.log", "TDS_3.log",
    "TDS_4.log", "TDS_Cal.log"]]

for path in TDS_Names:
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
    plt.show()
    plt.clf()
plt.legend()
plt.show()
