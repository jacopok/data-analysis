# -*- coding: utf-8 -*-
import numpy as np
import scipy
from scipy import optimize
import matplotlib.pyplot as plt


#Initialization of data arrays
#microamps
current_array = [1, 10.03, 100.12, 1004.4, 10004, 100320]
#millivolts
voltage_array = [528.2, 595.9, 659, 720, 782, 838]

current_errors_array = [0.15 + 0.0001 * current_array[0],
                        0.15 + 0.0001 * current_array[1],
                        0.15 + 0.0001 * current_array[2],
                        0.8 + 0.0008 * current_array[3],
                        8 + 0.0008 * current_array[4],
                        8 + 0.0008 * current_array[5]]

#Make sure the data is of the correct type
current_array = np.array(current_array, dtype=np.float64)
voltage_array = np.array(voltage_array, dtype=np.float64)
current_errors_array = np.array(current_errors_array, dtype=np.float64)

#milli amps
current_zener_array = [-40.048, -60.021]
#volts
voltage_zener_array = [-5.215, -5.292]
#milli amps
error_current_zener_array = [0.008 + 0.0008 * current_zener_array[0],
                             0.008 + 0.0008 * current_zener_array[1]]

max_voltage = np.max(voltage_array)
min_voltage = np.min(voltage_array)
N = 1000
voltage_step = (max_voltage - min_voltage) / N
granular_voltage = np.arange(min_voltage, max_voltage, voltage_step)

max_voltage_zener = np.max(voltage_zener_array)
min_voltage_zener = np.min(voltage_zener_array)
voltage_step_zener = (max_voltage_zener - min_voltage_zener) / N
granular_voltage_zener = np.arange(min_voltage_zener, max_voltage_zener, voltage_step_zener)



def current_theory(voltage, a, b):
    """
    Theoretical model: I = I_S (exp(V / (n*V_T)) -1), where
    I_S is some base current, n is the ideality factor (from 1 to 2 usually),
    V_T is the characteristic curren of the diode.
    We ignore the -1 and calculate I = a exp(b*V), so:
        I_S = a
        1/(n *V_T) = b
    """
    current = a * (np.exp(b * voltage) )
    return(current)
    
def current_zener_theory(voltage, a, b):
    current = a + b * voltage
    return(current)
    
    
#Optimization of the theoretical function
#Gives the parameter values and their variance
popt, pcov = scipy.optimize.curve_fit(current_theory, voltage_array, current_array,
                                      sigma=current_errors_array, absolute_sigma=True,
                                      p0=[10**(-9), 10**(-2)])
a = popt[0]
b = popt[1]
error_a = pcov[0, 0]
error_b = pcov[1, 1]

popt_zener, pcov_zener = scipy.optimize.curve_fit(current_zener_theory, voltage_zener_array, current_zener_array, sigma=current_zener_errors_array, absolute_sigma=True)
a_z = popt_zener[0]
b_z = popt_zener[1]
error_a_z = pcov_zener[0, 0]
error_b_z = pcov_zener[1, 1]

#Logarithmic plot of current vs voltage
plt.semilogy(voltage_array, current_array, 'ro', label="Raw data")
plt.semilogy(granular_voltage, current_theory(granular_voltage, *popt), 'g--')
plt.xlabel("voltage [mV]")
plt.ylabel("(logarithmic) current [microA]")
plt.show()

#Regular plot of current vs voltage
plt.plot(voltage_array, current_array, 'ro', label="Raw data")
plt.plot(granular_voltage, current_theory(granular_voltage, *popt), 'g--')
plt.xlabel("voltage [mV]")
plt.ylabel("current [microA]")
plt.show()

#Regular plot of Zener current vs voltage
plt.plot(voltage_zener_array, current_zener_array, 'ro', label="Raw data")
plt.plot(granular_voltage_zener, current_zener_theory(granular_voltage_zener, *popt_zener), 'g--')
plt.xlabel("voltage [V]")
plt.ylabel("current [mA]")
plt.show()

r_z = 1/b_z # in kilo ohms
v_z = - a_z / b_z # in volts