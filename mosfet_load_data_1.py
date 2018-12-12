from fits_multimeter_errors import *
from mosfet_load_data_basics import *

#1.1

I_d_qpt_11 = ufloat_single_value(801.61 * 10**(-6) , 10**(-3), 'm', 'a')
V_gs_qpt_11 = ufloat_single_value(2.373, 6, 'a', 'v')
V_ds_qpt_11 = ufloat_single_value(7, 60, 'a', 'v')

#1.2

V_ds_arr_12 = [1.002, 2, 3, 4, 5.006, 6.002, 7, 8, 9, 10, 11]
V_ds_scale_arr_12 = [6, 6, 6, 6, 6, 6, 60, 60, 60, 60, 60]

I_d_arr_12 = np.array([743.5, 766.1, 777.15, 784.5, 790.05,
                       795.52, 801.61, 805.5, 810.67, 815.80, 821.73]) * 10**(-6)
I_d_scale_arr_12 = np.ones(11) * 10**(-3)

characteristic_12 = dataset(V_ds_arr_12, I_d_arr_12, 'v', 'a')
characteristic_12.calculate_error(I_d_scale_arr_12, 'y', 'm')
characteristic_12.calculate_error(V_ds_scale_arr_12, 'x', 'a')

m_12, q_12 = characteristic_12.fit_uarray()

r_0_12 = 1 / m_12
lambda_n_12 = m_12 / q_12

#1.3

V_gs_arr = [1.973, 2.173, 2.373, 2.573, 2.773, 2.973]
V_gs_scale_arr = [6, 6, 6, 6, 6, 6]

I_d_arr_13 = np.array([376.55, 570.12, 799.95, 1063.3, 1355.1, 1675]) * 10**(-6)
I_d_scale_arr_13 = np.array([1, 1, 1, 10, 10, 10]) * 10**(-3)

I_d_13 = multimeter_error_array(I_d_arr_13, I_d_scale_arr_13, 'm', 'a')

Y_13 = unumpy.sqrt(I_d_13 / (1 + lambda_n_12 * V_ds_qpt_11))

characteristic_gs_13 = dataset(V_gs_arr, unumpy.nominal_values(Y_13), 'a', 'v')

characteristic_gs_13.y_error_array = unumpy.std_devs(Y_13)
characteristic_gs_13.calculate_error(V_gs_scale_arr, 'x', 'a')

m_13, q_13 = characteristic_gs_13.fit_uarray()

k_n_13 = 2 * m_13 * m_13
V_TN_13 = - q_13 / m_13

g_m_qpt_13 = 2 * I_d_qpt_11 / (V_gs_qpt_11 - V_TN_13)