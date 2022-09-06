# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 19:22:48 2022

@author: ppeng
"""

from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({'font.size': 24})


    
#Read the CSV file that contains the sales data obtained from CTA, one column should be "Year" and the other column should be "Sales"
input = pd.read_csv('DATA PATH')


t = input['Year']
sales = input['Sales'] 


var_incline = [0.1,10]   #Initial guesses for the parameters, can be flexible
def residual_incline(var_incline, t_incline, sales_incline):

    b2 = var_incline[0]
    c2 = var_incline[1]
    
    Logistic_incline = a2/(1+np.exp(-b2*(t_incline-c2)))
    return (Logistic_incline - (sales_incline))



t = t.to_numpy()
sales = sales.to_numpy ()


b = np.where(sales != 0)[0]
t_active = t [b]
sales_active = sales [b]



a2 = 2.2*10**8 ##Setting the maximum, changing this value for fast and growth scenario, initial guess might need to be changed as well


min_index = 10  ##Arbitrary starting index, can be flexible
t_incline = t_active [-min_index:]
factor = 1
t_incline_2 = t_incline - t_incline [0] +1
sales_incline = sales_active [-min_index:]/factor


 
varfinal_incline,success = leastsq(residual_incline, var_incline, args=(t_incline_2, sales_incline), maxfev=100000)

b2 = varfinal_incline[0]
c2 = varfinal_incline[1]


sales_predict = a2/(1+np.exp(-b2*(t_incline_2-c2)))*factor


o = int((2021-t_incline[-1]))  


t_predict_incline  = np.linspace(0, 12+o, num=13+o)
t_predict_incline_2  = t_predict_incline + t_incline_2 [-1]
sales_predict_incline = a2/(1+np.exp(-b2*(t_predict_incline_2-c2)))*factor


plt.plot (t_incline, sales_incline*factor, '.b', label = 'Recorded')
plt.plot (t_predict_incline + t_incline [-1], sales_predict_incline, 'r', label = 'fitted')
plt.plot (t_incline, sales_predict, 'r')
plt.xlim(2015, 2033)
plt.minorticks_on()

plt.xlabel('Year')
plt.ylabel('Number of sales unit')
plt.legend()
 

##After obtaining sales data prediction, combine the recorded historical sales data and predicted future sales data, and feed to the MFA as described in Althaf, S, Babbitt, CW, Chen, R. The evolution of consumer electronic waste in the U.S.. J Ind Ecol. 2021; 25: 693– 706.
