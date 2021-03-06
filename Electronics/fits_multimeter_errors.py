import numpy as np
import scipy
from scipy import optimize
import scipy.stats as sps
import matplotlib.pyplot as plt
from uncertainties import *
from uncertainties.umath import *
from uncertainties import unumpy
import math

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{amssymb}')
plt.rc('font', family='serif')


class dataset:
    def __init__(self, x_array, y_array, x_type, y_type):
        self.x_array = np.array(x_array)
        self.y_array = np.array(y_array)
        self.x_type = x_type
        self.y_type = y_type
        self.x_error_array = np.array([])
        self.y_error_array = np.array([])
        self.error_array = np.array([])
        self.y_prediction = np.array([])
        self.point_ignore = np.zeros(len(self.x_array)) #zero for points to keep, 
        #one for points to ignore

    def calculate_error(self, scale_array, axis, multimeter_type):
        if (axis=='x'):
            array = self.x_array
            data_type = self.x_type
        elif (axis=='y'):
            array = self.y_array
            data_type = self.y_type
        else:
            print("axis must be x or y")
            return(None)
        
        if (len(scale_array) != len(array)):
            print("scale_array must be have the same length as the data array")
            return(None)
        else:
            n = len(scale_array)
        
        test_error_array = np.zeros(n)
        
        for i in range(n):
            test_error_array[i] = multimeter_error(array[i],
                       scale_array[i], multimeter_type, data_type)
            
        if (axis=='x'):
            self.x_error_array = test_error_array
        elif (axis=='y'):
            self.y_error_array = test_error_array
        
        return(0)
        
    def model(self, x, a, b):
        y = x * a + b
        return(y)
        
    def fit (self, initial_params=None, correct_for_bad_fit=False):
        """
        fits the model
        
        returns params (if y=mx+q: first m, then q), error_params
        """
        x_array = self.x_array[self.point_ignore==0]
        y_array = self.y_array[self.point_ignore==0] 
        y_error_array = self.y_error_array[self.point_ignore==0]
        x_error_array = self.x_error_array[self.point_ignore==0]
        
        test_params, test_pcov = scipy.optimize.curve_fit(self.model, x_array, y_array,
                                      sigma=y_error_array, p0=initial_params, absolute_sigma=True)
        
        self.error_array = np.sqrt(self.y_error_array**2 +
                              (test_params[0] * self.x_error_array)**2)
        error_array = self.error_array[self.point_ignore==0]
        
        params, pcov = scipy.optimize.curve_fit(self.model, x_array, y_array,
                                      sigma=error_array, p0=initial_params, absolute_sigma=True)
        
        
        error_params = []
        for i in range(np.shape(pcov)[0]):
            error_params.append(np.sqrt(pcov[i,i]))
        error_params = np.array(error_params)

            
        if(correct_for_bad_fit == True):
            gof = self.goodness_of_fit()
            chi2_over_dof = gof[1] / gof[2]
            error_params = np.array(error_params)
            error_params *= np.sqrt(chi2_over_dof)
        return(params, error_params)
        
    def fit_uarray (self, initial_params=None):
        params, error_params = self.fit(initial_params)
        m = ufloat(params[0], error_params[0])
        q = ufloat(params[1], error_params[1])
        return m, q
    
    def calculate_residuals(self):
        params, error_params = self.fit()
        self.calculate_y_prediction()
        residuals = self.y_array - self.y_prediction
        return(residuals)
    
    def calculate_y_prediction(self):
        params, error_params = self.fit()
        y_model = []
        for x in self.x_array:
            y_model.append(self.model(x, *params))
        self.y_prediction = np.array(y_model)

        
    def goodness_of_fit(self):
        """
        Returns: p value, chi squared value,
        degrees of freedom, z-score of p value
        
        """
        
        self.calculate_y_prediction()
        y_array = self.y_array[self.point_ignore==0]
        y_prediction = self.y_prediction[self.point_ignore==0]
        y_error_array = self.error_array[self.point_ignore==0]
        df = len(y_array) - 2
        chi2 = sps.chi2(df=df)
        square_deviation = ((y_array - y_prediction) / y_error_array)**2
        sum_square_deviation = np.sum(square_deviation, axis=0)
        pvalue = chi2.sf(x=sum_square_deviation)
        sigma = chi2.std()
        mean = chi2.mean()
        
        return(pvalue, sum_square_deviation, df, (sum_square_deviation-mean)/sigma)
        
        
    def full_plot(self, xlabel='', ylabel='', figname='', plot_ignored=True):
        """Plots the data with the corresponding errors, along with the model
        
        """

        if(len(self.y_error_array) != len(self.y_array)):
            print('Must calculate errors first')
            return(None)
        
        m, q = self.fit_uarray()
        
        x_array = self.x_array[self.point_ignore==0]
        y_array = self.y_array[self.point_ignore==0]
        y_error_array = self.error_array[self.point_ignore==0]

        #Create gradual x values for plotting
        n_steps = 1000
        percent_plot_excess = 0.05
        if(plot_ignored==True):
            x_min = np.min(self.x_array)
            x_max = np.max(self.x_array)
        else:
            x_min = np.min(x_array)
            x_max = np.max(x_array)
        x_step = (x_max - x_min) / n_steps
        x_excess = n_steps * percent_plot_excess * x_step
        x_range = np.arange(x_min-x_excess, x_max+x_excess, x_step)
        
        #Generate arrays for ignored data points
        x_extra_array = self.x_array[self.point_ignore==1]
        y_extra_array = self.y_array[self.point_ignore==1]
        y_extra_error_array = self.error_array[self.point_ignore==1]
        
        #Generate y values for model plot
        params, error_params = self.fit()
        y_range = self.model(x_range, params[0], params[1])
        
        plt.plot(x_range, y_range, '--')
        plt.errorbar(x=x_array, y=y_array, yerr=y_error_array, fmt = 'bo', marker = '.')
        if(plot_ignored==True):
            plt.errorbar(x=x_extra_array, y=y_extra_array, yerr=y_extra_error_array, fmt = 'bo', mfc = 'grey', mec = 'grey', ecolor = 'grey')
        plt.xlabel(xlabel, fontsize = 12)
        plt.ylabel(ylabel, fontsize = 12)
        plt.tight_layout()
        plt.savefig('figures/' + figname, dpi = 600)
        plt.close()
    
    def residuals_plot(self, xlabel='', ylabel='', figname='', plot_ignored = True):
        all_residuals = self.calculate_residuals()
        if(len(self.y_error_array) != len(all_residuals)):
            print('Must calculate errors first')
            return(0)
        
        m, q = self.fit_uarray()
        
        x_array = self.x_array[self.point_ignore==0]
        y_error_array = self.error_array[self.point_ignore==0]
        residuals = all_residuals[self.point_ignore==0]
        
        x_extra_array = self.x_array[self.point_ignore==1]
        y_extra_error_array = self.error_array[self.point_ignore==1]
        extra_residuals = all_residuals[self.point_ignore==1]
        
        if(plot_ignored==True):
            plt.plot(self.x_array, np.zeros(len(all_residuals)), '--')
        else:
            plt.plot(x_array, np.zeros(len(residuals)), '--')
        plt.errorbar(x_array, residuals, y_error_array, fmt = 'bo', marker = 'x')
        if(plot_ignored==True):
            plt.errorbar(x=x_extra_array, y=extra_residuals, yerr=y_extra_error_array, fmt = 'bo', mfc = 'grey', mec = 'grey', ecolor = 'grey')
        plt.xlabel(xlabel, fontsize = 12)
        plt.ylabel(ylabel, fontsize = 12)
        plt.tight_layout()
        plt.savefig('figures/' + figname, dpi = 600)
        plt.close()
    
    def data_uarray(self, axis):
        """
        Returns array of ufloats of the x or y data points.
        The errors must have been calculated beforehand.
        """
        
        if(axis=="x"):
            values = self.x_array
            errors = self.x_error_array
        elif(axis=="y"):
            values = self.y_array
            errors = self.y_error_array
        else:
            print("Axis can only be x or y!")
            return(None)
        
        n = len(values)
        
        uarr = np.zeros(n, dtype = "object")
        
        for index, (v, e) in enumerate(zip(values, errors)):
            uarr[index] = ufloat(v, e)
        
        return(uarr)
    
