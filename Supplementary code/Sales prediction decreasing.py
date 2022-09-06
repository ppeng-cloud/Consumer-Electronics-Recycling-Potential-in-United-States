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
from matplotlib.ticker import MultipleLocator

plt.rcParams.update({'font.size': 24})


#Read the CSV file that contains the sales data obtained from CTA, one column should be "Year" and the other column should be "Sales"
input = pd.read_csv('DATA PATH')


t = input['Year']
sales = input['Sales'] 


var_decline = [1000,1,1]   #Initial guesses for the parameters, can be flexible
def residual_decline(var_decline, t_decline, sales_decline):
    a2 = var_decline[0]
    b2 = var_decline[1]
    c2 = var_decline[2]
    
    Logistic_decline = a2/(1+np.exp(b2*(t_decline-c2)))
    return (Logistic_decline - (sales_decline))


t = t.to_numpy()
sales = sales.to_numpy ()

b = np.where(sales != 0)[0]
t_active = t [b]
sales_active = sales [b]
max_index = np.argmax(sales_active)


t_decline = t_active [max_index:]

factor = 10**6  

t_decline_2 = t_decline - t_decline [0]
sales_decline = sales_active [max_index:]/factor

 
varfinal_decline,success = leastsq(residual_decline, var_decline, args=(t_decline_2, sales_decline), maxfev=8000)

a2 = varfinal_decline[0]
b2 = varfinal_decline[1]
c2 = varfinal_decline[2]

sales_predict = a2/(1+np.exp(b2*(t_decline_2-c2))) *factor


o = int((2021-t_decline[-1]))  

t_predict_decline  = np.linspace(0, 12+o, num=13+o)
t_predict_decline_2  = t_predict_decline + t_decline_2 [-1]
sales_predict_decline = a2/(1+np.exp(b2*(t_predict_decline_2-c2)))*factor  


plt.figure (1)
plt.plot (t_decline, sales_decline*factor, '.b', label = 'Recorded')
plt.plot (t_predict_decline + t_decline [-1], sales_predict_decline, 'r', label = 'fitted')
plt.plot (t_decline, sales_predict, 'r')
plt.minorticks_on()

plt.xlabel('Year')
plt.ylabel('Number of sales unit')
plt.legend()


##After obtaining sales data prediction, combine the recorded historical sales data and predicted future sales data, and feed to the MFA as described in Althaf, S, Babbitt, CW, Chen, R. The evolution of consumer electronic waste in the U.S.. J Ind Ecol. 2021; 25: 693– 706.

