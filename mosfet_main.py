from fits_multimeter_errors import *
from mosfet_load_data_4 import *

characteristic_12.full_plot('$V_{ds}$', '$I_d$', 'Punto 12: plot completo')
characteristic_12.residuals_plot('Vds-Vteor', '$I_d$', 'Punto12: residui')

characteristic_gs_13.full_plot('$V_{gs}$', '$Y$', 'Punto 13: plot completo')
characteristic_gs_13.residuals_plot('$V_{gs}$', '$Y-Y_{model}$', 'Punto 13: residui')