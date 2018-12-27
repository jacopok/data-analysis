from fits_multimeter_errors import *
from mosfet_load_data_2 import *

A_ass_CS = ufloat(-8, 0.8)

#3.1

R_VM = ufloat(10000000, 0)

# R_2 calcolata: ((15- (V_gs_qpt_11 + R[3] * I_d_qpt_11))/ (V_gs_qpt_11 + R[3] * I_d_qpt_11)) * R[2]


# 3.2

V_DD_32 = ufloat_single_value(15.01, 60, 'a', 'v')
V_Rd_32 = ufloat_single_value(5.358, 6, 'a', 'v') # ai capi di Rd
V_S_32 = ufloat_single_value(2.620, 6, 'a', 'v') # ai capi di Rs
V_DS_32 = V_DD_32 - V_S_32 - V_Rd_32 # per chirciof

Rp_32 = res_parallel(R_VM, R[2])

V_Gvoltm_32 = ufloat_single_value(4.878, 6, 'a', 'v')

V_G_32 = V_Gvoltm_32 * R[2] / (R[2] + R[4]) * (Rp_32 + R[4])/Rp_32
V_GS_32 = V_G_32 - V_S_32

I_D_32 = V_Rd_32 / R[5]
g_m_32 = 2 * I_D_32 / (V_GS_32 - V_TN_13)

A_att_32 = - R[5] * g_m_32

Names_32 = ["V_{DD}", "V_{Rd}", "V_S", "V_{DS}", "R_p", "V_G^{voltm}", "V_G", "V_{GS}",
            "I_D", "g_m", "A_{attesa}"]
Vars_32 = np.array([V_DD_32, V_Rd_32, V_S_32, V_DS_32, Rp_32, V_Gvoltm_32,
                    V_G_32, V_GS_32, I_D_32, g_m_32, A_att_32])
Units_32 = ["V", "V", "V", "V", "\Omega", "V", "V", "V", "A", "S", ""]

#print_ufloat_array(Names_32, Vars_32, Units_32)

# 3.3

f_33 = ufloat(10000, 0)


Vin_33 = ufloat_single_value(.204, 0.05, 'o', 'v')
Vout_33 = ufloat_single_value(1.65, .2, 'o', 'v')

A_sper_33 = Vout_33 / Vin_33

Names_33 = ["V_{in}", "V_{out}", "A_{sper}"]
Vars_33 = np.array([Vin_33, Vout_33, A_sper_33])
Units_33 = ["V", "V", ""]

#print_ufloat_array(Names_33, Vars_33, Units_33)

# 3.4

R_in_cs_34 = res_parallel(R[2], R[4])
R_out_cs_34 = res_parallel(r_0_12, R[5])

V_in_34 = ufloat_single_value(.206, .050, 'o', 'v')
V_out_34 = ufloat_single_value(1.27, .2, 'o', 'v')

V_out_load_34 = ufloat_single_value(.728, .05, 'o', 'v')

A_teor_34 = g_m_32 * res_parallel(R[5], r_0_12)
#da comparare con A_sper_33!

R_in_34 = R[6] * V_out_34 / (V_in_34 * A_sper_33 - V_out_34 )
R_out_load_34 = R[7] * ((V_in_34 * A_sper_33 / V_out_load_34 ) - 1 )

Names_34 = ["R_{in}^{cs}", "R_{out}^{cs}", "V_{in}", "V_{out}", "V_{out}^{load}",
            "A_{teor}", "R_{in}", "R_{out}^{load}"]
Vars_34 = np.array([R_in_cs_34, R_out_cs_34, V_in_34, V_out_34,
                    V_out_load_34, A_teor_34, R_in_34, R_out_load_34])
Units_34 = ["\Omega", "\Omega", "V", "V", "V", "", "\Omega", "\Omega", "\Omega"]

#print_ufloat_array(Names_34, Vars_34, Units_34)

# 3.5

f_35 = ufloat(10**4, 0)

V_in_35 = ufloat_single_value(.206, .05, 'o', 'v')
V_out_35 = ufloat_single_value(.320, .05, 'o', 'v')

A_exp_35 = - V_out_35 / V_in_35
A_teor_35 = - g_m_32 * res_parallel(R[5], r_0_12) / (1 + g_m_32 * R[3])

Names_35 = ["V_{in}", "V_{out}", "A_{sper}", "A_{teor}"]
Vars_35 = np.array([V_in_35, V_out_35, A_exp_35, A_teor_35])
Units_35 = ["V", "V", "", ""]

#print_ufloat_array(Names_35, Vars_35, Units_35)

# 3.6

f_36 = ufloat(10000, 0)

V_in_36 = ufloat_single_value(.2, .05, 'o', 'v')
V_out_36 = ufloat_single_value(.139, .05, 'o', 'v')
V_in_noload_36 = ufloat_single_value(.194, .05, 'o', 'v')
V_out_noload_36 = ufloat_single_value(.148, .05, 'o', 'v')

A_exp_36 = V_out_36 / V_in_36
A_exp_noload_36 = V_out_noload_36 / V_in_noload_36
A_teor_noload_36 = g_m_32 * res_parallel(R[3], r_0_12) / (1 + g_m_32 * res_parallel(R[3], r_0_12))
A_teor_36 = g_m_32 * res_parallel(R[3], res_parallel(r_0_12, R[7])) / (1 + g_m_32 * res_parallel(R[3], res_parallel(r_0_12, R[7])))

R_out_36 = res_parallel(1/g_m_32, res_parallel(R[3], r_0_12))
R_out_cd_36 = R[7] * (A_teor_noload_36 * V_in_36 / V_out_36 - 1)

Names_36 = ["V_{in}", "V_{out}", "V_{in}^{noload}", "V_{out}^{noload}",
            "A_{sper}", "A_{sper}^{noload}", "A_{teor}", "A_{teor}^{noload}",
            "R_{out}",  "R_{out}^{cd}"]
Vars_36 = np.array([V_in_36, V_out_36, V_in_noload_36, V_out_noload_36,
                    A_exp_36, A_exp_noload_36, A_teor_36, A_teor_noload_36,
                    R_out_36, R_out_cd_36])
Units_36 = ["V", "V", "V", "V", "", "", "", "", "\Omega", "\Omega"]

#print_ufloat_array(Names_36, Vars_36, Units_36)