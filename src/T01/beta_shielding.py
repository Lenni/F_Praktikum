
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

print(cnt)
print(dens)

def deine_mum(xs, ys, xerr, yerr, name):
    exp = lambda x, mu, a: a*np.exp(x * mu)#  + a2 * np.exp(mu2 * x)

    linf = lambda x, mu, ln_a: ln_a - mu*x
#opt[2], np.sqrt(cov[2][2]), opt[3], np.sqrt(cov[3][3]), 
    opt, cov, chi_sq = regression(exp, xs, ys, yerr, xErr=xerr, beta0 = [-0.001535,610])#, 10**-10, 1])
    print("""{}
\mu : {} \pm {}
a   : {} \pm {}
\mu2:  \pm 
a   :  \pm 
chi/ndf:\t {}""".format(name, opt[0], np.sqrt(cov[0][0]), opt[1], np.sqrt(cov[1][1]), chi_sq))
    simple_figure(xs, xerr, ys, yerr, exp(xs, *opt), name, "xlabel", "Counts",
    "{}/{}.png".format(ppath, name))

#    print("chisq: {}\n\n".format(np.sum(((ys-exp(xs,*opt))**2/((yerr) **2+(lambda x, mu, a, mu2, a2: a*mu*np.exp(x * mu)  + a2 * mu2 + np.exp(mu2 * x))(xs,*opt)**2) / (len(xs) - 2)))))

deine_mum(thickness, cnt - rausch_cnt, 0.01 * np.ones(len(thickness)), np.sqrt(cnt + rausch_cnt), "attenuation coefficient unf" )
deine_mum(dens, cnt - rausch_cnt, 0.01 * np.ones(len(dens)), np.sqrt(cnt + rausch_cnt), "mass attenuation coefficient unf" )

deine_mum(thickness[:-3], (cnt - rausch_cnt)[:-3],0.01 * np.ones(len(thickness[:-3])), np.sqrt(cnt + rausch_cnt)[:-3], "attenuation coefficient" )
deine_mum(dens[:-3], (cnt - rausch_cnt)[:-3], 0.01 * np.ones(len(thickness[:-3])), np.sqrt(cnt + rausch_cnt)[:-3], "mass attenuation coefficient" )
