
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

def plot_with_residuum(x, x_err, y, y_err, mod, name, x_label, y_label, ax_plot, ax_res ):
    ax_plot.errorbar(x, y, xerr=x_err, yerr=y_err, color="r", linewidth = 0,
        markersize=1, marker=",", elinewidth=1, capsize=2)
    ax_plot.plot(x, mod);

    y_prop_err = np.zeros(len(y_err))
    if  x_err is not None:
        y_prop_err = [ (mod[i + 1] - mod[i])/(x[i+1]-x[i]) * x_err[i] for i in range(len(x_err) - 1) ]
        y_prop_err.append((mod[-1] - mod[-2])/(x[-1] - x[-2]) * x_err[-1])
    y_prop_err = np.sqrt(np.array(y_prop_err)**2 + y_err**2)
    ax_res.errorbar(x, y-mod, yerr=y_prop_err, color="r", linewidth = 0,
        markersize=1, marker=",", elinewidth=1, capsize=2)
    ax_res.plot(x, np.zeros(len(x)))
    ax_res.set_xlabel(x_label)
    ax_plot.set_ylabel(y_label)
    ax_res.set_ylabel("Abweichung")
    ax_plot.set_title(name)
    ax_res.grid(True)
    ax_plot.grid(True)

def simple_figure(x, x_err, y, y_err, mod, name, x_label, y_label, filename):
    plt.clf()
    plt.figure(figsize=(8,6), dpi=1200)
    ax_plot = plt.subplot2grid((3,1), (0,0), rowspan=2)
    ax_res = plt.subplot2grid((3,1), (2,0), rowspan=1)
    plot_with_residuum(x, x_err, y, y_err, mod, name, x_label, y_label, ax_plot, ax_res)
    plt.savefig(filename)
    plt.clf()
