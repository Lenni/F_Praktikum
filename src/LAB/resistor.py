

import numpy as np
import matplotlib.pyplot as plt

from src.common.fitting import *
from src.common.plot_with_residuum import *

import csv
import os

voltage_err_stat = 5*10**-8
voltage_err_sys = 0.00003

print("Widerstände")

print("statistischer Fehler ist der Achsenabschnitt einer linearen Funktion mx + c")
print("Widerstand ist Steigung in mx")

if not os.path.exists("protocols/LAB/Plots/Widerstände"):
    os.makedirs("protocols/LAB/Plots/Widerstände")

def lin_func(x, m, c):
    return m * x + c
def prop_func(x, m):
    return m * x

mess_r = [1000, 470, 4700]
test_r = [99.3, 46.9, 220.4]
test_r_err = [0.1 for i in range(3)]

base_path = "data/LAB/Resistor/resistance_{}.txt"

pretty_output = "Widerstandkennngröße {}\n" + "sys. Fehler\t: {:.3e}\n"+"Widerstand\t: {:.3e} \pm {:.3e} \pm {:.3e}\n"  +"chi_sq\t: {:.3e}\n" + "Abweichung\t: {}\n"
for mr, tr, tr_unc in zip(mess_r, test_r, test_r_err):
    data = csv.reader(open(base_path.format(mr), "r"), delimiter='\t')
    test_r_voltage = list()
    mess_r_voltage = list()
    for row in data:
        test_r_voltage.append(float(row[0]))
        mess_r_voltage.append(float(row[2]))
    test_r_voltage = np.array(test_r_voltage)
    mess_r_voltage = np.array(mess_r_voltage) * 10
    current = mess_r_voltage / tr * 1000
    current_stat_err = np.sqrt((voltage_err_stat/tr)**2)*np.ones(len(test_r_voltage))
    voltage_stat_err = 2*10**-8 * np.ones(len(test_r_voltage))
    current_sys_err = ((mess_r_voltage /tr**2 * tr_unc) **2)*np.ones(len(test_r_voltage))

    opt, cov, chi_sq = regression(lin_func, current, test_r_voltage, voltage_err_stat * np.ones(len(test_r_voltage)),current_stat_err)
    #
    # bestimme  den statistischen Fehler als Streung ums model, gewichtet mit den rel. Stromfehlern
    #
    print("lege den statistischen Spannungsfehler auf {:.3e} fest".format(voltage_err_stat))

    opt, cov, chi_sq = regression(lin_func, current, test_r_voltage, voltage_stat_err,current_stat_err)
    cmax, noneval, noneval = regression(lin_func, current + current_sys_err, test_r_voltage + opt[1], voltage_stat_err, current_stat_err)
    cmin, noneval, noneval = regression(lin_func, current - current_sys_err, test_r_voltage - opt[1], voltage_stat_err, current_stat_err)
    sys_err = np.min(cmax[0] - cmin[0])/2

    simple_figure(current, current_stat_err, test_r_voltage, voltage_stat_err,
        lin_func(current, *opt), "{} $\Omega$ Widerstand".format(mr),
        "Stromstärke mA", "Spannung am Wiederstand / V", "protocols/LAB/Plots/Widerstände/Widerstand{}.png".format(mr))

    print(pretty_output.format(mr, opt[1], 1000 * opt[0], 1000*np.sqrt(cov[0][0]),  1000*sys_err, chi_sq,
        (1000*opt[0] -  mr) /np.sqrt(1000**2*cov[0][0] + (1000*sys_err)**2)))
