# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 14:48:32 2022

@author: ellio
"""

import matplotlib.pyplot as plt
import numpy as np
import math

points = 1000 #Number of points
xmin, xmax = 0, 975
rpms = np.linspace(xmin, xmax, points)

def gen_curve(x):
    y = x**2/400
    return y

powers = list(map(gen_curve,rpms))

omegas = [x / (2*math.pi/60) for x in rpms]

torques = np.divide(powers,omegas)

plt.plot(rpms, powers)
plt.xlabel('rpm')
plt.ylabel('power')
plt.show()

plt.plot(rpms, torques)
plt.xlabel('rpm')
plt.ylabel('torque')
plt.show()
             