import matplotlib.pyplot as plt
import numpy as np

import os

dpath = "data/T01/Experiment 2"
ppath = "protocols/T01/Plots/Scinti"
if not os.path.exists(ppath):
    os.makedirs(ppath)

#
# Erstelle Rohdaten Plot
#
#

NaICnt = np.array(list(map(lambda x: float(x.strip()), open("{}/Probe/NaI.TKA".format(
    dpath)).read().split("\n")[2:-1])))
PlasticCnt = np.array(list(map(lambda x: float(x.strip()), open("{}/Probe/Plastik.TKA".format(
    dpath)).read().split("\n")[2:-1])))
RauschNaICnt = np.array(list(map(lambda x: float(x.strip()), open("{}/Rausch/NaI.TKA".format(
    dpath)).read().split("\n")[2:-1])))
RauschPlasticCnt = np.array(list(map(lambda x: float(x.strip()), open("{}/Rausch/Plastik.TKA".format(
    dpath)).read().split("\n")[2:-1])))
channels = np.array(list(range(len(RauschNaICnt))))

plt.figure(figsize=(8,6), dpi=1200)
plt.plot(channels, NaICnt, label="NaI Counted All Events")
plt.plot(channels, RauschNaICnt, label="NaI Noise")
plt.plot(channels, NaICnt-RauschNaICnt, label="NaI Sample Events")
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("Scintilator")
plt.legend()
plt.savefig("{}/Spektren.png".format(ppath))



plt.figure(figsize=(8,6), dpi=1200)
#plt.plot(channels, PlasticCnt, label="Plastic Counted All Events")
#plt.plot(channels, RauschPlasticCnt, label="Plastic Noise")
#plt.plot(channels, NaICnt-RauschNaICnt, label="Plastic Sample Events")
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("Scintilator")
plt.legend()
plt.savefig("{}/Spektren.png".format(ppath))
