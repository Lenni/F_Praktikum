
import numpy as np
from scipy.optimize import curve_fit

def normal(x,my, sigma, a):
    return a * np.exp(-1.0 * (x-my)**2 / (2 * sigma ** 2))


def do_normal_regression(energy, counts, count_unc_stat):
    energy = np.array(energy)
    max_idx, max_val = max(enumerate(counts), key=lambda x: x[1])
    p = (energy[max_idx]-energy)**2
    sigma = np.sum((p * counts)) / np.sqrt(np.sum(counts**2))
    print(energy[max_idx])
    print(sigma)
    print(max_val)
    popt, pcov = curve_fit(normal, energy, counts,
        p0=[energy[max_idx], sigma ,max_val],
        sigma=np.array(np.array(count_unc_stat)/np.array(counts)))
    return popt, pcov
