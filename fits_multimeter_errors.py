import numpy as np
import scipy
from scipy import optimize
import matplotlib.pyplot as plt

class dataset:
    def __init__(self, x_array, y_array, x_type, y_type):
        self.x_array = x_array
        self.y_array = y_array
        self.x_type = x_type # 'a' or 'v', for current or tension
        self.y_type = y_type
        self.x_error_array = []
        self.y_error_array = []
    
    def calculate_error(self, scale_array, axis, multimeter_type):
        if (axis=='x'):
            array = self.x_array
            data_type = self.x_type
        elif (axis=='y'):
            array = self.y_array
            data_type = self.y_type
        else:
            print("axis must be x or y")
            return(0)
        
        if (len(scale_array) != len(array)):
            print("scale_array must be have the same length as the data array")
            return(0)
        else:
            n = len(scale_array)
        
        error_array = np.zeros((n))
        
        for i in range(n):
            error_array[i] = multimeter_error(array[i],
                       scale_array[i], multimeter_type, data_type)
            
        if (axis=='x'):
            self.x_error_array = error_array
        elif (axis=='y'):
            self.y_error_array = error_array
        
        return(0)
        
    def model(x, params):
        y = x * params[0] + params[1]
        return(y)
        
    def fit (self, initial_params=False):
        """
        fits the model
        
        returns params, error_params
        """
        
        params, pcov = scipy.optimize.curve_fit(self.model, self.x_array, self.y_array,
                                      sigma=self.y_error_array, absolute_sigma=True)
        
        error_params = []
        for i in range(np.shape(pcov)[0]):
            error_params.append(pcov[i,i])
        
        return(params, error_params)
        
    #def plot (self):
        
        
def multimeter_error(value, scale, multimeter_type, measure_type):
    """
    value is the value measured by the multimeter
    scale is the "end of scale" given by the multimeter
    multimeter_type is 'a' for agilent or 'm' for metrix
    measure_type is:
        'a' for current
        'v' for tension
        'ohm' for resistance
        'c' for capacity
     
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
            return(0)
    elif(multimeter_type == 'm'):
        if(measure_type == 'v'):
            scale_array = np.array([1, 10, 100, 1000])
            resolution_array = float(10)**(np.array([-5, -4, -3, -2]))
            percent_accuracy = np.array([0.05, 0.03, 0.03, 0.035])
            digit_accuracy = 8 * np.array([1, 1, 1, 1])
        if(measure_type == 'a'):
            scale_array = float(10)**(np.array([-3, -2, -1, 0, 1]))
            resolution_array = float(10)**(np.array([-3, -2, -1, 0, 1] - 5))
            percent_accuracy = np.array([0.1, 0.08, 0.08, 0.15, 0.5])
            digit_accuracy = np.array([15, 8, 8, 8, 15])
        if(measure_type == 'ohm'):
            scale_array = float(10)**(np.array([3, 4, 5, 6, 7, 8]))
            resolution_array = float(10)**(np.array([3, 4, 5, 6, 7, 8]) - 5)
            percent_accuracy = np.array([0.1, 0.07, 0.07, 0.07, 1, 3])
            digit_accuracy = np.array([8, 8, 8, 8, 80, 80])
        if(measure_type == 'c'):
            scale_array = float(10)**(np.array([-9, -8, -7, -6, -5, -4, -3, -2]))
            resolution_array = float(10)**(np.array([-9, -8, -7, -6, -5, -4, -3, -2]) - 3)
            percent_accuracy = np.array([2.5, 1, 1, 1, 1, 1, 1, 1.5])
            digit_accuracy = np.array([15, 8, 8, 10, 10, 10, 15, 15])
        else:
            print(f'{measure_type} is not a valid measure type')
            return(0)
    else:
        print(f'{multimeter_type} is not a valid multimeter type')
        return(0)
    
    if(not(len(scale_array) == len(resolution_array)
    == len(percent_accuracy) == len(digit_accuracy))):
        print('Error in hardcoded values')
        return(0)
    
    tolerance = 0.1
    index = -1
    for i in range(len(scale_array)):
        if(np.abs(np.log(scale_array[i]) - np.log(scale)) < tolerance):
            index = i
    if(index == -1):
        print(f'{scale} is an invalid scale')
        return(0)
    
    print(index)
    error = (percent_accuracy[index] * value / 100 
             + digit_accuracy[index] * resolution_array[index])
    
    return(error)
    