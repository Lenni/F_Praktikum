
from src.common.analyse_peak import *
from src.common.plot_with_residuum import *
import matplotlib.pyplot as plt
import numpy as np

import os

plt.rc('text', usetex=True)

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

xs = [0.0]
ys = [opt1[2]]
y_err = [np.sqrt(cov1[2][2])]
for led_thickn in [1,2,4,6,8,10,12,14,16,18,20,40,52]:
    Cnt = (np.array(list(map(lambda x: float(x.strip()), open("{}/Abschwächung/{}mm.TKA".format(
        dpath, led_thickn)).read().split("\n")[2:-1])))[:2500] - RauschNaICnt)
    opt, cov, chi = analyse_back_peak(np.array(list(range(len(Cnt)))) + 1, Cnt-RauschNaICnt[:2500],
        np.sqrt(Cnt), 0, 1.4, lower=930, upper=1130)
    
    xs.append(0.1 * led_thickn)
    ys.append(opt[2])
    print(opt[2], cov[2][2])
    y_err.append(np.sqrt(cov[2][2]) if cov[2][2] != 0 else y_err[-1])
#
# Kalibration
#
xs = np.array(xs)
x_err = 0.01*np.ones(len(xs))
ys = np.array(ys)
y_err = np.array(y_err)

print(y_err)
density = 11.340
print("using lead density {} mg/cm^3".format(density))
 
def deine_mum(xs, ys, yerr, xerr, name, xlabel, beta0):
    exp = lambda x, mu, a: a*np.exp(-1.0 * x * mu) 

    linf = lambda x, mu, ln_a: ln_a - mu*x

    opt, cov, chi_sq = regression(linf, xs, np.log(ys), 1/ys * yerr, xErr=xerr)
    print("""{}
\mu:\t {} \pm {}
I_0:\t {} \pm {}
chi/ndf:\t {}""".format(name, opt[0], np.sqrt(cov[0][0]), opt[1], np.sqrt(cov[1][1]),  chi_sq))
    simple_figure(xs, xerr, np.log(ys), 1/ys * yerr, linf(xs, *opt), name, xlabel, "Counts",
    "{}/{}.png".format(ppath, name.replace(' ', '_')))

    print("chisq: {}\n\n".format(np.sum((np.log(ys)-linf(xs,*opt))**2/((1/ys * yerr) **2 + (opt[0] * xs *xerr) **2) / (len(xs) - 2))))

deine_mum(xs, ys, y_err, x_err, "attenuation coefficient unfiltered", "Distance /cm", [1.64, 610] )
deine_mum(density * xs, ys, y_err, x_err, "mass attenuation coefficient unfiltered", "Area mass density /$\\frac{mg}{cm^2}$", [1.64/density, 610] )

print("first value is runaway so redo without")

deine_mum(xs[1:-2], ys[1:-2], y_err[1:-2], x_err[1:-2], "attenuation coefficient", "Distance /cm", [1.64, 610] )
deine_mum(density * xs[1:-2], ys[1:-2], y_err[1:-2], density*x_err[1:-2], "mass attenuation coefficient", "Area mass density /$\\frac{mg}{cm^2}$", [1.64/density, 610] )

