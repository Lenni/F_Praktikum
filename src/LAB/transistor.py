# coding=utf-8
import csv
import os

ppath = "protocols/LAB/Plots/Transistor"

if not os.path.exists(ppath):
    os.makedirs(ppath) 

import numpy as np
import matplotlib.pyplot as plt

from src.common.fitting import *
from src.common.plot_with_residuum import *

rb = 350
rc = 4.7

ib = list()
ic = list()
ube = list()
for row in csv.reader(open("data/LAB/Tansistor/transistor_current.txt"), delimiter="\t"):
    ube.append(float(row[0].strip()))
    ib.append(float(row[2].strip())/rb)
    ic.append(float(row[1].strip())/rc)
ube = np.array(ube)
ib = np.array(ib)
ic = np.array(ic)

plt.figure(figsize=(8,6), dpi=1200)
plt.plot(ic, ib)
plt.xlabel("Basisstom /mA")
plt.ylabel("Collectorstrom /mA")
plt.grid(True)
plt.title("Stomsteuerkennline $I_C  = f(I_B)$")
plt.tight_layout()
plt.savefig(ppath + "/Stomsteuerkennline.png")
plt.clf()

linf = lambda x, m ,c: m * x + c
opt, cov, chi = regression(linf, ic, ib, 10**-12 /np.sqrt(3) / rb * np.ones(len(ic)), xErr = 10**-12 / np.sqrt(3) / rc * np.ones(len(ib)))
print(opt, np.sqrt(cov), chi)
simple_figure(ic,10**-12/np.sqrt(3) / rb*np.ones(len(ic)),ib,10**-12/np.sqrt(3)/rc*np.ones(len(ic)),linf(ic, *opt),"Gleichstromverstärkungsfaktor","Basisstrom mA","Kollektorstrom mA",ppath+"/gsvf.png")

ib = list()
ic = list()
ube = list()
for row in csv.reader(open("data/LAB/Tansistor/transistor_ein.txt"), delimiter="\t"):
    ube.append(float(row[0].strip()))
    ib.append(float(row[1].strip())/rb)
    ic.append(float(row[2].strip())/rc)
ube = np.array(ube)
ib = np.array(ib)
ic = np.array(ic)
plt.figure(figsize=(8,6), dpi=1200)
plt.plot(ube, ic)
plt.xlabel("Basisemitterspannnug /V")
plt.ylabel("Kollektorstrom /mA")
plt.grid(True)
plt.title("Eingangskennline $I_C  = f(U_{BE})$")
plt.tight_layout()
plt.savefig(ppath + "/Einganskennline.png")
plt.clf()


plt.figure(figsize=(8,6), dpi=1200)
for (i, I) in zip(range(3), [1, 5, 10] ):
    ib = list()
    ic = list()
    ube = list()
    for row in csv.reader(open("data/LAB/Tansistor/transistor_out{}.txt".format(i+1)), delimiter="\t"):
        ube.append(float(row[0].strip()))
        ib.append(float(row[1].strip())/rb)
        ic.append(float(row[2].strip())/rc)
    ube = np.array(ube)
    ib = np.array(ib)
    ic = np.array(ic)
    plt.plot(ube, ic, label="Basisstrom: {}  mA".format(I))
    plt.xlabel("Kollektoremitterspannnug /V")
    plt.ylabel("Kollektorstrom /mA")
    plt.grid(True)
    plt.title("Ausgangskennlinie $I_C  = f(U_{BE})$")
    plt.tight_layout()
plt.legend()
plt.savefig(ppath + "/Ausgangskennlinen.png")
