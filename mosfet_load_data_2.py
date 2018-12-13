from fits_multimeter_errors import *
from mosfet_load_data_1 import *

# 2.1

V_DD_21 = ufloat_single_value(5, 6, 'a', 'v')

V_GS_arr_21 = [.1926, 5]
V_GS_scale_arr_21 = [.6, 6]

V_GS_21 = multimeter_error_array(V_GS_arr_21, V_GS_scale_arr_21, 'a', 'v')

V_DS_arr_21 = [4.996, .1066]
V_DS_scale_arr_21 = [6, .6]

V_DS_21 = multimeter_error_array(V_DS_arr_21, V_DS_scale_arr_21, 'a', 'v')

V_DS_th_21 = V_DD_21 - V_GS_21 #??? forse sbagliato

# 2.2 

V_gs_22 = ufloat_single_value(1.782, 6, 'a', 'v')
V_ds_22 = ufloat_single_value(2.782, 6, 'a', 'v')
f_22 = ufloat(1000, 0)
V_in_22 = ufloat_single_value(.206, .05, 'o', 'v')
V_out_22 = ufloat_single_value(1.31, .2, 'o', 'v')

V_ds_sat_22 = V_gs_22 - V_TN_13

A_vt_exp_22 = V_out_22 / V_in_22

g_m_22 = #RICALCOLARE

A_vt_teor_22 = - g_m_22 * res_parallel(r_0_12, R[1])

I_d_22 = ufloat_single_value(.00022287, .001, 'm', 'a')