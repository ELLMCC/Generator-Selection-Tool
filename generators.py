# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 15:40:42 2022

@author: ellio
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString

def QM_100W():
    
    points = 1000 #Number of points
    xmin, xmax = 0.01, 350.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = x ** 2 / 1225
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='QM 100W')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
    
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='QM 100W')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))

def QM_500W(): #http://www.qm-magnets.com/product_Generator_0.3.htm
    points = 1000 #Number of points
    xmin, xmax = 0.01, 210.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = x ** 2 * 1 / 80
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='QM 500W')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
        
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='QM 500W')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))

def QM_300W(): #http://www.qm-magnets.com/product_Generator_0.3.htm
    points = 1000 #Number of points
    xmin, xmax = 0.01, 900.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = x ** 2 * 3 / 7225
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='QM 300W')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
        
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='QM 300W')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))


def FE_1kW_24V():
    points = 1000 #Number of points
    xmin, xmax = 0.01, 975.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = (x - 100) ** 2 * 19 / 5625
        if x < 100:
            y = 0
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='FE 1kW 24V')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
        
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='FE 1kW 24V')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))

def FE_1kW_12V():
    points = 1000 #Number of points
    xmin, xmax = 0.01, 1180.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = (x - 100) ** 2 * 1 / 540
        if x < 100:
            y = 0
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='FE 1kW 12V')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
        
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='FE 1kW 12V')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))

def EE_1_300_1kW():
    #NOT USED 
    pass
    # points = 1000 #Number of points
    # xmin, xmax = 0.01, 300.01
    # xlist = np.linspace(xmin, xmax, points)
    
    # def approximate_curve(x):
    #     y = x * 10 / 3
    #     if x < 60:
    #         y = np.nan
    #     return y
    # ylist = list(map(approximate_curve, xlist))
    
    
    # omegas = [x * (2*math.pi/60) for x in xlist]
    # # torques = np.divide(powers,omegas)
    # plt.figure(1000)
    # plt.plot(omegas, ylist)
    # #plt.plot(xlist, ylist)
    # plt.xlabel('Radians per Second')
    # plt.ylabel('Power (W)')
    # plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
    # colstack = np.column_stack((ylist, omegas))
    # no_nan_colstack = colstack[~np.isnan(colstack).any(axis=1)]
    
        
    # plt.figure(1001)
    # torques = np.divide(ylist,omegas)
    # plt.plot(omegas, torques)
    # #plt.plot(xlist, ylist)
    # plt.xlabel('Radians per Second')
    # plt.ylabel('Torque (Nm)')
    # plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
    
    
    return LineString(no_nan_colstack)

def QM_1kW():
    points = 1000 #Number of points
    xmin, xmax = 0.01, 210.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = x ** 2 * 3 / 100
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='QM 1kW')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
        
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='QM 1kW')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))

def QM_1500W():
    points = 1000 #Number of points
    xmin, xmax = 0.01, 105.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = x ** 2 * 3 / 20
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='QM 1.5kW')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
        
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='QM 1.5kW')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))

def QM_2kW():
    points = 1000 #Number of points
    xmin, xmax = 0.01, 190.01
    xlist = np.linspace(xmin, xmax, points)
    
    def approximate_curve(x):
        y = x ** 2 * 5 / 81
        return y
    ylist = list(map(approximate_curve, xlist))
    
    
    omegas = [x * (2*math.pi/60) for x in xlist]
    # torques = np.divide(powers,omegas)
    plt.figure(1000)
    plt.plot(omegas, ylist, label='QM 2kW')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Power (W)')
    plt.title('Wind turbine power curves at different windspeeds \nand the generator power curves, against rotational speed')
        
    plt.figure(1001)
    torques = np.divide(ylist,omegas)
    plt.plot(omegas, torques, label='QM 2kW')
    #plt.plot(xlist, ylist)
    plt.xlabel('Radians per Second')
    plt.ylabel('Torque (Nm)')
    plt.title('Wind turbine torque curves at different windspeeds \nand the generator torque curves, against rotational speed')
    
    return LineString(np.column_stack((ylist, omegas)))
generators = [FE_1kW_12V()]
# generators = [QM_100W(),
#               QM_300W(),
#               QM_500W(),
#               QM_1kW(),
#               QM_1500W(),
#               QM_2kW(),
#               FE_1kW_24V(),
#               FE_1kW_12V()]
#plt.legend(['QM_100W','QM_300W','QM_500W','QM_1kW','QM_1.5kW','QM_2kW','FE_1kW_24V','FE_1kW_12V'])
#plt.show()




