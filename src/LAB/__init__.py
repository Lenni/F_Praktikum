#
#
# import imports
#
#

import sys
import os

sys.path.append(os.environ['PWD'])

if not os.path.exists("protocols/LAB/Plots"):
    os.makedirs("protocols/LAB/Plots")

#
# global constants
#
#
print("Statistischer Fehler auf Spannungsmessung: letze Stelle durch Wurzel 12")
print("Systematischer Fehler auf Spannungsmessungs: Offset * Bereich (10 V)")
