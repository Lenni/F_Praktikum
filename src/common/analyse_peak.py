
from src.common.fitting import *

import matplotlib.pyplot as plt

def analyse_back_peak(xs, ys, yerr, threshold, hys, xerr=None, file_name = None,
        title=None, xlabel = None, ylabel=None, upper=None, lower=None):
    #
    # find peak
    #
    if upper is None and lower is None:
        upper = len(xs) - 1
        while ys[upper] < hys * threshold:
            upper = upper - 1
        lower = upper
        while ys[lower] > threshold:
            lower = lower - 1
    opt, cov, chi_sq = do_normal_regression(xs[lower:upper], ys[lower:upper],
        yerr[lower:upper], xErr=xerr[lower:upper] if xerr is not None else None)
    if file_name is not None:
        plot_peak_res(xs, ys, yerr, xerr, lower, upper, file_name, title, xlabel, ylabel, opt, cov, chi_sq)
    return (opt,cov, chi_sq)

def plot_peak_res(x, y, y_err, x_err, lower, upper, filename, name, x_label, y_label, opt, cov, chi_sq):
    mod = opt[2] * np.exp(-1.0 * (x[lower:upper] - opt[0])**2/(2*opt[1]**2))

    print("""Gaußfit {}
mu     : {:.3e} \pm {:3e}
sigma  : {:.3e} \pm {:.3e} 
hight: : {:.3e} \pm {:.3e}
chi_sq : {:.3e} \n
""".format(name, opt[0], np.sqrt(cov[0][0]), opt[1], np.sqrt(cov[1][1]), opt[2],
        np.sqrt(cov[2][2]), chi_sq))

    plt.clf()
    plt.close('all')
    plt.figure(figsize=(8,6), dpi=1200)
    ax_plot = plt.subplot2grid((3,1), (0,0), rowspan=2)
    ax_res = plt.subplot2grid((3,1), (2,0), rowspan=1)

    ax_plot.errorbar(x, y, xerr=x_err, yerr=y_err, color="r", linewidth = 0,
        markersize=0, marker=",", elinewidth=1)
    ax_plot.plot(x[lower:upper], mod);

    ax_plot.axvspan(x[lower], x[upper], label="selected data", alpha=0.2)

    y_prop_err = np.zeros(len(y_err[lower:upper]))
    if  x_err is not None:
        y_prop_err = [ (mod[i + 1] - mod[i])/(x[i+1]-x[i]) * x_err[lower + i] for i in range(len(mod) - 1) ]
        y_prop_err.append((mod[-1] - mod[-2])/(x[upper] - x[upper -1]) * x_err[upper])
    y_prop_err = np.sqrt(np.array(y_prop_err)**2 + y_err[lower:upper]**2)

    ax_res.errorbar(x[lower:upper], y[lower:upper]-mod, yerr=y_prop_err, color="r", linewidth = 0,
        markersize=0, marker=",", elinewidth=1, capsize=2)
    ax_res.plot(x[lower:upper], np.zeros(len(x[lower:upper])))
    ax_res.set_xlabel("Channels")
    ax_plot.set_ylabel("Events")
    ax_res.set_ylabel("Diviation")
    ax_plot.set_title(name)
    ax_res.grid(True)
    ax_plot.grid(True)

    plt.savefig(filename)
    plt.clf()
