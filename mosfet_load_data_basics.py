from fits_multimeter_errors import *


# RESISTENZE

R_arr = [680, 9.850, 389.3, 3.23, 783, 6.65]
R_scale_arr = [6000, 60, 600, 6, 6000, 60]

R_arr = 1000 * np.array(R_arr)
R_scale_arr = 1000 * np.array(R_scale_arr)

# NOMI: 
# protezione = 0
# d (drain) = 1
# 1 = 2
# S = 3
# 2 = 4 (la vogliamo da: )
# d nuova = 5

R = multimeter_error_array(R_arr, R_scale_arr, 'a', 'ohm')

# CAPACITÀ

C_arr = [114*10**(-12), 114*10**(-12), 161*10**(-9), 146*10**(-9), 90.2*10**(-6)]
C_scale_arr = [10**(-9), 10**(-9), 10**(-6), 10**(-6), 10**(-4)]

# NOMI: 
# Cp1 (protezione) = 0
# Cp2 (protezione) = 1
# C1 (attaccata al gate) = 2
# C2 (attaccata al drain) = 3
# C3 (attaccata al source: bypass) = 4

C = multimeter_error_array(C_arr, C_scale_arr, 'm', 'c')

# 
