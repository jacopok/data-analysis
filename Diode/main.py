# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import scipy
from scipy import optimize
import matplotlib.pyplot as plt


#Initialization of data arrays
current_array = [1, 10, 100, 1000, 10**4, 10**5, 10**6]
voltage_array = [1, 2, 3, 4, 5, 6, 7]
current_errors_array = np.ones(len(voltage_array))

max_voltage = np.max(voltage_array)
min_voltage = np.min(voltage_array)
N = 1000
voltage_step = (max_voltage - min_voltage) / N
granular_voltage = np.arange(min_voltage, max_voltage, voltage_step)

#Make sure the data is of the correct type
current_array = np.array(current_array, dtype=float)
voltage_array = np.array(voltage_array, dtype=float)

def current_theory(voltage, a, b):
    """
    Theoretical model: I = I_S (exp(V / (n*V_T)) -1), where
    I_S is some base current, n is the ideality factor (from 1 to 2 usually),
    V_T is the characteristic curren of the diode.
    We ignore the -1 and calculate I = a exp(b*V), so:
        I_S = a
        1/(n *V_T) = b
    """
    current = a * np.exp(b * voltage)
    return(current)
    
popt, pcov = scipy.optimize.curve_fit(current_theory, voltage_array, current_array, sigma=current_errors_array)
a = popt[0]
b = popt[1]
error_a = pcov[0, 0]
error_b = pcov[1, 1]

#Logarithmic plot of current vs voltage
plt.semilogy(voltage_array, current_array, 'ro', label="Raw data")
plt.semilogy(granular_voltage, current_theory(granular_voltage, *popt), 'g--')
plt.xlabel("voltage")
plt.ylabel("(logarithmic) current")
plt.show()

#Regular plot of current vs voltage
plt.plot(voltage_array, current_array, 'ro', label="Raw data")
plt.plot(granular_voltage, current_theory(granular_voltage, *popt), 'g--')
plt.xlabel("voltage")
plt.ylabel("current")
plt.show()