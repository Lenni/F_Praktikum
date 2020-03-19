
import os
from src.common.fitting import *
from src.common.plot_with_residuum import *

print("Kapazitäten")
print("Schmeiße hälfte der Daten Weg, weil der Fit sonst nicht klappt")
print("Kaputte Residuen graphen wegen verstecken kapazitäten")
print("Fitte summe aus kondensator funktionen an, um Systematiken zu eliminieren")
print("Die Systematiken gelten als ausgeglichen, wenn 2 taus derGroßenordnung 0.29 auftreten")
print("0.29 ist das erwartete tau")
print("der Systematische Fehler kann mich am Arsch lecken")
print("der statistische Fehler wird aus der Streuung um das Modell bestimmt")

def take_pairs(array):
    idx = 0
    while idx + 1 < len(array):
        yield (array[idx], array[idx + 1])
        idx = idx + 2

charge_file = open("data/LAB/Capacitor/cap_charge.txt")
discharge_file = open("data/LAB/Capacitor/cap_discharge.txt")

if not os.path.exists("protocols/LAB/Plots/Capacitor"):
    os.makedirs("protocols/LAB/Plots/Capacitor")

def do_eval(dataFile, name, start_at ,many, func):
    data= list(map(lambda row: list(map(lambda f: float(f.strip()), row.split("\t")[0:-2])),
        dataFile.read().split("\n")))
    last_idx = int(len(data[0]) *0.66)
    voltages = np.array(data[0][0:last_idx])
    times = np.array(data[1][0:last_idx])
    voltage_err = 0.00025 *np.ones(len(voltages))
    mutable_voltages = np.copy(voltages)
    function = lambda x, *args: sum(map(lambda p: func(x, *p), take_pairs(args)))
    opt, cov, chi_sq = regression(function, times, voltages, voltage_err, beta0=[0.3, 10.0])
    parameter_sets = list(opt)
    for i in range(many-1):
        opt, cov, chi_sq = regression(function, times, voltages, voltage_err, beta0=parameter_sets)
        mutable_voltages = voltages - function(times, *opt)
        opt_new, n, m = regression(func, times, mutable_voltages, voltage_err, beta0=[0.3, 10.0])
        print(opt_new[0])
        parameter_sets.extend(opt)

    opt, cov, chi_sq = regression(function, times, voltages, voltage_err, beta0 = np.array(parameter_sets))

    #
    # Fehler neu intepretiren und daten filtern
    #
    vol_err = np.sum(np.abs(function(times, *opt) - voltages))/len(times)
    filtered = list(filter(lambda x: np.abs(function(x[0], *opt) - x[1]) < 50000 * vol_err and x[0] >= start_at, zip(times, voltages, voltage_err)))
    times = np.array([f[0] for f in filtered])
    voltages = np.array([f[1] for f in filtered])
    voltage_err =np.array([f[2] for f in filtered])
# np.sum(np.abs(function(times, *opt) - voltages))/np.sqrt(12)/len(times)
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
do_eval(discharge_file, "Entladung",1.5, 2,lambda x, tau, a: a * np.exp(-1.0 * x /tau))
    # take_pairs(locals().values()) a*np.exp(-1.0 * x /tau) + a2*np.exp(-1.0 * x /tau2) + a3*np.exp(-1.0 * x /tau3) + a4*np.exp(-1.0 * x /tau4) + a5*np.exp(-1.0 * x /tau5))
do_eval(charge_file, "Aufladung", 1.7 , 2, lambda x, tau, a: a * (1-np.exp(-1.0* x /tau)))

print("nun werde ich noch einen Plot erstellen, der zeigt, wie kaputt die Daten sind")
print("im Residuengraph werden die weiteren Kapazitäten sichtbar")
do_eval(discharge_file, "Systematiken", 0.0, 5, lambda x, tau, a: a*np.exp(-1.0 * x /tau))
