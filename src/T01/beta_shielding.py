
from src.common.fitting import * 
from src.common.plot_with_residuum import *

import matplotlib.pyplot as plt

import csv
import os

ppath = "protocols/T01/Plots/Beta"
if not os.path.exists(ppath):
    os.makedirs(ppath)

rausch_cnt = None
cnt = list()
thickness = list()
dens = list()
for row in csv.DictReader(open("data/T01/betaShielding.csv")):
    if row["Plaettchen"] != "0":
        cnt.append(sum([float(stri.strip()) for stri in [row["1Cnt"], row["2Cnt"], row["3Cnt"]]]))
        dens.append(float(row["density"].strip()))
        thickness.append(float(row["thickness"].strip()))
    else:
        rausch_cnt = sum([float(stri.strip()) for stri in [row["1Cnt"], row["2Cnt"], row["3Cnt"]]])

cnt = np.array(cnt)
thickness = np.array(thickness)
dens = np.array(dens)

def deine_mum(xs, ys, yerr, name):
    exp = lambda x, mu, a, mu2, a2: a*np.exp(-1.0 * x * mu) + a2*np.exp(-1.0 * mu2 * x)

    opt, cov, chi_sq = regression(exp, xs, ys, yerr)
    print("""{}
\mu:\t {} \pm {}
a:\t {} \pm {}
\mu2:\t {} \pm {}
a2:\t {} \pm {}
chi/ndf:\t {} \n\n\n""".format(name, opt[0], np.sqrt(cov[0][0]), opt[1], np.sqrt(cov[1][1]),
        opt[2], np.sqrt(cov[2][2]), opt[3], np.sqrt(cov[3][3]), chi_sq))
    simple_figure(xs, None, ys, yerr, exp(xs, *opt), name, "Distance /cm", "Counts",
    "{}/{}.png".format(ppath, name))

deine_mum(thickness, cnt - rausch_cnt, np.sqrt(cnt + rausch_cnt), "attenuation coefficient unf" )
deine_mum(dens, cnt - rausch_cnt, np.sqrt(cnt + rausch_cnt), "mass attenuation coefficient unf" )

deine_mum(thickness[:-3], (cnt - rausch_cnt)[:-3], np.sqrt(cnt + rausch_cnt)[:-3], "attenuation coefficient" )
deine_mum(dens[:-3], (cnt - rausch_cnt)[:-3], np.sqrt(cnt + rausch_cnt)[:-3], "mass attenuation coefficient" )
