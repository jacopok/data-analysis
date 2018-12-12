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

Rp_32 = (R_VM * R[2])/(R_VM + R[2])

V_Gvoltm_32 = ufloat_single_value(4.878, 6, 'a', 'v')

V_G_32 = V_Gvoltm_32 * R[2] / (R[2] + R[4]) * (Rp_32 + R[4])/Rp_32
V_GS_32 = V_G_32 - V_S_32

I_D_32 = V_Rd_32 / R[5]
g_m_32 = 2 * I_D_32 / (V_GS_32 - V_TN_13)

A_att_32 = - R[5] * g_m_32

# 3.3

f_33 = ufloat(10000, 0)


Vin_33 = ufloat_single_value(.204, 0.05, 'o', 'v')
Vout_33 = ufloat_single_value(1.65, .2, 'o', 'v')

A_sper_33 = - Vout_33 / Vin_33