
# encoding: utf-8

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


#
# from src.common.plot_with_residuum import *
#
#
#
#
#

def plot_with_residuum(x, x_err, y, y_err, mod, name, x_label, y_label, ax_plot, ax_res ):
    ax_plot.errorbar(x, y, xerr=x_err, yerr=y_err, color="r", linewidth = 0,
        markersize=2, marker=".", elinewidth=1)
    ax_plot.plot(x, mod);

    y_prop_err = np.zeros(len(y_err))
    if  x_err != None:
        y_prop_err = [ (mod[i + 1] - mod[i])/(x[i+1]-x[i]) * xerr[i] for i in range(len(x_err) - 1) ]
        y_prop_err.append((mod[-1] - mod[-2])/(x[-1] - x[-2]) * xerr[-1])
    y_prop_err = np.sqrt(np.array(y_prop_err)**2 + y_err**2)
    ax_res.errorbar(x, y-mod, yerr=y_prop_err, color="r", linewidth = 0,
        markersize=2, marker=".", elinewidth=1, capsize=2)
    ax_res.plot(x, np.zeros(len(x)))
    ax_res.set_xlabel(x_label)
    ax_plot.set_ylabel(y_label)
    ax_res.set_ylabel("Abweichung")
    ax_plot.set_title(name)
    ax_res.grid(True)
    ax_plot.grid(True)


#
# INPUT PARAMTERS
#
#
#
cnt_rate = 29.188
cnt_rate_err = 0.252

def read_hist(filen):
    all_str = open(filen, "r").read()
    str_split = all_str.split(";")[1:-1]
    str_double_split = [[int(a.strip()) for a in s.split(",")] for s in str_split]
    return (np.array([s[0] for s in str_double_split]),
            np.array([s[1] for s in str_double_split]))

(rausch_en, rausch_cnt) = read_hist("data/M21/Noise_Singles.log")
def calc_err_and_red_noice(counts):
    # Rauschen abziehen
    m_rausch_cnt = rausch_cnt[:len(counts)]
    rausch_counts = np.sum(rausch_cnt)
    hier_counts = np.sum(counts)
    time_rausch =  rausch_counts / cnt_rate
    time_hier = hier_counts / cnt_rate
    time_rausch_err = np.sqrt((np.sqrt(rausch_counts)/cnt_rate)**2 +
        (rausch_counts/cnt_rate**2 * cnt_rate_err) ** 2)
    time_hier_err = np.sqrt((np.sqrt(hier_counts)/cnt_rate)**2 +
        (hier_counts/cnt_rate**2 * cnt_rate_err) ** 2)

    n_counts = counts - time_rausch / time_hier * m_rausch_cnt
    ##
    ## FALSCH
    ##
    counts_stat_err = np.sqrt(np.sqrt(counts) ** 2 +
        (time_hier_err / time_rausch * m_rausch_cnt) **2 +
        (time_hier / time_rausch**2 * m_rausch_cnt * time_rausch_err) ** 2 +
        (time_hier / time_rausch * np.sqrt(m_rausch_cnt)))
    return n_counts, counts_stat_err, time_rausch/time_hier * m_rausch_cnt

def normal(x,my, sigma, a):
    return a * np.exp(-1.0 * (x-my)**2 / (2 * sigma ** 2))

def determineLineraty(energy, counts, count_unc_stat ,decr):
    print(decr)
    low = 0
    high = len(energy) - 1
    while True:
        plt.plot(energy, counts)
        plt.axvline(energy[low])
        plt.axvline(energy[high])
        plt.show()
        inp = input()
        if inp[0] == "l":
            if inp[1] == "+":
                low = low + int(inp[2:])
            if inp[1] == "-":
                low = low - int(inp[2:])
        elif inp[0] == "h":
            if inp[1] == "+":
                high = high + int(inp[2:])
            if inp[1] == "-":
                high = high - int(inp[2:])
        else:
            break
        plt.clf()
        plt.close('all')
    plt.scatter(energy[low:high], counts[low:high])
    print("fitting")
    #
    # guessing params
    #
    max_idx, max_val = max(enumerate(counts[low::high]), key=lambda x: x[1])
    popt, pcov = curve_fit(normal, energy[low:high], counts[low:high],
        p0=[energy[low + max_idx], 10.0,max_val],
        sigma=np.array(count_unc_stat[low:high]/np.array(counts[low:high])))
    print(popt)
    plt.plot(energy, normal(np.array(energy), *popt))
    plt.show()

    print(decr)
    print("Median:  " + str(popt[0] )+ "\t" + str(np.sqrt(np.diag(pcov)[0])))
    print("Uncert:  " + str(popt[1] )+ "\t" + str(np.sqrt(np.diag(pcov)[1])))
    print("Hight :  " + str(popt[2] )+ "\t" + str(np.sqrt(np.diag(pcov)[2])))

    return popt, pcov, low, high

