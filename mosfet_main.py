from fits_multimeter_errors import *
from mosfet_load_data_4 import *

characteristic_12.full_plot('$V_{ds}$', '$I_d$', 'p12completo')
characteristic_12.residuals_plot('Vds-Vteor', '$I_d$', 'p12residui')

characteristic_gs_13.full_plot('$V_{gs}$', '$Y$', 'p13completo')
characteristic_gs_13.residuals_plot('$V_{gs}$', '$Y-Y_{model}$', 'p13residui')