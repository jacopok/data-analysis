#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 22:18:14 2018

@author: jacopo
"""

from fits_multimeter_errors import *
from opamp_load_data import *

# 1: MISURA DELLA CURVA DI TRASFERIMENTO PER UN AMPLIFICATORE INVERTENTE 

m_theory_1 = - R_1[1] / R_1[0]

print('1: valore teorico di coefficiente angolare')
print(m_theory_1)

print('1: valore sperimentale del coefficiente angolare')
params_1, error_params_1 = transfer_1.fit()
m_experiment_1 = ufloat(params_1[0], error_params_1[0])
q_experiment_1 = ufloat(params_1[1], error_params_1[1])
print(m_experiment_1)

print('1: valore sperimentale dell intercetta')
print(q_experiment_1)

print('1: valori di m per i dati + e -')


print('\n(')
# 2: AMPLIFICATORE DELLE DIFFERENZE – AMPLIFICATORE NON INVERTENTE

#Non-invertent: 2.1a

A_21 = Vout_21 / Vin_21

A_teor_21 = (1 + R_1[1] / R_1[0])/(1 + R_21[0]/R_21[1]) * np.ones(len(A_21))

compatibility_21a = uarray_compatibility(A_21, A_teor_21)

print('2.1a: valore teorico delle amplificazioni')
print(A_teor_21)

print('2.1a: valore sperimentale delle amplificazioni')
print(A_21)

print('2.1a: compatibilità')
print(compatibility_21a)

print('\n')
#Amp differences: 2.1b

Vout_teor_21 = (1 + R_1[1] / R_1[0])/(1 + R_21[0]/R_21[1]) * Vin2_21 - (R_1[1]/R_1[0]) * Vin1_21

compatibility_21b = uarray_compatibility(Vout_teor_21, Voutb_21)

print('2.1b: valori di V1')
print(Vin1_21)

print('2.1b: valori di V2')
print(Vin2_21)


print('2.1b: valore teorico dei Vout')
print(Vout_teor_21)

print('2.1b: valore sperimentale dei Vout')
print(Voutb_21)

print('2.1b: compatibilità')
print(compatibility_21b)

print('\n')

#Amp sums invertent: 2.2

Vout_teor_22 = - ((Rf_22 / R_1[0]) * Vin1_22 + (Rf_22 / R_21[0]) * Vin2_22)
compatibility_22 = uarray_compatibility(Vout_teor_22, Vout1_22)

print('2.2: valori di V1')
print(Vin1_22)

print('2.2: valori di V2')
print(Vin2_22)

print('2.2: valore teorico dei Vout')
print(Vout_teor_22)

print('2.2: valore sperimentale dei Vout')
print(Vout1_22)

print('2.1b: compatibilità')
print(compatibility_22)

print('\n')
#Integrator for impulses: 2.3

m_theory_23 = C_23[1] / C_23[0]

params_23, errorparams_23 = transfer_23.fit()
m_experiment_23 = ufloat(params_23[0], errorparams_23[0])
compatibility_23 = ufloat_compatibility(m_theory_23, m_experiment_23)

print('2.3: valore teorico coefficiente angolare')
print(m_theory_23)

print('2.3: valore sperimentale coefficiente angolare')
print(m_experiment_23)

print('2.3: compatibilità')
print(compatibility_23)

# RADDRIZZATORE DI PRECISIONE CON OPERAZIONALI: 3

R2_23 = 1 / (1/R_1[1] +1/R_21[1])
