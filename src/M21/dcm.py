################# PRELUDE ##############

import sys
from sys import platform

# import libraries needed

import csv
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, Normalize
import numpy as np

########################################

## load data

filenames = ["data/M21/DCM/spu1_3.dcmTileCoords", "data/M21/DCM/spu1_6.dcmTileCoords", "data/M21/DCM/spu2_3.dcmTileCoords", "data/M21/DCM/spu2_6.dcmTileCoords"]

## put it into a nice form
dcm = list()

for name in filenames:
    x_list = np.empty(shape=(400, 512))
    with open(name) as file:
        reader = csv.reader(file, delimiter=" ", skipinitialspace=True)
        for row in reader:
            print(row)
            x = int(int(row[0]) / 2)
            y = int(row[1])
            x_list[x, y] = float(row[2])
    dcm.append(np.array(x_list))

i = 1
for plot_data in dcm:
    pcm1 = plt.imshow(plot_data)
    plt.colorbar(pcm1)
    plt.title("DCM " + str(i) + "Linear skaliert")
    plt.savefig("test" + str(i) + "_lin.eps")
    plt.close()

    pcm2 = plt.imshow(np.nan_to_num(np.log(plot_data + 0.000001), nan=0.00001))
    plt.colorbar(pcm2)
    plt.title("DCM " + str(i) + "Logarithmisch skaliert")
    plt.savefig("test" + str(i) + "_log.eps")
    plt.close()

    i = i + 1