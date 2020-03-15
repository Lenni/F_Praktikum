
import os
import sys
sys.path.append(os.environ['PWD'])

from energy import *
from dcm import *
from weg_cal import *
from timediff import *

#
# Vergleiche time distance und längen kalib 
#
#


print("Vergleiche Positionen")
motor_pos = np.array([23871, 16274, 28661, 34139, 18000])
pos_td = np.array([37.35, 11.3])
pos_td_err = 1/np.sqrt(12) * 0.05
td_mittelwert.sort()
motor_pos.sort()
mitte = 0.5 * (pos_td[0] + pos_td[1])
mitte_err = 0 * np.sqrt(2) * pos_td_err

motor_pos_lin = weg_m * (motor_pos) - mitte + weg_c
motor_pos_lin_err = np.sqrt(np.sum(np.array([ err ** 2 for err in [motor_pos * weg_m_err, 
        weg_c_err * np.ones(len(motor_pos)), mitte_err] ])))

delta_l = -0.5 * 3*10**-2 * td_mittelwert
deltal_err =  0.5 * (3*10**-2 * td_error)* np.ones(len(motor_pos))

abw_mttw = motor_pos_lin - delta_l
sigma = abw_mttw / np.sqrt(deltal_err ** 2 + motor_pos_lin_err ** 2)

print("Motorpos\t DeltaMittelWertLin cm \tErr\t\tDeltaMittelWert cm \tErr\t\tAbw cm \t\tSigma")
for i in range(len(motor_pos)):
    print("{:08.2f}\t{:08.2f}\t\t{:08.2f}\t{:08.2f}\t\t{:08.2f}\t {:08.2f}\t {:08.2f}".format(
        motor_pos[i], motor_pos_lin[i], motor_pos_lin_err[i], delta_l[i], deltal_err[i],
        abw_mttw[i], sigma[i]))

plt.clf()
plt.plot(motor_pos, motor_pos_lin, label="lin-model")
plt.plot(motor_pos, delta_l, label="Coinzidenzen")
plt.legend()
plt.show()


print("Generelle Anmerkungen zur Fehler Rechnnung: Ereignisse haben den Fehler Wurzel N")
print("Energie und Zeitfehler: Bereich durch Wurzel 12")
print("Fehler auf Fitparameter durch Varianz von Chi-Quadrat\n")
print("Bei der Energiespektrumskorrektur: Gaußsche Fehlerfortpflanzung")
print("Fehlerfortpflanzung auf 'Streckungsfaktor' (1275-511)(gemessener Hochpeak - gemesser Tiefpeak) ")
