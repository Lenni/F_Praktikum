
import numpy as np
import matplotlib.pyplot as plt

def read_hist(filen):
    all_str = open(filen, "r").read()
    str_split = all_str.split(";")[1:-1]
    str_double_split = [[int(a.strip()) for a in s.split(",")] for s in str_split]
    return (np.array([s[0] for s in str_double_split]),
            np.array([s[1] for s in str_double_split]))

(srausch_en, srausch_cnt) = read_hist("data/M21/Noise_Singles.log")
(crausch_en, crausch_cnt) = read_hist("data/M21/Noise_Coincidence.log")

plt.figure(figsize=(6,8), dpi=1200)
plt.plot(crausch_en, crausch_cnt, label="Coincidences")
plt.plot(srausch_en, srausch_cnt, label="Singles")
plt.legend()
plt.title("Rauschmessung")
plt.xlabel("Energien /keV")
plt.ylabel("Ereignisse")
plt.grid(True)
plt.savefig("protocols/M21/Plots/rausch.png")
