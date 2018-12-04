from fits_multimeter_errors import *


def test_initialization():
    global test
    test = dataset([1, 2, 3], [1, 1.6, 2], 'v', 'a')
    test.y_error_array = [0.1, 0.05, 0.2]
    
# alimentation capacities
C_arr_0 = 10**(-9) * np.array([98.2, 89.0])
C_scale_arr_0 = 10**(-7) * np.ones(2)

C_0 = multimeter_error_array(C_arr_0, C_scale_arr_0, 'm', 'c')

# 1: MISURA DELLA CURVA DI TRASFERIMENTO PER UN AMPLIFICATORE INVERTENTE 

R_arr_1 = np.array([5612.2, 32624, 46.79])
R_scale_arr_1 = np.array([10000, 100000, 1000])

R_1 = multimeter_error_array(R_arr_1, R_scale_arr_1, 'm', 'ohm', ignore_gain=True)
#contains R1, R2, R3 with uncertainties 

freq_1 = ufloat(1000, 0) # Hz

Vin_plus_1 = np.array([0.100, 0.292, .536, .780, 1.02, 1.26, 1.5, 1.76, 2, 2.48, 2.88])
Vout_minus_1 = np.array([0.592, 1.76, 3.20, 4.72, 6.08, 7.80, 9.4, 10.8, 12.2, 14.8, 15.2])
Vin_minus_1 = np.array([-0.096, -0.284, -.528, -.780, -1.02, -1.26, -1.5, -1.72, -1.96, -2.44, -2.88])
Vout_plus_1 = np.array([-0.568, -1.72, -3.16, -4.72, -6, -7.60, -9, -10.4, -11.8, -14, -14.2])

Vin_plus_vdiv_1 = np.array([0.05, 0.1, 0.2, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1])
Vout_plus_vdiv_1 = np.array([0.2, 1, 1, 2, 2, 5, 5, 5, 5, 5, 5])
Vin_minus_vdiv_1 = Vin_plus_vdiv_1 # the resolution is the same since it's the same scale
Vout_minus_vdiv_1 = Vout_plus_vdiv_1

Vout_minus_1 = np.flip(Vout_minus_1, axis = 0)
Vin_minus_1 = np.flip(Vin_minus_1, axis = 0)
Vin_minus_vdiv_1 = np.flip(Vin_minus_vdiv_1, axis = 0)
Vout_minus_vdiv_1 = np.flip(Vout_minus_vdiv_1, axis = 0)

Vin_1 = np.concatenate((Vin_minus_1, Vin_plus_1), axis=0)
Vout_1 = np.concatenate((Vout_minus_1, Vout_plus_1), axis=0)
Vin_vdiv_1 = np.concatenate((Vin_minus_vdiv_1, Vin_plus_vdiv_1), axis=0)
Vout_vdiv_1 = np.concatenate((Vout_minus_vdiv_1, Vout_plus_vdiv_1), axis=0)

transfer_plus_1 = dataset(Vin_plus_1, Vout_plus_1, 'v', 'v')
transfer_minus_1 = dataset(Vin_minus_1, Vout_minus_1, 'v', 'v')
transfer_1 = dataset(Vin_1, Vout_1, 'v', 'v')

transfer_plus_1.calculate_error(Vin_plus_vdiv_1, 'x', 'o')
transfer_plus_1.calculate_error(Vout_plus_vdiv_1, 'y', 'o')
transfer_minus_1.calculate_error(Vin_minus_vdiv_1, 'x', 'o')
transfer_minus_1.calculate_error(Vout_minus_vdiv_1, 'y', 'o')
transfer_1.calculate_error(Vin_vdiv_1, 'x', 'o')
transfer_1.calculate_error(Vout_vdiv_1, 'y', 'o')

transfer_plus_1.point_ignore = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
transfer_minus_1.point_ignore = np.flip(transfer_plus_1.point_ignore)
transfer_1.point_ignore = np.concatenate((transfer_minus_1.point_ignore,  transfer_plus_1.point_ignore), axis=0)

# 2: AMPLIFICATORE DELLE DIFFERENZE – AMPLIFICATORE NON INVERTENTE

R_arr_21 = np.array([5613.3, 32515, 46.64])
R_scale_arr_21 = np.array([10000, 100000, 1000])

R_21 = multimeter_error_array(R_arr_21, R_scale_arr_21, 'm', 'ohm', ignore_gain=True)
#contains R1, R2, R3 (b) 

freq_21 = ufloat(1000, 0)

#Non-invertent: 2.1a

