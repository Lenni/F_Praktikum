################# PRELUDE ##############

import sys
from sys import platform

# import libraries needed

import csv
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, Normalize
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


########################################

## load data

filenames = ["data/M21/DCM/spu1_3.dcmTileCoords", "data/M21/DCM/spu1_6.dcmTileCoords", "data/M21/DCM/spu2_3.dcmTileCoords", "data/M21/DCM/spu2_6.dcmTileCoords"]

plot = False

## put it into a nice form
dcm = list()

for name in filenames:
    x_list = np.empty(shape=(400, 512))
    with open(name) as file:
        reader = csv.reader(file, delimiter=" ", skipinitialspace=True)
        for row in reader:
            x = int(int(row[0]) / 2)
            y = int(row[1])
            x_list[x, y] = float(row[2])
    dcm.append(np.array(x_list))

text = [(1, 1), (1, 2), (2, 1), (2, 2)]
i = 0

count_rates = np.empty((1))

for plot_data in dcm:

    if(plot):
        pcm1 = plt.imshow(plot_data)
        plt.colorbar(pcm1, label=r"Count Rate in $\frac{1}{s}$")
        plt.title(r"DCM SPU " + str(text[i][0]) + ", Sensor " + str(text[i][1]) + " (Linear skaliert)")
        plt.savefig("DCM_SPU" + str(text[i][0]) + "_Sensor" + str(text[i][1]) + "_lin.eps", bbox_inches = "tight")
        plt.close()

        pcm2 = plt.imshow(np.nan_to_num(np.log(plot_data + 0.000001), nan=0.00001))
        plt.colorbar(pcm2, label=r"Count Rate in $\ln(x)$")
        plt.title(r"DCM SPU " + str(text[i][0]) + ", Sensor " + str(text[i][1]) + " Logarithmisch skaliert")
        plt.savefig("DCM_SPU" + str(text[i][0]) + "_Sensor" + str(text[i][1]) + "_log.eps", bbox_inches = "tight")
        plt.close()

    count_rates = np.append(count_rates, plot_data.flatten())

    i = i+1

count_rates = count_rates[count_rates != -1]

sorted_count_rates = np.sort(count_rates)

sum = np.zeros(len(sorted_count_rates))
marker = 0

for i in range(2, len(sorted_count_rates)):

    cut_array = sorted_count_rates[0:-i]
    sum[i-2] = np.sum(cut_array)

    if(marker == 0 and sum[i-2] < 0.5 * sum[0]):
        marker = i


fig = plt.figure(figsize=(16,9))
plt.plot(sum, marker =".", linewidth = 0)
plt.axvline(marker, color = "r", label=r"15$\%$ der Anfangsrate x = {}".format(marker))
plt.xlabel(r"Anzahl Abgeschalteter SPADs", fontsize = 16)
plt.ylabel(r"Dark Count Rate in $\frac{1}{s}$", fontsize = 16)
plt.legend(fontsize = 16)

plt.savefig("DCR_vs_N.png", bbox_inches="tight")
