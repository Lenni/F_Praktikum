
import os
from src.common.fitting import *
from src.common.plot_with_residuum import *

print("Kapazitäten")
print("Schmeiße hälfte der Daten Weg, weil der Fit sonst nicht klappt")
print("Kaputte Residuen graphen wegen verstecken kapazitäten")
print("Fitte summe aus vielen Kondesator funktionen an, wenn die Amplitude nicht mehr kleiner wird, ist der Fit maximal angepasst")
print("Der dominante Effekt ist dann der mit größten Amplitude, also unsere Kondensatorfunktion")
def take_pairs(array):
    idx = 0
    while idx + 1 < len(array):
        yield (array[idx], array[idx + 1])
        idx = idx + 2

charge_file = open("data/LAB/Capacitor/cap_charge.txt")
discharge_file = open("data/LAB/Capacitor/cap_discharge.txt")

if not os.path.exists("protocols/LAB/Plots/Capacitor"):
    os.makedirs("protocols/LAB/Plots/Capacitor")

def do_eval(dataFile, name, epsilon, func):
    data= list(map(lambda row: list(map(lambda f: float(f.strip()), row.split("\t")[0:-2])),
        dataFile.read().split("\n")))
    last_idx = int(len(data[0]) *0.66)
    voltages = np.array(data[0][0:last_idx])
    times = np.array(data[1][0:last_idx])
    voltage_err = 10**-9 *np.ones(len(voltages))
    mutable_voltages = np.copy(voltages)
    parameter_sets = list()
    ampl = 0.0
    function = lambda x, *args: sum(map(lambda p: func(times, *p), take_pairs(args)))
    while True:
        opt, cov, chi_sq = regression(func, times, mutable_voltages, voltage_err, bounds=(0.0, 10.0), beta0=[10, 0.1])
        mutable_voltages = mutable_voltages - func(times, *opt)
        parameter_sets.extend(opt)
        print(opt[1])
        if np.abs(opt[1]) < epsilon:
            break
    voltage_err = epsilon*np.ones(len(times))
    function = lambda x, *args: sum(map(lambda p: func(times, *p), take_pairs(args)))
    opt, cov, chi_sq = regression(function, times, voltages, voltage_err, beta0 = np.array(parameter_sets))
    i = 0
    while 2 * (i) + 1< len(opt):
        print("Parameterset {}".format(i))
        print("tau: {} \pm {}".format(opt[0 + 2*i], np.sqrt(cov[0+2*i][0+2*i])))
        print("a  : {} \pm {}".format(opt[1 + 2*i], np.sqrt(cov[1+2*i][1+2*i])))
        print()
        i = i +1
    print("chi: {}".format(chi_sq))
    simple_figure(times, None, voltages, voltage_err, function(times, *opt), name,
        "Zeit /s", "Kondensatorspannung /V", "protocols/LAB/Plots/Capacitor/Capacitor{}.png".format(name))
    print("\n\n\n")
do_eval(discharge_file, "Entladung",0.0001,lambda x, tau, a: a * np.exp(-1.0 * x /tau))
    # take_pairs(locals().values()) a*np.exp(-1.0 * x /tau) + a2*np.exp(-1.0 * x /tau2) + a3*np.exp(-1.0 * x /tau3) + a4*np.exp(-1.0 * x /tau4) + a5*np.exp(-1.0 * x /tau5))
do_eval(charge_file, "Aufladung", 0.0001, lambda x, tau, a: a * (1-np.exp(-1.0* x /tau)))
