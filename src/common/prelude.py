import sys
from sys import platform

# fuck you apple
if platform == "darwin":
    sys.path = sys.path.append("/usr/local/lib/python3.7/site-packages/")

# import libraries needed

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

