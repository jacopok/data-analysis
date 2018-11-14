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

m_theory_1 = - R_1[1] / R_1[0]

freq_1 = ufloat(1000, 0) # Hz

Vin_plus_1 = np.array([0.100, 0.292, .536, .780, 1.02, 1.26, 1.5, 1.76, 2, 2.48, 2.88])
Vout_plus_1 = np.array([0.592, 1.76, 3.20, 4.72, 6.08, 7.80, 9.4, 10.8, 12.2, 14.8, 15.2])
Vin_minus_1 = np.array([-0.096, -0.284, -.528, -.780, -1.02, -1.26, -1.5, -1.72, -1.96, -2.44, -2.88])
Vout_minus_1 = np.array([-0.568, -1.72, -3.16, -4.72, -6, -7.60, -9, -10.4, -11.8, -14, -14.2])

Vin_plus_vdiv_1 = np.array([0.05, 0.1, 0.2, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1])
Vout_plus_vdiv_1 = np.array([0.2, 1, 1, 2, 2, 5, 5, 5, 5, 5, 5])
Vin_minus_vdiv_1 = Vin_plus_vdiv_1 # the resolution is the same since it's the same scale
Vout_minus_vdiv_1 = Vout_plus_vdiv_1

transfer_plus_1 = dataset(Vin_plus_1, Vout_plus_1, 'v', 'v')
transfer_minus_1 = dataset(Vin_minus_1, Vout_minus_1, 'v', 'v')

transfer_plus_1.calculate_error(Vin_plus_vdiv_1, 'x', 'o')
transfer_plus_1.calculate_error(Vout_plus_vdiv_1, 'y', 'o')
transfer_minus_1.calculate_error(Vin_minus_vdiv_1, 'x', 'o')
transfer_minus_1.calculate_error(Vout_minus_vdiv_1, 'y', 'o')


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

A_21 = Vout_21 / Vin_21

A_teor_21 = R_1[1]/R_1[0] * np.ones(len(A_21))

compatibility_21a = uarray_compatibility(A_21, A_teor_21)

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

Vout_teor_21 = R_1[1] / R_1[0] * (Vin2_21 - Vin1_21)

compatibility_21b = uarray_compatibility(Vout_teor_21, Voutb_21)

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

Vout_teor_22 = - (Vin1_22 + Vin2_22)
compatibility_22 = uarray_compatibility(Vout_teor_22, Vout1_22)

#Integrator for impulses: 2.3

C_arr_23 = 10**(-12) * np.array([340, 646]) 
C_scale_arr_23 = 10**(-12) * np.array([1000, 1000])

C_23 = multimeter_error_array(C_arr_23, C_scale_arr_23, 'm', 'c', ignore_gain=True)
#Contains Cf, C1

freq_23 = ufloat(50, 0)

Rf_23 = ufloat_single_value(1.0008 * 10**(6), 10**7, 'm', 'ohm')

Vin_23 = np.array([])
Vout_23 = np.array([])
Vin_vdiv_23 = np.array([])
Vout_vdiv_23 = np.array([])

transfer_23 = dataset(Vin_23, Vout_23, 'v', 'v')
transfer_23.calculate_error(Vin_vdiv_23, 'x', 'o')
transfer_23.calculate_error(Vout_vdiv_23, 'y', 'o')

# RADDRIZZATORE DI PRECISIONE CON OPERAZIONALI: 3
