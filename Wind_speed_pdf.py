# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 15:52:35 2022

different curves for describing windspeed
can be updated by accounting for hub - height TODO

@author: ellio
"""
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt


def weibull_pdf(v, c, k=2):
    """
    Parameters
    ----------
    v : float
        windspeed value.
    c : float
        scale parameter - proportional to assumed average wind speed.
    k : float, optional
        form parameter between 1-3. 
        1 means very variable winds, 
        3 means constant winds. 
        The default is 2.

    Returns
    -------
    f_w : float
        probability of wind at speed v.
        
    """
    f_w = k/c*(v/c)**(k-1)*math.exp(-(v/c)**k)
    return f_w

def weibull_cum(v, c, k=2):
    F_w = 1 - math.exp(-(v/c)**k)
    return F_w

def rayleigh_pdf(v, v_m):
    """
    Parameters
    ----------
    v : float
        windspeed value.
    v_m : float
        assumed average windspeed.

    Returns
    -------
    f_r : float
        probability of wind at speed v.

    """
    f_r = (math.pi*v)/(2*v_m**2)*math.exp(-math.pi/4*(v/v_m)**2)
    return f_r

def rayleigh_cum(v, v_m):
    F_r = 1 - math.exp(-math.pi/4*(v/v_m)**2)
    return F_r

    
assumed_average_wind = 10
assumed_average_wind_scale_factor = math.sqrt(4/math.pi) * assumed_average_wind
assumed_max_wind = assumed_average_wind * 3
points = 10000 #Number of points
xmin, xmax = 0, assumed_max_wind

xlist = np.linspace(xmin, xmax, points)

windlocations = [[2.0025, 6.8643],
                 [1.7032, 2.2728],
                 [1.82, 8.1],
                 [1.63, 5.5]]
for loc in windlocations:
    kval, assumed_average_wind_scale_factor = loc[0], loc[1]
    ylist = list(map(lambda y: weibull_pdf(y, assumed_average_wind_scale_factor, k=kval), xlist))
    plt.plot(xlist, ylist)
    
plt.xlim(0,30)
plt.ylim(0,0.4)
plt.xlabel('windspeed (m/s)')
plt.ylabel('probability')
plt.title('weibull pdf')
plt.legend(['Jeju Island Islet Gapado', 'Jeju Island Inland Ohdeung', 'West Turkey Coastal', 'West Turkey Inland'])
plt.show()

# ylist = list(map(lambda y: weibull_cum(y, assumed_average_wind_scale_factor, k=2), xlist))
# plt.plot(xlist, ylist)
# plt.xlabel('windspeed (m/s)')
# plt.ylabel('cumalitve probability')
# plt.title('weibull cumulative')
# plt.show()

# ylist = list(map(lambda y: rayleigh_pdf(y, assumed_average_wind), xlist))
# plt.plot(xlist, ylist)
# plt.xlabel('windspeed (m/s)')
# plt.ylabel('probability')
# plt.title('rayleigh pdf')
# plt.show()

# ylist = list(map(lambda y: rayleigh_cum(y, assumed_average_wind), xlist))
# plt.plot(xlist, ylist)
# plt.xlabel('windspeed (m/s)')
# plt.ylabel('cumalitve probability')
# plt.title('rayleigh cumulative')
# plt.show()

#f_v = (pi*v)/(k)





