#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:44:20 2019

@author: jacopo
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib 
matplotlib.rcParams['lines.linewidth'] = 1
matplotlib.rcParams["errorbar.capsize"] = 3

# Choose the "true" parameters.
m_true = -0.9594
b_true = 4.294
f_true = 0.534

# Generate some synthetic data from the model.
N = 50
x = np.sort(10*np.random.rand(N))
yerr = 0.1+0.5*np.random.rand(N)
y = m_true*x+b_true
y += np.abs(f_true*y) * np.random.randn(N)
y += yerr * np.random.randn(N)

y_true = m_true*x + b_true

"""
plt.errorbar(x, y, yerr=yerr, fmt='.', capthick=0.5)
plt.plot(x, y_true, linewidth=2)
plt.xlabel('x')
plt.ylabel('y')
"""