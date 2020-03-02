import re
import readline

from itertools import *

################# PRELUDE ##############

import sys
from sys import platform

# import libraries needed

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np


########################################

## load data
raw_spu_1_3 = open("data/M21/DCM/spu1_3.dcmTileCoords", "r")
raw_spu_1_6 = open("data/M21/DCM/spu1_6.dcmTileCoords", "r")
raw_spu_2_3 = open("data/M21/DCM/spu2_3.dcmTileCoords", "r")
raw_spu_2_6 = open("data/M21/DCM/spu2_6.dcmTileCoords", "r")

dcm_file_data = list()

any_list = list()
while True:
    try:
        match_obj = re.match(r'\s*([0-9]+)\s+([0-9]+)\s+([0-9]+)', raw_spu_1_3.readline())
        any_list.append((int(match_obj.group(1)) - 1, int(match_obj.group(2)), float(match_obj.group(3))))
    except:
        break
dcm_file_data.append(any_list)

while True:
    try:
        match_obj = re.match(r'\s*([0-9]+)\s+([0-9]+)\s+([0-9]+)', raw_spu_1_6.readline())
        any_list.append((int(match_obj.group(1)) - 1, int(match_obj.group(2)), float(match_obj.group(3))))
    except:
        break
dcm_file_data.append(any_list)

while True:
    try:
        match_obj = re.match(r'\s*([0-9]+)\s+([0-9]+)\s+([0-9]+)', raw_spu_2_3.readline())
        any_list.append((int(match_obj.group(1)) - 1, int(match_obj.group(2)), float(match_obj.group(3))))
    except:
        break
dcm_file_data.append(any_list)

while True:
    try:
        match_obj = re.match(r'\s*([0-9]+)\s+([0-9]+)\s+([0-9]+)', raw_spu_2_6.readline())
        any_list.append((int(match_obj.group(1)) - 1, int(match_obj.group(2)), float(match_obj.group(3))))
    except:
        break
dcm_file_data.append(any_list)

## put it into a nice form
dcm = list()
for i in range(4):
    x_list = list()
    for k, g in groupby(sorted(dcm_file_data[i], key = lambda x: x[0]), key = lambda x: x[0]):
        gl = list(g)
        gl.sort(key = lambda x: x[1])
        x_list.append(np.array([g[2] for g in gl]))
    dcm.append(np.array(x_list))


dark_color = (0.0, 0.0, 0.0)
light_color = (1.0, 1.0, 1.0)
i=1
for plot_data in dcm:
    mmin = min([min(p) for p in plot_data])
    mmax = max([max(p) for p in plot_data])

    def color_map(value):
        a = [float(light_color[i] - dark_color[i])/float(mmax - mmin) * float(value)
            + float(dark_color[i]) for i in range(3)]
        return (a[0], a[1], a[2])

    #turn plot data to rgb
    pplot = [[x for x in xs] for xs in plot_data]

    tplot = np.empty((len(pplot), len(pplot[0])))
    for l in range(len(pplot)):
        for j in range(len(pplot[l])):
                tplot[l, j] = pplot[l][j]

    pcm = plt.pcolor(tplot)
    #plt.colorbar(pcm)
    plt.title("DCM " + str(i))
    plt.savefig("test" + str(i) + ".png")
    i = i + 1
