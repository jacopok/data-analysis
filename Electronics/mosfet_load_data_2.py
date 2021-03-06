from fits_multimeter_errors import *
from mosfet_load_data_1 import *
import itertools

# 2.1

V_DD_21 = ufloat_single_value(5, 6, 'a', 'v')

V_GS_arr_21 = [.1926, 5]
V_GS_scale_arr_21 = [.6, 6]

V_GS_21 = multimeter_error_array(V_GS_arr_21, V_GS_scale_arr_21, 'a', 'v')

V_DS_arr_21 = [4.996, .1066]
V_DS_scale_arr_21 = [6, .6]

V_DS_SPICE_21 = [5, 0.145]

V_DS_21 = multimeter_error_array(V_DS_arr_21, V_DS_scale_arr_21, 'a', 'v')

V_DS_th_21 = V_DD_21 - V_GS_21 #inizializzazione di base, poi sistemata
R_on_21 = 1/k_n_13 /(V_GS_21[1] - V_TN_13)

V_DS_th_21[1] = V_DD_21 * R_on_21 / (R_on_21 + R[1])

M_21 = np.stack((V_GS_21, V_GS_scale_arr_21, V_DS_21,
                 V_DS_scale_arr_21, V_DS_SPICE_21)).T

col_names_21 = "$V_{GS}$ & v/div & $V_{DS}$ & v/div & $V_{DS}^{SPICE}$"

#print_matrix(M_21, col_names_21, uniform_units="V")

lambda_array_21 = []

for pair in itertools.combinations((V_DS_21, V_DS_SPICE_21, V_DS_th_21), r=2):
    lambda_array_21.append(uarray_compatibility(*pair))

M_lambda_21 = np.stack(lambda_array_21).T

#print_matrix(M_lambda_21)

# 2.2 

R_VM = ufloat(10000000, 0)

V_gs_22 = ufloat_single_value(1.782, 6, 'a', 'v') 
V_ds_22 = ufloat_single_value(2.782, 6, 'a', 'v')
f_22 = 1000
V_in_22 = ufloat_single_value(.206, .05, 'o', 'v')
V_out_22 = ufloat_single_value(1.31, .2, 'o', 'v')

V_ds_sat_22 = V_gs_22 - V_TN_13

A_vt_exp_22 = - V_out_22 / V_in_22

I_D_exp_22 = (V_DD_21 - V_ds_22) / R[1]

g_m_22 = sqrt(2 * I_D_exp_22 * k_n_13)
#g_m_22 = 2 * I_D_exp_22 / (V_gs_22 - V_TN_13)

r_0_22 = (1 / lambda_n_12 + V_ds_22) / I_D_exp_22

A_vt_teor_22 = - g_m_22 * res_parallel(r_0_22, R[1])

I_d_22 = ufloat_single_value(.00022287, .001, 'm', 'a')

g_m_amp_22 = sqrt(2 * I_d_22 * k_n_13)

A_vt_teor_amp_22 = - g_m_amp_22 * res_parallel(r_0_12, R[1])

Names_22 = ["V_{gs}", "V_{ds}", "V_{in}", "V_{out}",
            "V_{ds}^{sat}", "A_{sper}",
            "I$ misurata come tensione su resistenza $I_D  ",
            "g_m", "A_{teor}", "I$ misurata con amperometro $I_D"]
Vars_22 = np.array([V_gs_22, V_ds_22, V_in_22, V_out_22, V_ds_sat_22, A_vt_exp_22,
                    I_D_exp_22, g_m_22, A_vt_teor_22, I_d_22])
Units_22 = ["V", "V", "V", "V", "V", "", "A", "S", "", "A"]

#print_ufloat_array(Names_22, Vars_22, Units_22)