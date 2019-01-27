from fits_multimeter_errors import *
from mosfet_load_data_4 import *

characteristic_12.full_plot('$V_{ds}$ [V]', '$I_d$ [A]', 'p12completo')
characteristic_12.residuals_plot('$V_{ds}$ [V]', '$I_d - I_d^{fit}$ [A]', 'p12residui')

characteristic_gs_13.full_plot('$V_{gs}$ [V]', '$Y$ [A$^{1/2}$]', 'p13completo')
characteristic_gs_13.residuals_plot('$V_{gs}$ [V]', '$Y-Y_{fit}$ [A$^{1/2}$]', 'p13residui')

maximum_ignored_12 = 6
values = np.empty((5, maximum_ignored_12))

values[0,:] = range(maximum_ignored_12)

for i in range(maximum_ignored_12):
    characteristic_12.point_ignore *=0
    for j in range(i):
        characteristic_12.point_ignore[j] = 1
    fit = characteristic_12.fit()
    #characteristic_12.residuals_plot(figname="ignored" + str(i))
    values[1:,i] = characteristic_12.goodness_of_fit()
values = values.T
#print_matrix(values, low_precision=True,
#    column_names = "Ignored points & $p$-value & $ \\chi ^2$ & $\\chi ^2 /\\nu$ & $z$-score")


#print(characteristic_gs_13.goodness_of_fit())

def Id(Vds, Vgs, Vtn, Kn, lambda_n):
    if(Vgs < Vtn):
        return(None)
    if(Vds < Vgs - Vtn):
        Id = Kn * (Vgs - Vtn - Vds / 2) * Vds
        #TRIODE
    else:
        Id = Kn / 2 * (Vgs - Vtn)**2 * (1 + lambda_n * Vds)
        #SATURATION
    return(Id)
Id_v = np.vectorize(Id)

def Id_sat(Vds, Vtn, Kn, lambda_n):
    return(Id(Vds, Vds+Vtn, Vtn, Kn, lambda_n))
Id_sat_v = np.vectorize(Id_sat)

def Id_sat_gs(Vgs, Vtn, Kn, lambda_n):
    return(Id(Vds-Vtn, Vgs, Vtn, Kn, lambda_n))
Id_sat_gs_v = np.vectorize(Id_sat_gs)
    
Vds = np.linspace(0, 12, num=400)
Vgs_array = np.concatenate((np.linspace(0, V_gs_qpt_11.n, num=3, endpoint=False), 
                            np.linspace(V_gs_qpt_11.n, 2 * V_gs_qpt_11.n, num=4)))
for Vgs in Vgs_array:
    I = Id_v(Vds, Vgs, V_TN_13.n, k_n_13.n, lambda_n_12.n)
    plt.plot(Vds, I, label = ("$V_{GS} \\approx $ " + '{0:.{1}f}'.format(Vgs, 1) + " V"))
plt.errorbar(x=characteristic_12.x_array, y=characteristic_12.y_array,
             yerr=characteristic_12.error_array, fmt = 'bo', marker = 'x',
             label = "Dati sperimentali")

Imax = Id_v(Vds[-1], Vgs_array[-1], V_TN_13.n, k_n_13.n, lambda_n_12.n)

#Vds_sat_array = Vds[Id_sat_v(Vds, V_TN_13.n, k_n_13.n, lambda_n_12.n) is not None]
#plt.fill_between(Vds, Id_sat_v(Vds, V_TN_13.n, k_n_13.n, lambda_n_12.n))

plt.ylim([0,Imax])
plt.plot(Vds, Id_sat_v(Vds, V_TN_13.n, k_n_13.n, lambda_n_12.n),linestyle="--",
         label = "Separazione triodo-saturazione")

plt.xlabel("$V_{DS} [V]$", fontsize=12)
plt.ylabel("$I_d [A]$", fontsize=12)
plt.legend(loc=1)
plt.tight_layout()
plt.savefig('figures/characteristic_vds', dpi = 600)
plt.close()

Vgs = np.linspace(1.5, 5, num=400)
Vds_array = np.linspace(1, 7, num=7)
for Vds in Vds_array:
    I = Id_v(Vds, Vgs, V_TN_13.n, k_n_13.n, lambda_n_12.n)
    plt.plot(Vgs, I, label = ("$V_{DS} \\approx $ " + '{0:.{1}f}'.format(Vds, 1) + " V"))
plt.errorbar(x=characteristic_gs_13.x_array, y=unumpy.nominal_values(I_d_13),
            yerr=unumpy.std_devs(I_d_13), fmt = 'bo', marker = 'x',
            label = "Dati sperimentali")

Imax = Id_v(Vds_array[-1], Vgs[-1], V_TN_13.n, k_n_13.n, lambda_n_12.n)

plt.ylim([0,Imax])
plt.plot(Vgs, Id_sat_gs_v(Vgs, V_TN_13.n, k_n_13.n, lambda_n_12.n),linestyle="--",
         label = "Separazione triodo-saturazione")

plt.xlabel("$V_{GS} [V]$", fontsize=12)
plt.ylabel("$I_d$ [A]", fontsize=12)
plt.legend(loc=0)
plt.tight_layout()
plt.savefig('figures/characteristic_vgs', dpi = 600)
plt.close()