Vin_arr_21 = np.array([.196, .984, 1.94])
Vin_scale_arr_21 = np.array([.05, .2, .5])
Vout_arr_21  = np.array([1.16, 5.8, 11.6])
Vout_scale_arr_21 = np.array([.2, 1, 2])

Vin_21 = multimeter_error_array(Vin_arr_21, Vin_scale_arr_21, 'o', 'v')
Vout_21 = multimeter_error_array(Vout_arr_21, Vout_scale_arr_21, 'o', 'v')

#Amp differences: 2.1b

Vin1_arr_21 = np.array([-.284, .292, .292, -.284])
Vin1_scale_arr_21 = 0.1 * np.ones(4)
Vin2_arr_21 = np.array([.488, .488, -.480, -.480])
Vin2_scale_arr_21 = 0.2 * np.ones(4)
Voutb_arr_21 = np.array([4.56, 1.2, -4.4, -1.12]) 
Voutb_scale_arr_21 = 2 * np.ones(4)

Vin1_21 = multimeter_error_array(Vin1_arr_21, Vin1_scale_arr_21, 'o', 'v')
Vin2_21 = multimeter_error_array(Vin2_arr_21, Vin2_scale_arr_21, 'o', 'v')
Voutb_21 = multimeter_error_array(Voutb_arr_21, Voutb_scale_arr_21, 'o', 'v')

#Amp sums invertent: 2.2

Rf_22 = ufloat_single_value(5621.6, 100000, 'm', 'ohm')
#contains Rf
#also, use R1 from 1 and R1b from 21

Vin1_arr_22 = np.array([-.284, .292, .292, -.284])
Vin1_scale_arr_22 = 0.1 * np.ones(4)
Vin2_arr_22 = np.array([.488, .488, -.480, -.480])
Vin2_scale_arr_22 = 0.2 * np.ones(4)
Vout1_arr_22 = np.array([-.180, -.760, .200, .780]) 
Vout1_scale_arr_22 = 0.5 * np.ones(4)

Vin1_22 = multimeter_error_array(Vin1_arr_22, Vin1_scale_arr_22, 'o', 'v')
Vin2_22 = multimeter_error_array(Vin2_arr_22, Vin2_scale_arr_22, 'o', 'v')
Vout1_22 = multimeter_error_array(Vout1_arr_22, Vout1_scale_arr_22, 'o', 'v')

#Integrator for impulses: 2.3

C_arr_23 = 10**(-12) * np.array([345, 648, 22]) 
C_scale_arr_23 = 10**(-12) * np.array([1000, 1000, 1000])

C_23 = multimeter_error_array(C_arr_23, C_scale_arr_23, 'm', 'c', ignore_gain=True)
#Contains C1, Cf, C_fondo

for i in range(2):
    C_23[i] = C_23[i] - C_23[2]
    
freq_23 = ufloat(50, 0)

Rf_23 = ufloat_single_value(10.580 * 10**(6), 10**8, 'm', 'ohm')

Vin_23 = np.array([.300, .504, .800, 1, 1.3, 1.8, 2.28, 3])
Vout_23 = np.array([.472, .800, 1.44, 1.78, 2.36, 3.2, 4.16, 5.36])
Vin_vdiv_23 = np.array([.1, .2, .5, .5, .5, 1, 1, 1])
Vout_vdiv_23 = np.array([.2, .5, .5, .5, 1, 1, 2, 2])

transfer_23 = dataset(Vin_23, Vout_23, 'v', 'v')
transfer_23.calculate_error(Vin_vdiv_23, 'x', 'o')
transfer_23.calculate_error(Vout_vdiv_23, 'y', 'o')

# RADDRIZZATORE DI PRECISIONE CON OPERAZIONALI: 3


R_arr_3 = np.array([32659, 32510, 32670, 32540])
R_scale_arr_3 = 10**5 * np.ones(4)

R_3 = multimeter_error_array(R_arr_3, R_scale_arr_3, 'm', 'ohm')
#R1: a, b, c, d

Vin_arr_3 = np.array([10.4, 5.2, -5.2])
Vin_scale_arr_3 = np.array([2, 2, 2])

Vin_3 = multimeter_error_array(Vin_arr_3, Vin_scale_arr_3, 'o', 'v')
#Contains Vinpp, Vin max, Vin min

Vout_arr_3 = np.array([5.12, 5.12, -5.04, 0.08, -5.6, 0.56])
#Vout(Vin_max), Vout(vin_min), V2(Vin_max), V2(Vin_min)
#Vo'(Vin_max), Vo'(Vin_min)
Vout_scale_arr_3 = 2 * np.ones(6)

Vout_3 = multimeter_error_array(Vout_arr_3, Vout_scale_arr_3, 'o', 'v')