def do_regression(energy, counts, count_unc_stat,low, high):
    max_idx, max_val = max(enumerate(counts[low::high]), key=lambda x: x[1])
    popt, pcov = curve_fit(normal, energy[low:high], counts[low:high],
        p0=[energy[low + max_idx], 10.0,max_val],
        sigma=np.array(count_unc_stat[low:high]/np.array(counts[low:high])))
    return popt, pcov

(energy, counts) = read_hist("data/M21/Energy/singles.log")
nCounts, counts_stat_err, hier_rausch = calc_err_and_red_noice(counts)

a=2
tup5=determineLineraty(energy,counts,counts_stat_err,"511 Peak")
tup12 = determineLineraty(energy, counts, counts_stat_err, "1255 Peak")
corrected_energy = (1275 - 511)/(tup12[0][0] - tup5[0][0]) * energy
energy_errors_sys = energy * (1275-511)/(tup12[0][0] - tup5[0][0])**2 * (np.diag(tup5[1])[0]
    + np.diag(tup12[1])[0])


#(ax1, ax2) = (plt.subplot(221), plt.subplot(222))
#plot_with_residuum(energy[low:high], None, nCounts[low:high], counts_stat_err[low:high],
#    normal(energy[low:high], *tup5[0]), "test", "test x", "test y", ax1, ax2)
#plt.show()

plt.figure(figsize=(8, 9))
# get subplots
shape = (7, 2)
ax_spectrum = plt.subplot2grid(shape, (0,0), colspan=2, rowspan=4)
ax_511_peak = plt.subplot2grid(shape, (4,0), colspan=1, rowspan=2)
ax_1275_peak = plt.subplot2grid(shape, (4,1), colspan=1, rowspan=2)
ax_511_res = plt.subplot2grid(shape, (6,0), colspan=1, rowspan=1)
ax_1275_res = plt.subplot2grid(shape, (6,1), colspan=1, rowspan=1)

print("Kein Energie fehler angezeigt, da diese systematisch sind")
all_plot = ax_spectrum.errorbar(corrected_energy, counts, yerr=np.sqrt(counts),
        elinewidth=2, linewidth=0, marker=".")
all_plot.set_label("gesamte Ereignisse")
rausch_plot = ax_spectrum.errorbar(corrected_energy, hier_rausch, yerr=np.sqrt(hier_rausch),
        elinewidth=2, linewidth=0, marker=".")
rausch_plot.set_label("auf Zeit normiertes Rauschen")
data_plot = ax_spectrum.errorbar(corrected_energy, nCounts, yerr=np.sqrt(counts_stat_err),
        elinewidth=2, linewidth=0, marker=".")

data_plot.set_label("Na-22 Ereignisse")
low_sel = ax_spectrum.axvspan(corrected_energy[tup5[2]], corrected_energy[tup5[3]], alpha=0.2)
low_sel.set_label("511 kEV Peak")
high_sel = ax_spectrum.axvspan(corrected_energy[tup12[2]], corrected_energy[tup12[3]],
        alpha=0.2, color ="r")
high_sel.set_label("1275 kEV Peak")
ax_spectrum.set_xlabel("Energie kEV")
ax_spectrum.set_ylabel("Ereignisse")
ax_spectrum.set_title("Energiespektrum")
ax_spectrum.legend()
ax_spectrum.grid(True)

opt5, cov5 = do_regression(corrected_energy, nCounts, counts_stat_err, tup5[2], tup5[3])
plot_with_residuum(corrected_energy[tup5[2]:tup5[3]], None,
        nCounts[tup5[2]:tup5[3]], counts_stat_err[tup5[2]:tup5[3]],
        normal(corrected_energy[tup5[2]:tup5[3]], *opt5), "511 kEV Peak",
        "Energie kEV", "gezählte Ereignisse", ax_511_peak, ax_511_res)


opt12, cov12 = do_regression(corrected_energy, nCounts, counts_stat_err, tup12[2], tup12[3])
plot_with_residuum(corrected_energy[tup12[2]:tup12[3]], None,
        nCounts[tup12[2]:tup12[3]], counts_stat_err[tup12[2]:tup12[3]],
        normal(corrected_energy[tup12[2]:tup12[3]], *opt12), "1275 kEV Peak",
        "Energie kEV", "gezählte Ereignisse", ax_1275_peak, ax_1275_res)
plt.tight_layout()

print("511 kEV plot parameter")
print(opt5)
print(np.diag(cov5))
chiSq5 = np.sum(((nCounts[tup5[2]:tup5[3]] - normal(corrected_energy[tup5[2]:tup5[3]], *opt5)) ** 2 /
        counts_stat_err[tup5[2]:tup5[3]]**2))/(tup5[3] - tup5[2] - 3)
print(chiSq5)
print("\n\n")

print("1275 kEV plot parameter")
print(opt12)
print(np.diag(cov12))
chiSq12 = np.sum(((nCounts[tup12[2]:tup12[3]] - normal(corrected_energy[tup12[2]:tup12[3]], *opt12)) ** 2 /
        counts_stat_err[tup12[2]:tup12[3]]**2))/(tup12[3] - tup12[2] - 3)
print(chiSq12)
print("\n\n")

plt.savefig("data/M21/energy_resultion.eps")
plt.clf()
