# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 16:42:02 2022

@author: ellio
"""

import matplotlib.pyplot as plt
import numpy as np
import statistics
import math



max_tip_ratio = 20 # accurate between 4-20

points = 1000 #Number of points
xmin, xmax = 0, max_tip_ratio
x_tip_ratios = np.linspace(xmin, xmax, points)

rotor_radius = 2
air_density = 1.225
rotor_area = math.pi * rotor_radius**2
cubic_mean_windspeed = 5
rotor_power_coefficient = 0.4


def model_turbine_w_gen(BWEA_ref_power, BWEA_ref_speed, cut_in_speed, rated_power, survival_cutoff):
    x = [0, cut_in_speed, BWEA_ref_speed, survival_cutoff]
    y = [0, 0, BWEA_ref_power, rated_power]
    plt.plot(x,y)

def power_coeff_by_lift_drag_coeff_ratio(tip_ratio, C_l_on_C_d, B=3):
    C_p_max = 16/27*tip_ratio*(1/(tip_ratio+(1.32+((tip_ratio-8)/20)**2)/B**(2/3)))-0.57*tip_ratio**2/(C_l_on_C_d*(tip_ratio+1/(2*B)))
    return C_p_max

def model_mech_rotor_pow(rho, A, U, C_p):
    wind_power = 0.5 * rho * U**3
    mech_power = wind_power * C_p * A
    return mech_power, wind_power

def compute_optimal_tip_ratio(tip_ratios, power_factors):
    optimal_tip_ratio = tip_ratios[np.argmax(power_factors)]
    return optimal_tip_ratio

def windspeed_rotation_optimal(rotor_radius, optimal_tip_ratio):
    # tip ratio = rotation (rad/s) * radius / windspeed
    def rotation_from_wind(wind):
        return wind*optimal_tip_ratio/rotor_radius * (2*math.pi/60)
    xmin = 0
    xmax = 60
    points = 1000
    ylist =   np.linspace(xmin, xmax, points)  
    xlist = list(map(rotation_from_wind, ylist))
    plt.plot(xlist, ylist)
    plt.xlabel('rotor rotation (rpm)')
    plt.ylabel('windspeed (m/s)')
    plt.show()

def plot_torque_rpm_at_speed(windspeed, radius, rho, C_l_on_C_d, B=3):
    def wind_turbine_torque(omega):
        tip_ratio = radius * omega / windspeed
        C_p = power_coeff_by_lift_drag_coeff_ratio(tip_ratio, C_l_on_C_d, B=3) 
        torque = 0.5 * rho * C_p/omega * windspeed**3 * math.pi * radius
        return torque
    omegas = np.linspace(0.001, 120, 1000)
    rpms = [x * (2*math.pi/60) for x in omegas]
    torques = list(map(wind_turbine_torque, omegas))
    powers = [a*b for a,b in zip(omegas,torques)]
    plt.plot(rpms, powers)
    plt.xlabel('rpm')
    plt.ylabel('power')
    plt.show()
    
    plt.plot(rpms, torques)
    plt.xlabel('rpm')
    plt.ylabel('torque')
    plt.show()
    
# model_turbine_w_gen(4711, 11, 3, 5000, 60)

def plot_tip_ratio_power_coeff():
#lift_coefficient = C_l
#drag_coefficient = C_d

    lift_drag_ratios = [25]
    #lift_drag_ratios = [25]
    
    for ratio in lift_drag_ratios:
        C_l_on_C_d = ratio
        
        ylist = list(map(lambda y: power_coeff_by_lift_drag_coeff_ratio(y, C_l_on_C_d, B=3), x_tip_ratios))
        plt.plot(x_tip_ratios, ylist)
        plt.xlabel('tip ratio ()')
        plt.ylabel('power coefficient ()')
    plt.show()
    return ylist

y_power_coeffs = plot_tip_ratio_power_coeff()

optimal_tip_ratio = compute_optimal_tip_ratio(x_tip_ratios, y_power_coeffs)
windspeed_rotation_optimal(rotor_radius, optimal_tip_ratio)

plot_torque_rpm_at_speed(5, 2, 1.225, 25)

modelled_mech_power, modelled_wind_power = model_mech_rotor_pow(air_density, rotor_area, cubic_mean_windspeed, rotor_power_coefficient)


