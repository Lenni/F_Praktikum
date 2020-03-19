
import numpy as np
from scipy.optimize import curve_fit
from scipy import odr

def normal(x,my, sigma, a):
    return a * np.exp(-1.0 * (x-my)**2 / (2 * sigma ** 2))

def other_normal(B, x):
    return normal(x, *B)

def do_normal_regression_x(energy, counts, count_unc_stat):
    energy = np.array(energy)
    max_idx, max_val = max(enumerate(counts), key=lambda x: x[1])
    my = np.sum(counts * energy) / np.sum(counts)
#    deltas = [energy[i + 1] - energy[i] for i in range(len(energy) - 1)]
#    deltas.append(energy[-1] - energy[-2])
#    deltas = np.array(deltas)
    sigma = np.sqrt(np.sum((energy**2 * counts))/np.sum(counts) - my**2)
    popt, pcov = curve_fit(normal, energy, counts,
        p0=[my, sigma , 1.2 * max_val],
        sigma=np.array(np.array(count_unc_stat)/np.array(counts)), maxfev=10_000)
    return popt, pcov

def do_normal_regression(x, y, yErr, xErr=None, beta0=None):
    if beta0 is None:
        #popt, none = do_normal_regression_x(x, y, yErr)
        max_idx, max_val = max(enumerate(y), key=lambda x: x[1])
        my = np.sum(y * x) / np.sum(y)
        sigma = np.sqrt(np.sum((x**2 * y))/np.sum(y) - my**2)
        beta0 = [my, sigma, max_val]
    else:
        pass
    return regression(normal, x, y, yErr, xErr=xErr, beta0=beta0)


#def do_normal_regression(x, y, yErr, xErr=None):
#    from scipy import odr
#    model = odr.Model(other_normal)
#    data = odr.RealData(x, y, sx = xErr, sy=yErr)
#    popt, pcov = do_normal_regression_x(x, y, yErr)
#    modr = odr.ODR(data, model, beta0=popt)
#    output = modr.run()
#    return output.beta, output.cov_beta, output.res_var/(len(x) - 3)

def regression(model, x, y, yErr, xErr=None, beta0=None):
    if beta0 is None:
        beta0, none = curve_fit(model, x, y, sigma = yErr, maxfev = 100000)
    mod = odr.Model(lambda B, x: model(x, *B))
    data = odr.RealData(x,y, sx=xErr, sy = yErr)
    modr = odr.ODR(data, mod, beta0=beta0, maxit=1000)
    outp = modr.run()
    beta = outp.beta
    propagated_x_err = list()
    if xErr is not None:
        propagated_x_err = [ (model(x[i + 1], *beta) - model(x[i], *beta))/
        ((x[i+1] - x[i])*xErr[i]) for i in range(len(x) -1 )]
        propagated_x_err.append((model(x[-1], *beta) - model(x[-2], *beta))/(x[-1] - x[-2]) * xErr[-1])
    else:
        pass
    propagated_x_err = np.zeros(len(x))
    propagated_x_err = np.array(propagated_x_err)
    return beta, outp.cov_beta, np.sum((np.array(y) - model(np.array(x), *outp.beta))**2/((propagated_x_err ** 2 + yErr ** 2)*(len(x) - len(beta0))))

def propagate_error (model, beta ,x, xErr):
    propagated_x_err = [ (model(x[i + 1], *beta) - model(x[i], *beta))/
        ((x[i+1] - x[i])*xErr[i]) for i in range(len(x) -1 )]
    propagated_x_err.append((model(x[-1], *beta) - model(x[-2], *beta))/(x[-1] - x[-2]) * xErr[-1])
    return propagated_x_err
