
def plot_with_residuum(x, x_err, y, y_err, mod, name, x_label, y_label, ax_plot, ax_res ):
    ax_plot.errorbar(x, y, xerr=x_err, yerr=y_err, color="r", linewidth = 0)
    ax_plot.plot(x, mod);
    ax_plot.xlabel(x_label)
    ax_plot.ylabel(y_label)
    ax_plot.name(name)

    y_prop_err = [ (mod[i + 1] - mod[i])/(x[i+1]-x[i]) * xerr[i] for i in range(len(x_err) - 1) ]
    y_prop_err.append((mod[-1] - mod[-2])/(x[-1] - x[-2]) * xerr[-1]
    y_prop_err = np.sqrt(np.array(y_prop_err)**2 + y_err**2)
    ex_res.errorbar(x, y-mod, yerr=y_prop_err, color="r", linnewidth = 0)
    ax_res.plot(x, np.zeros(len(x)))
