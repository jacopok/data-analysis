from fits_multimeter_errors import *
from mosfet_load_data_basics import *

def print_sat(arr):
    sat = []
    for x in arr:
        if(x == 0):
            sat.append("")
        elif(x == 1):
            sat.append("Saturazione")
        else:
            return(None)
    return(sat)

#1.1

I_d_qpt_11 = ufloat_single_value(801.61 * 10**(-6) , 10**(-3), 'm', 'a')
V_gs_qpt_11 = ufloat_single_value(2.373, 6, 'a', 'v')
V_ds_qpt_11 = ufloat_single_value(7, 60, 'a', 'v')

I_d_qpt_teor_11 = ufloat(8e-4, 0)
V_ds_qpt_teor_11 = ufloat(7, 0)

Names_11 = ["I_d" , "V_{gs}", "V_{ds}"]
Vars_11 = np.array([I_d_qpt_11, V_gs_qpt_11, V_ds_qpt_11])
Units_11 = ["A", "V", "V"]

#print_ufloat_array(Names_11, Vars_11, Units_11)

#1.2

V_ds_arr_12 = [1.002, 2, 3, 4, 5.006, 6.002, 7, 8, 9, 10, 11]
V_ds_scale_arr_12 = [6, 6, 6, 6, 6, 6, 60, 60, 60, 60, 60]

I_d_arr_12 = np.array([743.5, 766.1, 777.15, 784.5, 790.05,
                       795.52, 801.61, 805.5, 810.67, 815.80, 821.73]) * 10**(-6)
I_d_scale_arr_12 = np.ones(11) * 10**(-3)


characteristic_12 = dataset(V_ds_arr_12, I_d_arr_12, 'v', 'a')
characteristic_12.calculate_error(I_d_scale_arr_12, 'y', 'm')
characteristic_12.calculate_error(V_ds_scale_arr_12, 'x', 'a')

characteristic_12.point_ignore = np.array([1, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0])

m_12, q_12 = characteristic_12.fit_uarray()

r_0_12 = 1 / m_12
lambda_n_12 = m_12 / q_12

#values from SPICE simulation, without error
I_d_arr_spice_12 = np.array([711.32, 758.4, 765.17, 771.97, 778.78, 785.59,
                             792.4, 799.2, 806.01, 812.81, 819.62]) * 1e-6

I_d_uarray_12 = characteristic_12.data_uarray("y")
I_d_ratios_uarray_12 = (I_d_uarray_12 - I_d_arr_spice_12) / I_d_arr_spice_12
I_d_ratios_12 = 100 * np.array([x.n for x in I_d_ratios_uarray_12])
#percent differences between simulation and measured values

M_12 = np.stack((characteristic_12.data_uarray("x"), V_ds_scale_arr_12,
                 characteristic_12.data_uarray("y"), I_d_arr_12,
                 print_sat(characteristic_12.point_ignore))).T
                 
M_Id_12 = np.stack((I_d_uarray_12, I_d_arr_spice_12, I_d_ratios_12)).T
                 
column_names_12 = "$V_{DS}$ & fondoscala & $I_D$ & fondoscala & Triodo"
#print_matrix(M_12, column_names_12)

Names_12 = ["m", "q", "r_0", "\lambda_n"]
Vars_12 = np.array([m_12, q_12, r_0_12, lambda_n_12])
Units_12 = ["S", "A", "\Omega", "V^{-1}"]

#print_ufloat_array(Names_12, Vars_12, Units_12)

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

#values from SPICE simulation, without error
I_d_arr_spice_13 = np.array([380.04, 567.49, 792.4, 1054.75, 1354.55, 1691.08]) * 1e-6

I_d_ratios_uarray_13 = np.abs(I_d_13 - I_d_arr_spice_13) / I_d_arr_spice_13
I_d_ratios_13 = 100 * np.array([x.n for x in I_d_ratios_uarray_13])
#percent differences between simulation and measured values

Names_13 = ["m", "q", "k_n", "V_{TN}", "g_m^{qpt}"]
Vars_13 = np.array([m_13, q_13, k_n_13, V_TN_13, g_m_qpt_13])
Units_13 = ["A^{1/2}V^{-1}", "A^{1/2}", "AV^{-2}", "V", "S"]

print()
#print_ufloat_array(Names_13, Vars_13, Units_13)

M_13 = np.stack((characteristic_gs_13.data_uarray("x"), V_gs_scale_arr,
                 I_d_13, I_d_scale_arr_13, Y_13)).T

column_names_13 = "$V_{gs}$ & fondoscala & $I_d$ & fondoscala & Y"                 

M_Id_13 = np.stack((I_d_13, I_d_arr_spice_13, I_d_ratios_13)).T

#print_matrix(M_Id_13)

#print_matrix(M_13, column_names_13)