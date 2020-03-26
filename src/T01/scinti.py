
from src.common.analyse_peak import *

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
plt.plot(channels, NaICnt, label="NaI Counted All Events", alpha=0.4)
plt.plot(channels, RauschNaICnt, label="NaI Noise", alpha=0.4)
plt.plot(channels, NaICnt-RauschNaICnt, label="NaI Sample Events")
plt.axvspan(932, 1300, label="$\gamma 0.66 MeV$", color='yellow', alpha=0.3)
plt.axvspan(275, 680, label="$\\beta_-$ 0.59 MeV", color='chocolate', alpha=0.3)
plt.axvspan(4960, 5040, label="runaway value", color='grey', alpha=0.3)
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("NaI Scintillator")
plt.legend()
#plt.savefig("{}/SpektrenNaI.png".format(ppath))
plt.close('all')


plt.figure(figsize=(8,6), dpi=1200)
plt.plot(channels, PlasticCnt, label="Plastic Counted All Events", alpha=0.4)
plt.plot(channels, RauschPlasticCnt, label="Plastic Noise", alpha=0.4)
plt.plot(channels, PlasticCnt-RauschPlasticCnt, label="Plastic Sample Events")
plt.axvspan(700, 1400, label="$\gamma 0.66 MeV$", color='yellow', alpha=0.3)
plt.axvspan(265, 700, label="$\\beta_-$ 0.59 MeV", color='chocolate', alpha=0.3)
plt.axvspan(4960, 5040, label="runaway value", color='grey', alpha=0.3)
plt.grid(True)
plt.xlabel("Channel")
plt.ylabel("Events")
plt.title("Plastic Scintillator")
plt.legend()
#plt.savefig("{}/SpektrenPlastic.png".format(ppath))
plt.close('all')

print("Disacard High Values")
print("Fit gauss peak to peaks")
print("detected rate by proportion of peak hights")
print("light yield by proportion of peak mids")
print("Using of course the gamme peak")

#
#
# determine 
#
NaICnt =NaICnt[:2500] 
PlasticCnt =PlasticCnt[:2500] 
RauschNaICnt =RauschNaICnt[:2500] 
RauschPlasticCnt =RauschPlasticCnt[:2500] 
channels =channels[:2500] 

NaICnt = NaICnt - RauschNaICnt
PlasticCnt = PlasticCnt - RauschPlasticCnt

NaICntErr = np.sqrt(NaICnt + RauschNaICnt)
PlasticCntErr = np.sqrt(PlasticCnt + RauschPlasticCnt)

opt1, cov1, noneval = analyse_back_peak(channels, NaICnt, NaICntErr, 280, 1.4, file_name = "{}/PeakNaIBest.png".format(ppath),
        title="Peakcenter NaI", xlabel="Events", ylabel="Channel")
opt2, cov2, noneval = analyse_back_peak(channels, PlasticCnt, PlasticCntErr, 280, 1.4, file_name = "{}/PeakPlasticBest.png".format(ppath),
        title="Peakcenter Plastic", xlabel="Events", ylabel="Channel", lower = 700, upper=1400)


print("""Relative detection Rate, Platic / NaI \t: {:.3e} \pm {:.3e}
Relative light yield, Plastic / NaI \t: {:.3e} \pm {:.3e}
Devide by NaI to keep uncertainty smaller""".format(opt2[2]/opt1[2],
    np.sqrt(cov2[2][2]/opt1[2] ** 2 + opt2[2]**2/opt1[2]**4 * cov1[2][2]),
    opt2[0]/opt1[0],
    np.sqrt(cov2[0][0]/opt1[0] ** 2 + opt2[0]**2/opt1[0]**4 * cov1[0][0])))