def multimeter_error(value, scale, multimeter_type, measure_type,
                     ignore_gain = False, ignore_digit = False):
    """
    value is the value measured by the multimeter
    scale is the "end of scale" given by the multimeter, 
        or the v/div on the oscilloscope
    multimeter_type is:
        'a' for agilent
        'm' for metrix
        'o' for oscilloscope
    measure_type is:
        'a' for current
        'v' for tension
        'ohm' for resistance
        'c' for capacity
        's' for time
     
    Returns the error of the measure.
    """
    if(multimeter_type == 'a'):
        if(measure_type == 'a'):
            scale_array = np.array([6*10**(-5), 6*10**(-4), 6, 10])
            resolution_array = float(10)**(np.array([-8, -7, -3, -2]))
            percent_accuracy = np.array([1, 1, 1, 1])
            digit_accuracy = np.array([2, 2, 3, 3])
        elif(measure_type == 'v'):
            scale_array = 6 * np.array([10**(-1), 1, 10, 100])
            resolution_array = float(10)**(np.array([-4, -3, -2, -1]))
            percent_accuracy = 0.5 * np.array([1, 1, 1, 1])
            digit_accuracy = 2 * np.array([1, 1, 1, 1])
        elif(measure_type == 'ohm'):
            scale_array = 6 * float(10)**(np.array([2, 3, 4, 5, 6, 7]))
            resolution_array = float(10)**(np.array([2, 3, 4, 5, 6, 7]) - 3)
            percent_accuracy = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 1.5])
            digit_accuracy = 3 * np.array([1, 1, 1, 1, 1, 1])
        else:
            print(f'{measure_type} is not a valid measure type')
            return(None)
    elif(multimeter_type == 'm'):
        if(measure_type == 'v'):
            scale_array = np.array([1, 10, 100, 1000])
            resolution_array = float(10)**(np.array([-5, -4, -3, -2]))
            percent_accuracy = np.array([0.05, 0.03, 0.03, 0.035])
            digit_accuracy = 8 * np.array([1, 1, 1, 1])
        elif(measure_type == 'a'):
            scale_array = float(10)**(np.array([-3, -2, -1, 0, 1]))
            resolution_array = float(10)**(np.array([-3, -2, -1, 0, 1]) - 5)
            percent_accuracy = np.array([0.1, 0.08, 0.08, 0.15, 0.5])
            digit_accuracy = np.array([15, 8, 8, 8, 15])
        elif(measure_type == 'ohm'):
            scale_array = float(10)**(np.array([3, 4, 5, 6, 7, 8]))
            resolution_array = float(10)**(np.array([3, 4, 5, 6, 7, 8]) - 5)
            percent_accuracy = np.array([0.1, 0.07, 0.07, 0.07, 1, 3])
            digit_accuracy = np.array([8, 8, 8, 8, 80, 80])
        elif(measure_type == 'c'):
            scale_array = float(10)**(np.array([-9, -8, -7, -6, -5, -4, -3, -2]))
            resolution_array = float(10)**(np.array([-9, -8, -7, -6, -5, -4, -3, -2]) - 3)
            percent_accuracy = np.array([2.5, 1, 1, 1, 1, 1, 1, 1.5])
            digit_accuracy = np.array([15, 8, 8, 10, 10, 10, 15, 15])
        else:
            print(f'{measure_type} is not a valid measure type')
            return(None)
    elif(multimeter_type == 'o'):
        if(measure_type == 'v'):
            mag_ord = float(10)**(np.arange(-9, 2))
            scale_array = np.concatenate((mag_ord, 2*mag_ord, 5*mag_ord))
            resolution_array = scale_array/10
            percent_accuracy = 0.01 * np.ones(len(scale_array))
            digit_accuracy = np.ones(len(scale_array))
        elif(measure_type == 's'):
            scale_array = float(10)**(np.arange(-9, 2))
            resolution_array = scale_array/10
            percent_accuracy = 3 * np.ones(len(scale_array))
            digit_accuracy = np.ones(len(scale_array))
        else:
            print(f'{measure_type} is not a valid measure type')
            return(None)
    else:
        print(f'{multimeter_type} is not a valid multimeter type')
        return(None)
    
    if(not(len(scale_array) == len(resolution_array)
    == len(percent_accuracy) == len(digit_accuracy))):
        print('Error in hardcoded values')
        return(None)
    
    tolerance = 0.01
    index = -1
    for i in range(len(scale_array)):
        if(np.abs(np.log(scale_array[i]) - np.log(scale)) < tolerance):
            index = i
    if(index == -1):
        print(f'{scale} is an invalid scale')
        return(None)
    
    distribution_factor = 1/np.sqrt(3)
    
    if(ignore_gain==False and ignore_digit==False):
        error = np.sqrt((percent_accuracy[index] * value / 100 )**2
             + (digit_accuracy[index] * resolution_array[index])**2 ) * distribution_factor
    elif(ignore_gain==True and ignore_digit==False):
        error = digit_accuracy[index] * resolution_array[index] * distribution_factor
    elif(ignore_gain==False and ignore_digit==True):
        error = percent_accuracy[index] * value / 100 * distribution_factor
    else:
        print('Cannot ignore both errors')
        return(None)
    
    return(error)

