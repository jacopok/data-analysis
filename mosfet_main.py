from fits_multimeter_errors import *
from mosfet_load_data_4 import *

characteristic_12.full_plot('$V_{ds}$', '$I_d$', 'p12completo')
characteristic_12.residuals_plot('Vds-Vteor', '$I_d$', 'p12residui')

characteristic_gs_13.full_plot('$V_{gs}$', '$Y$', 'p13completo')
characteristic_gs_13.residuals_plot('$V_{gs}$', '$Y-Y_{model}$', 'p13residui')

maximum_ignored_12 = 6
values = np.empty((5, maximum_ignored_12))

values[0,:] = range(maximum_ignored_12)

for i in range(maximum_ignored_12):
    characteristic_12.point_ignore *=0
    for j in range(i):
        characteristic_12.point_ignore[j] = 1
    characteristic_12.fit()
    #characteristic_12.residuals_plot(figname="ignored" + str(i))
    values[1:,i] = characteristic_12.goodness_of_fit()
values = values.T
print_matrix(values, low_precision=True,
    column_names = "Ignored points & $p$-value & $ \\chi ^2$ & $\\chi ^2 /\\nu$ & $z$-score")