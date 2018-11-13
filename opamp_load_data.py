from fits_multimeter_errors import *


def test_initialization():
    global test
    test = dataset([1, 2, 3], [1, 1.6, 2], 'v', 'a')
    test.y_error_array = [0.1, 0.05, 0.2]
    
# 1: MISURA DELLA CURVA DI TRASFERIMENTO PER UN AMPLIFICATORE INVERTENTE 

R_arr_1 = np.array([])
R_scale_arr_1 = np.array([])

R_1 = multimeter_error_array(R_arr_1, R_scale_arr_1, 'm', 'ohm', ignore_gain=True)
#contains R1, R2, R3 with uncertainties. CHECH MULT TYPE

m_theory_1 = - R_1[1] / R_1[0]

freq_1 = ufloat(, 0)

Vin_plus_1 = np.array([])
Vout_plus_1 = np.array([])
Vin_minus_1 = np.array([])
Vout_minus_1 = np.array([])
Vin_plus_vdiv_1 = np.array([])
Vout_plus_vdiv_1 = np.array([])
Vin_minus_vdiv_1 = np.array([])
Vout_minus_vdiv_1 = np.array([])

transfer_plus_1 = dataset(Vin_plus_1, Vout_plus_1, 'v', 'v')
transfer_minus_1 = dataset(Vin_minus_1, Vout_minus_1, 'v', 'v')

transfer_plus_1.calculate_error(Vin_plus_vdiv_1, 'x', 'o')
transfer_plus_1.calculate_error(Vout_plus_vdiv_1, 'y', 'o')
transfer_minus_1.calculate_error(Vin_minus_vdiv_1, 'x', 'o')
transfer_minus_1.calculate_error(Vout_minus_vdiv_1, 'y', 'o')

# 2: AMPLIFICATORE DELLE DIFFERENZE – AMPLIFICATORE NON INVERTENTE

R_arr_21 = np.array([])
R_scale_arr_21 = np.array([])

R_21 = multimeter_error_array(R_arr_21, R_scale_arr_21, 'm', 'ohm', ignore_gain=True)
#contains R1, R2, R3 (b) 

freq_21 = ufloat(, 0)

#Non-invertent: 2.1

Vin_arr_21 = np.array([])
Vin_scale_arr_21 = np.array([])
Vout_arr_21  = np.array([])
Vout_scale_arr_21 = np.array([])

Vin_21 = multimeter_error_array(Vin_arr_21, Vin1_scale_arr_21, '', 'v')
Vout_21 = multimeter_error_array(Vout_arr_21, Vout_scale_arr_21, '', 'v')

#Amp differences: 2.1

Vin1_arr_21 = np.array([])
Vin1_scale_arr_21 = np.array([])
Vin2_arr_21 = np.array([])
Vin2_scale_arr_21 = np.array([])
Vout1_arr_21 = np.array([]) 
Vout1_scale_arr_21 = np.array([])

Vin1_21 = multimeter_error_array(Vin1_arr_21, Vin1_scale_arr_21, '', 'v')
Vin2_21 = multimeter_error_array(Vin2_arr_21, Vin2_scale_arr_21, '', 'v')
Vout1_21 = multimeter_error_array(Vout1_arr_21, Vout1_scale_arr_21, '', 'v')

#Amp sums invertent: 2.2

R_arr_22 = np.array([])
R_scale_arr_22 = np.array([])

R_22 = multimeter_error_array(R_arr_22, R_scale_arr_22, 'm', 'ohm', ignore_gain=True)
#contains Rf, R1, R1b

Vin1_arr_22 = np.array([])
Vin1_scale_arr_22 = np.array([])
Vin2_arr_22 = np.array([])
Vin2_scale_arr_22 = np.array([])
Vout1_arr_22 = np.array([]) 
Vout1_scale_arr_22 = np.array([])

Vin1_22 = multimeter_error_array(Vin1_arr_22, Vin1_scale_arr_22, '', 'v')
Vin2_22 = multimeter_error_array(Vin2_arr_22, Vin2_scale_arr_22, '', 'v')
Vout1_22 = multimeter_error_array(Vout1_arr_22, Vout1_scale_arr_22, '', 'v')


#Integrator for impulses: 2.3

C_arr_23 = np.array([])
C_scale_arr_23 = np.array([])

C_23 = multimeter_error_array(C_arr_23, C_scale_arr_23, '', 'c', ignore_gain=True)
#Contains Cf, C1

freq_23 = ufloat(, 0)

Rf_val_23 = 
Rf_scale_23 = 
Rf_23 = ufloat(Rf_val_23, multimeter_error(Rf_val_23, Rf_scale_23, '', 'ohm'))

Vin_23 = np.array([])
Vout_23 = np.array([])
Vin_vdiv_23 = np.array([])
Vout_vdiv_23 = np.array([])

transfer_23 = dataset(Vin_23, Vout_23, 'v', 'v')
transfer_23.calculate_error(Vin_vdiv_23, 'x', 'o')
transfer_23.calculate_error(Vout_vdiv_23, 'y', 'o')

# RADDRIZZATORE DI PRECISIONE CON OPERAZIONALI: 3