def multimeter_error_array(value, scale, multimeter_type, measure_type, ignore_gain = False, ignore_digit = False):
    """
    Applies multimeter_error to arrays.
    Returns numpy array of ufloats
    """
    if(not(len(value) == len(scale))):
        print("Value and scale arrays must be of the same size")
        return(None)
    
    errors_array = np.zeros(len(value), dtype = object)
    
    for i in range(len(value)):
        error = multimeter_error(value[i], scale[i], multimeter_type, measure_type, ignore_gain)
        entry = ufloat(value[i], error)
        errors_array[i] = entry
        
    return(errors_array)
    
def ufloat_single_value(value, scale, multimeter_type, measure_type, ignore_gain=False):
    return(ufloat(value,
                  float(multimeter_error(value, scale, multimeter_type, measure_type, ignore_gain))))
    
def ufloat_compatibility(xt, yt, printout=False):
    test = (xt, yt)
    arr = []
    for var in test:
        if((str(type(var)) != "<class 'uncertainties.core.Variable'>")
               and (str(type(var)) != "<class 'uncertainties.core.AffineScalarFunc'>")):
            arr.append(ufloat(var, 0))
        else:
            arr.append(var)
    x = arr[0]
    y = arr[1]
    diff = np.abs(x.n - y.n)
    error = (x - y).s
    lam = np.round(diff/error, decimals=1)
    if(printout==True):
        print("$" + "\\" + "lambda=%.1f" % lam + "$")
    return(lam)
    
