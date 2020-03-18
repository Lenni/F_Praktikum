

from src.common.fitting import *
from src.common.plot_with_residuum import *

import numpy as np
import matplotlib.pyplot as plt

print_and_do = lambda f, *args: (lambda printnone, fs, *argss: f(*args))(print(args), f, *args)

data_file = open("data/M21/coincidences.log")
data = list(filter( lambda x: x[1] != 0,
        map( lambda x: (np.sum(np.array([360.0, 60.0, 1.0]) * np.array(x[0:3])), x[-1]),
            map(lambda x: list(map(lambda idx: float(x[idx].strip()), [0,1,2,-1])),
                map( lambda x: x.split(":"),
                    data_file.read().split("\n")[5:-1]
                )
            )
        )
    ))

x_data = np.array([x[0] for x in data])
y_data = np.array([y[1] for y in data])

y_err = np.sqrt(y_data)
x_err = (x_data[1] - x_data[0])/np.sqrt(12) * np.ones(len(x_data))

def linf(x, m, c):
    return m * x + c


opt, cov, chi_sq = regression(linf, x_data, y_data, y_err, xErr=x_err)
simple_figure(x_data, x_err, y_data, y_err, linf(x_data, *opt), "Sensititibität", "Zeit / s", "Ereignisse", "protocols/M21/Plots/sensitivity.png")

print()
print()
print("Sensitivitätsauswertung")
print("m: {:.3e} \pm {:.3e}".format(opt[0], np.sqrt(cov[0][0])))
print("c: {:.3e} \pm {:.3e}".format(opt[1], np.sqrt(cov[1][1])))
print("chi_sq: {}".format(chi_sq))
