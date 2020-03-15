
# encoding: utf-8

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

from src.common.fitting import *
from itertools import *

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
    if  x_err is not None:
        y_prop_err = [ (mod[i + 1] - mod[i])/(x[i+1]-x[i]) * x_err[i] for i in range(len(x_err) - 1) ]
        y_prop_err.append((mod[-1] - mod[-2])/(x[-1] - x[-2]) * x_err[-1])
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
    counts_stat_err = np.sqrt(np.sqrt(counts) ** 2 +
        (time_rausch_err / time_hier * m_rausch_cnt) **2 +
        (time_rausch / time_hier**2 * m_rausch_cnt * time_hier_err) ** 2 +
        (time_hier / time_rausch * np.sqrt(m_rausch_cnt))**2 )
    return n_counts, counts_stat_err, time_rausch/time_hier * m_rausch_cnt

def normal(x,my, sigma, a):
    return a * np.exp(-1.0 * (x-my)**2 / (2 * sigma ** 2))

def determineLineraty(energy, counts, count_unc_stat ,decr, tupl = None):
    print(decr)
    low = 0
    high = len(energy) - 1
    if tuple is None:
        while True:
            plt.figure(figsize=(3,3), dpi=300)
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
            plt.close('all')
    else:
        low = tupl[0]
        high = tupl[1]
    plt.clf()
    plt.close('all')
    #
    # guessing params
    #
    max_idx, max_val = max(enumerate(counts[low::high]), key=lambda x: x[1])
    plt.figure(figsize=(6,8), dpi=1200)
    data = plt.subplot2grid((3,1), (0,0), rowspan=2)
    res = plt.subplot2grid((3,1), (2,0), rowspan=1)
    popt, pcov, chi_sq = do_normal_regression(energy[low:high], counts[low:high], count_unc_stat[low:high],
        xErr=(energy[1]-energy[0])/np.sqrt(12) * np.ones(len(energy[low:high])))
        #sigma=np.array(count_unc_stat[low:high]/np.array(counts[low:high])))
    plot_with_residuum(energy[low:high], (energy[1]-energy[0])/np.sqrt(12) * np.ones(len(energy[low:high])),
        counts[low:high], count_unc_stat[low:high], normal(energy[low:high], *popt),
        decr + " unkorrigiertes Spektrum", "Energy kEV","Ereignisse", data, res )
    plt.savefig("protocols/M21/Plots/EnergyUnkorrigiert" + decr + ".png")
    plt.clf()
    plt.close('all')
    return popt, pcov, low, high, chi_sq

def do_regression(energy, energy_unc, counts, count_unc_stat,low, high, beta0=None):
#    max_idx, max_val = max(enumerate(counts[low::high]), key=lambda x: x[1])
#    popt, pcov = curve_fit(normal, energy[low:high], counts[low:high],
#        p0=[energy[low + max_idx], 10.0,max_val],
#        sigma=np.array(count_unc_stat[low:high]/np.array(counts[low:high])))
#    return popt, pcov
    return do_normal_regression(energy[low:high], counts[low:high], count_unc_stat[low:high],
           xErr= energy_unc[low:high], beta0=beta0)

(energy, counts) = read_hist("data/M21/Energy/singles.log")
nCounts, counts_stat_err, hier_rausch = calc_err_and_red_noice(counts)

a=2
print("X Fehler werden bei der Energie korrektur ignoriert")
tup5=determineLineraty(energy,counts,counts_stat_err,"511 Peak", (164, len(energy)-501))
tup12 = determineLineraty(energy, counts, counts_stat_err, "1255 Peak",(495,len(energy)-120))
correction_factor = 511.0/tup5[0][0]
corrected_energy = correction_factor * energy
energy_errors_sys = energy * (511)/(tup5[0][0])**2 * (np.diag(tup5[1])[0])
energy_error_stat = (corrected_energy[1] - corrected_energy[0])/np.sqrt(12) * np.ones(len(corrected_energy))


plt.figure(figsize=(8, 9), dpi=1200)
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

#
# 2nd guess over standard derivation
#
#
opt5, cov5, chiSq5 = do_regression(corrected_energy, energy_error_stat, nCounts, counts_stat_err, tup5[2], tup5[3])
plot_with_residuum(corrected_energy[tup5[2]:tup5[3]], energy_error_stat[tup5[2]:tup5[3]],
        nCounts[tup5[2]:tup5[3]], counts_stat_err[tup5[2]:tup5[3]],
        normal(corrected_energy[tup5[2]:tup5[3]], *opt5), "511 kEV Peak",
        "Energie kEV", "gezählte Ereignisse", ax_511_peak, ax_511_res)
plt.tight_layout()
cov5=np.diag(cov5)

opt12, cov12, chiSq12 = do_regression(corrected_energy, energy_error_stat, nCounts, counts_stat_err, tup12[2], tup12[3])
plot_with_residuum(corrected_energy[tup12[2]:tup12[3]], energy_error_stat[tup12[2]:tup12[3]],
        nCounts[tup12[2]:tup12[3]], counts_stat_err[tup12[2]:tup12[3]],
        normal(corrected_energy[tup12[2]:tup12[3]], *opt12), "1275 kEV Peak",
        "Energie kEV", "gezählte Ereignisse", ax_1275_peak, ax_1275_res)
plt.tight_layout()
cov12=np.diag(cov12)


fit_info_form_str= "Fitparameter \t\t{}\n" + "Mittelwert\t\t:{:9.4e} \pm {:9.4e} keV\n" + "Standardabbweichung\t:{:9.4e} \pm {:9.4e} keV^2\n" + "Peakhöhe\t\t:{:9.4e} \pm {:9.4e} \n" + "\chi^2\t\t\t:{:9.4e}"

print(fit_info_form_str.format("Korrekturpeak 511", tup5[0][0], tup5[1][0][0],
    tup5[0][1], tup5[1][1][1], tup5[0][2], tup5[1][2][2], tup5[-1] ))
print(fit_info_form_str.format("Korrekturpeak 1275", tup12[0][0], tup12[1][0][0],
    tup12[0][1], tup12[1][1][1], tup12[0][2], tup12[1][2][2], tup12[-1] ))
print(fit_info_form_str.format("Peak 511", opt5[0], cov5[0],
    opt5[1], cov5[1], opt5[2], opt5[2], chiSq5 ))
print(fit_info_form_str.format("Peak 1275", opt12[0], cov12[0],
    opt12[1], cov12[1], opt12[2], opt12[2], chiSq12 ))

plt.savefig("protocols/M21/Plots/energy_resultion.png")
plt.clf()
plt.close('all')