def uarray_compatibility(x, y):
    if(len(x) != len(y)):
        print("x and y must be of the same size")
        return(None)
        
    n = len(x)
    compatibility = np.zeros(n)
    for i in range(n):
        compatibility[i] = ufloat_compatibility(x[i], y[i])
    return(compatibility)
        
def res_parallel(r1, r2):
    return(r1 * r2 / (r1 + r2))
    
def print_ufloat(x, units = '', error_decimals = 1):
    """
    Prints the first input, which must be a ufloat,
    in a format compatible with the LaTeX package siunitx.
    Output is \SI{x}{units}, with x rounded to the right number of decimal places.
    error_decimals can be set to be larger than 1 if needed
    
    """
    
    if(x<0):
        neg = "-"
        x = -x
    else:
        neg = ""

    order_error = math.floor(log10(x.s * 1.001)) - error_decimals + 1
    #Horrible hack, but it was the easiest way to make sure that errors like 10**n
    #with n integer were rounded correctly
    if(x.n > 10**error_decimals * x.s):
        order_value = math.floor(log10(x.n))
    else:
        order_value = order_error
    precision = -order_error+order_value
    error = round(x.s * 10**(-order_value), precision)
    value = round(x.n * 10**(-order_value), precision)
    string = '$\\' + 'SI{' + neg + '%s +- %s e%s}{' % (value, error, order_value)
    #string = '\\' + 'SI[round-precision = %s]{%s +- %s}{' % (order_error, x.n, x.s)
    if(units is not None):
        string += units
    string += '}$'
    print(string, end='')
    return()

def print_float(x, units = '', low_precision = False):
    """
    Prints the first input, which must be a float,
    in a format compatible with the LaTeX package siunitx.
    Output is \SI{x}{units}, with x not rounded at all.
    
    """
    
    if(x<0):
        neg = "-"
        x = -x
    else:
        neg = ""
    
    if(np.abs(x) > (1e-20)):
        order_value = math.floor(log10(x))
    else:
        print('\\' + 'SI{0}{}', end = '')
        return(None)

    value = x * 10**(-order_value)

    string = '$\\' + 'SI{' + neg
    if(low_precision==False):
        string += '%s e%s}{' % (value, order_value)
    else:
        string += '%.1f e %s}{' % (value, order_value)
    if(units is not None):
        string += units
    string += '}$'
    print(string, end='')
    return()

def print_matrix(M, column_names="", uniform_units = None, low_precision = False):
    row_number = np.shape(M)[1]
    c_string = "c"
    for i in range(row_number - 1):
        c_string += "|c"
    print("\\" + "begin{tabular}{" + c_string + "}")
    print(column_names + " \\\\")
    print("\\" + "hline")
    for row in M:
        for index, item in enumerate(row):
            if(index!=0):
                print(' & ', end='')
            if(str(type(item)) == "<class 'uncertainties.core.Variable'>"
               or str(type(item)) == "<class 'uncertainties.core.AffineScalarFunc'>"):
                print_ufloat(item, units = uniform_units)
            elif(str(type(item)) == "<class 'float'>" or 
                 str(type(item)) == "<class 'int'>" or
                 str(type(item)) == "<class 'numpy.float64'>"):
                print_float(item, units = uniform_units, low_precision=low_precision)
            else:
                print(item, end='')
        print(' \\\\')
    print("\\" + "hline")
    print("\\" + "end{tabular}")

        
def print_ufloat_array(names, variables, units):
    if(len(units) > 1):
        for name, var, unit in zip(names, variables, units):
            print("$" + name + "$ =", end = '')
            print_ufloat(var, units=unit)
            print()
    else:
        for name, var in zip(names, variables):
            print("$" + name + "$ =", end = '')
            print_ufloat(var, units=units)
            print()