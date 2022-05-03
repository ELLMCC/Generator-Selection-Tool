# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:35:06 2022
econimicy bits
more than 1 criteria consider for the selection cost other eng requirements etc.



@author: ellio
"""

import math
import numpy as np
import matplotlib.pyplot as plt
# import matplotx
from shapely.geometry import LineString
from shapely.geos import TopologicalError
from generators import generators
import pandas as pd

class Selector:
    def __init__(self, rotor_radius=1, peak_wind=60, blades_num=3, gear_ratio=1, gustiness=2, air_density=1.225, wind_scale_factor=False):
        #self.mean_wind_speed = mean_wind_speed
        self.rotor_radius = rotor_radius
        #self.lift_drag_ratio = lift_drag_ratio
        self.peak_wind = peak_wind
        self.gustiness = gustiness
        self.blades_num = blades_num
        self.gear_ratio = gear_ratio
        self.air_density = air_density
        self.already_plotted_winds = []
        if wind_scale_factor:
            self.wind_scale_factor = wind_scale_factor
        else:
            #self.wind_scale_factor = math.sqrt(4/math.pi) * mean_wind_speed
            pass
            
        self.optimal_tip_ratio = None
        self.windspeed_optimised = None
    
    def wind_profile(self, test_wind_speed):
        f_w = self.gustiness/self.wind_scale_factor*(test_wind_speed/self.wind_scale_factor)**(self.gustiness-1)*math.exp(-(test_wind_speed/self.wind_scale_factor)**self.gustiness)
        F_w = 1 - math.exp(-(test_wind_speed/self.wind_scale_factor)**self.gustiness)
        return f_w, F_w
    
    def compute_mode_wind(self, pdf, windspeeds):
        mode_wind = windspeeds[np.argmax(pdf)]
        return mode_wind
        
    def make_wind_profile(self):
        windspeeds = np.linspace(0, self.peak_wind, 1000)
        pdf_probabilities = list(map(lambda y: self.wind_profile(y)[0],windspeeds))
        cum_probabilities = list(map(lambda y: self.wind_profile(y)[1],windspeeds))
        plt.figure()
        plt.plot(windspeeds, pdf_probabilities)
        plt.title('pdf windspeeds')
        # plt.show()
        plt.figure()
        plt.plot(windspeeds, cum_probabilities)
        plt.title('cumulative prob windspeeds')
        # plt.show()
        
        self.windspeed_optimised = self.compute_mode_wind(pdf_probabilities, windspeeds)
        return self.windspeed_optimised
    
    
        
    
    def plot_tip_ratio_power_coeff(self):
        #lift_coefficient = C_l
        #drag_coefficient = C_d
        # def power_coeff_by_lift_drag_coeff_ratio(tip_ratio, C_l_on_C_d, B=self.blades_num):
            
        #     C_p_max = 16/27*tip_ratio*(1/(tip_ratio+(1.32+((tip_ratio-8)/20)**2)/B**(2/3)))-0.57*tip_ratio**2/(C_l_on_C_d*(tip_ratio+1/(2*B)))
        #     return C_p_max
        
        def compute_optimal_tip_ratio(tip_ratios, power_factors):
            optimal_tip_ratio = tip_ratios[np.nanargmax(power_factors)]
            #print(np.nanmax(power_factors))
            return optimal_tip_ratio
        
        def new_Cp_from_tip_ratio(tip_ratio): # zero pitch angle
            part1 = (60.04 - 4.69 * tip_ratio) / tip_ratio
            part2 = math.exp((-21 + 0.735 * tip_ratio) / tip_ratio)
            part3 = 0.0068 * tip_ratio / (1 - 0.035 * tip_ratio)
            Cp = part1 * part2 + part3
            if Cp < 0:
                Cp = np.nan
            return Cp
        
    
        
        max_tip_ratio = 20

        points = 1000 #Number of points
        xmin, xmax = 0.0001 , max_tip_ratio
        x_tip_ratios = np.linspace(xmin, xmax, points)
        
        #ylist2 = list(map(lambda y: power_coeff_by_lift_drag_coeff_ratio(y, self.lift_drag_ratio, B=3), x_tip_ratios))
        ylist = list(map(new_Cp_from_tip_ratio, x_tip_ratios))
        plt.figure()
        #plt.plot(x_tip_ratios, ylist2)
        plt.plot(x_tip_ratios, ylist)
        plt.xlabel('tip ratio ()')
        plt.ylabel('power coefficient ()')
        plt.title('power to tip ratio')
        # plt.show()
        
        self.optimal_tip_ratio = compute_optimal_tip_ratio(x_tip_ratios,ylist)
        return self.optimal_tip_ratio
    
    def windspeed_rotation_optimal(self):
        # tip ratio = rotation (rad/s) * radius / windspeed
        # rotation = tip ratio * wind / radius
        def rotation_from_wind(wind):
            return wind * self.optimal_tip_ratio / self.rotor_radius# * (2*math.pi/60)
        xmin = 0
        xmax = 25
        points = 1000
        ylist =   np.linspace(xmin, xmax, points)  
        xlist = list(map(rotation_from_wind, ylist))
        plt.figure()
        plt.plot(xlist, ylist)
        plt.xlabel('rotor rotation (omega)')
        plt.ylabel('windspeed (m/s)')
        plt.title('optimal windspeed at x omega')
        # plt.show()
        
    def plot_torque_rpm_at_speed(self, windspeed_calced, plot=True):
        
        B = self.blades_num
        #C_l_on_C_d = self.lift_drag_ratio
        rho = self.air_density
        
        # def power_coeff_by_lift_drag_coeff_ratio(tip_ratio):
        #     C_p_max = 16/27*tip_ratio*(1/(tip_ratio+(1.32+((tip_ratio-8)/20)**2)/B**(2/3)))-0.57*tip_ratio**2/(C_l_on_C_d*(tip_ratio+1/(2*B)))
        #     return C_p_max
        
        def new_Cp_from_tip_ratio(tip_ratio): # zero pitch angle
            if tip_ratio < 14:
                part1 = (60.04 - 4.69 * tip_ratio) / tip_ratio
                part2 = math.exp((-21 + 0.735 * tip_ratio) / tip_ratio)
                part3 = 0.0068 * tip_ratio / (1 - 0.035 * tip_ratio)
                Cp = part1 * part2 + part3
                if Cp < 0:
                    Cp = np.nan
            else:
                Cp = np.nan
            return Cp
        
        def wind_turbine_torque(omega):
            tip_ratio = self.rotor_radius * omega / windspeed_calced
            #C_p = power_coeff_by_lift_drag_coeff_ratio(tip_ratio)
            C_p = new_Cp_from_tip_ratio(tip_ratio) 
            torque = 0.5 * rho * C_p/omega * windspeed_calced**3 * math.pi * self.rotor_radius
            return torque
        
        omegas = np.linspace(0.0001, 1200.0001, 1200)
        #rpms = [x * (2*math.pi/60) for x in omegas]
        
        torques = list(map(wind_turbine_torque, omegas))
        powers = [a*b for a,b in zip(omegas,torques)]
    
        gear_ratio = self.gear_ratio
        omegas = [x * gear_ratio for x in omegas]
        torques = [x / gear_ratio for x in torques]
        
        if plot:
            if windspeed_calced not in self.already_plotted_winds:
                if 9.9 < windspeed_calced < 10.1:
                    plt.figure(1000)
                    plt.plot(omegas, powers, linestyle='dashed', label=f'{windspeed_calced:.0f}m/s windspeed')
                    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
                    plt.tight_layout()
                    plt.gcf().set_size_inches(10, 6)
                    # plt.xlabel('omegas')
                    # plt.ylabel('power')
                    # plt.title('rotor power omegas')
                    #plt.show()
                    
                    plt.figure(1001)
                    plt.plot(omegas, torques, linestyle='dashed', label=f'{windspeed_calced:.0f}m/s windspeed')
                    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
                    plt.tight_layout()
                    plt.gcf().set_size_inches(10, 6)
                    # plt.xlabel('omegas')
                    # plt.ylabel('torque')
                    # plt.title('torque omegas')
            self.already_plotted_winds.append(windspeed_calced)
        a = np.column_stack((powers, omegas))
        a = a[~np.isnan(a).any(axis=1)]
        if a.shape[0] == 1:
            a = np.concatenate((a, a))
        return LineString(a)#, np.column_stack((powers, omegas))
        #return LineString(np.column_stack((torques, omegas)))
    
def test_gen():
    
    
    points = 1000 #Number of points
    xmin, xmax = 0.001, 1100
    rpms = np.linspace(xmin, xmax, points)
    
    def gen_curve(x):
        y = x**2/700
        return y

    powers = list(map(gen_curve,rpms))
    
    
    omegas = [x * (2*math.pi/60) for x in rpms]
    torques = np.divide(powers,omegas)
    
    
    
    plt.figure(1000)
    plt.plot(omegas, powers, linestyle='dashed')
    plt.xlabel('Radians per second')
    plt.ylabel('Power (W)')
    plt.title('power omegas generator')
    #plt.show()
    
    plt.figure(1001)
    plt.plot(omegas, torques, linestyle='dashed')
    plt.xlabel('omegas')
    plt.ylabel('torque')
    plt.title('torque omegas generator')
    
    return LineString(np.column_stack((powers, omegas)))
    return LineString(np.column_stack((torques, omegas)))
        #plt.show()
        


def hub_height_adjustment(mean_measured, height_measured, hub_height, parameter=0, log=False, power=False):
    if not log or power:
        raise Exception('need method for hub height')
        hub_wind = None
    else:
        if log:
            roughness = parameter
            hub_wind = mean_measured * ((math.log(hub_height / roughness))/(math.log(height_measured / roughness)))
        elif power:
            power_law_exp = parameter
            hub_wind = mean_measured * (hub_height/height_measured)**power_law_exp
    return hub_wind
    
actualwind = hub_height_adjustment(5, 2, 4,parameter=1.1,log=True)



# gear ratio is generator rotations for each rotor rotation
max_wind = 25
points = 1000 #Number of points
xmin, xmax = 0.001, max_wind + 0.001
winds = np.linspace(xmin, xmax, points)
bucket_size = (xmax - xmin) / points

colnams = ['QM_100W','QM_300W','QM_500W','QM_1kW','QM_1.5kW','QM_2kW','FE_1kW_24V','FE_1kW_12V']
results = pd.DataFrame(columns=colnams)

windlocations = [[2.0025, 6.8643],
                 [1.4147, 3.1923],
                 [1.7032, 2.2728],
                 [1.82, 8.1],
                 [1.63, 5.5]]

gear_ratios = [0.5, 0.7, 1, 1.3]

radii = [0.5, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 2, 3]

test_condition_at_index = []
test_scenarios = [[windlocations[0], 1, 1],
                  [windlocations[2], 0.5, 0.7],
                  [windlocations[3], 0.06, 0.7],
                  [windlocations[3], 0.5, 0.7],
                  [windlocations[4], 1, 1]]

test_scenarios = [test_scenarios[4]]
for test in test_scenarios:
    location, gear, radius = test
    k, c = location[0], location[1]
    test1 = Selector(rotor_radius=radius, gear_ratio=gear, peak_wind=max_wind, gustiness=k, wind_scale_factor=c)
    mode_wind = test1.make_wind_profile()
    optimal_tip_ratio = test1.plot_tip_ratio_power_coeff()
    test1.windspeed_rotation_optimal()
    plt.show()
    
    gep_powers = []
    gen_info = pd.DataFrame(columns=['expected_power', 'energy_over_day','energy_over_year','efficiency'])
    #generators = [generators[-1]]
    for generator in generators:
        Line2 = generator
        
        # use power
        energy = 0
        counter = 0
        expected_power = 0
        for wind in winds:
            counter += 1
            probability = test1.wind_profile(wind)[0]
            if counter % 200 == 0:
                Line1 = test1.plot_torque_rpm_at_speed(wind)
            else:
                Line1 = test1.plot_torque_rpm_at_speed(wind, plot=False)
            if Line1.is_valid:
                #print('valid')
                intersection = Line1.intersection(Line2)
                if intersection.type == 'MultiPoint':
                    biggest_value = 0
                    for i in range(len(intersection)):
                        powertest = intersection[0].x
                        if powertest > biggest_value:
                            biggest_value = powertest
                    power = biggest_value
                else:
                    try:
                        power = intersection.x
                        #print(intersection.xy)
                    except AttributeError:
                        power = 0
                expected_power += power * probability * bucket_size
            else:
                pass
                #print('invalid')
        energy_over_year = expected_power/1000 * 8760
        energy_over_day = expected_power/1000 * 24
        
        tot_pow_wind = 0
        for wind in winds:
            probability = test1.wind_profile(wind)[0]
            tot_pow_wind += 0.5 * 1.225 * math.pi * wind ** 3 * probability * bucket_size
        
        total_efficiency = expected_power / tot_pow_wind * 100
        # print(expected_power, 'W')
        # print(energy_over_year, 'kWh for a year')
        # print(energy_over_day, 'kWh for a day')
        # print(tot_pow_wind, 'W power in wind')
        # print(total_efficiency, '% total efficiency')
        # print('\n')
        gep_powers.append(f'{expected_power:.3f}')
        
        temp_df = pd.DataFrame(columns=['expected_power', 'energy_over_day','energy_over_year','efficiency'])
        temp_df['expected_power'] = [expected_power]
        temp_df['energy_over_day']  = [energy_over_day]
        temp_df['energy_over_year'] = [energy_over_year]
        temp_df['efficiency'] = [total_efficiency]
        gen_info = pd.concat([gen_info,temp_df])
        
        
    dframe = pd.DataFrame([gep_powers], columns=colnams)
    results = pd.concat([results, dframe],axis=0)
    print(gep_powers)
    
    
    
    
# for gear in gear_ratios:
#     for radius in radii:
#         for location in windlocations:
#             test_condition_at_index.append([gear, radius, location])

# for gear in gear_ratios:
#     for radius in radii:
#         print('###################')
#         print('gear: ',gear)
#         print('radius: ',radius)
#         for location in windlocations:
#             print('------------------------')
#             k, c = location[0], location[1]
#             test1 = Selector(6, 1, rotor_radius=radius, gear_ratio=gear, peak_wind=max_wind, gustiness=k, wind_scale_factor=c)
#             mode_wind = test1.make_wind_profile()
#             optimal_tip_ratio = test1.plot_tip_ratio_power_coeff()
#             test1.windspeed_rotation_optimal()
#             plt.show()
            
#             gep_powers = []
#             for generator in generators:
#                 Line2 = generator
                
#                 # use power
#                 energy = 0
#                 counter = 0
#                 expected_power = 0
#                 for wind in winds:
#                     counter += 1
#                     probability = test1.wind_profile(wind)[0]
#                     if counter % 50 == 0:
#                         Line1 = test1.plot_torque_rpm_at_speed(wind)
#                     else:
#                         Line1 = test1.plot_torque_rpm_at_speed(wind, plot=False)
#                     if Line1.is_valid:
#                         intersection = Line1.intersection(Line2)
#                         if intersection.type == 'MultiPoint':
#                             biggest_value = 0
#                             for i in range(len(intersection)):
#                                 powertest = intersection[0].x
#                                 if powertest > biggest_value:
#                                     biggest_value = powertest
#                             power = biggest_value
#                         else:
#                             try:
#                                 power = intersection.x
#                             except AttributeError:
#                                 power = 0
#                         expected_power += power * probability * bucket_size
#                 # print(expected_power, 'W')
#                 # energy_over_year = expected_power/1000 * 8760
#                 # print(energy_over_year, 'kWh for a year')
#                 # energy_over_day = expected_power/1000 * 24
#                 # print(energy_over_day, 'kWh for a day')
                
#                 # tot_pow_wind = 0
#                 # for wind in winds:
#                 #     probability = test1.wind_profile(wind)[0]
#                 #     tot_pow_wind += 0.5 * 1.225 * math.pi * wind ** 3 * probability * bucket_size
                
#                 # print(tot_pow_wind, 'W power in wind')
#                 # total_efficiency = expected_power / tot_pow_wind * 100
#                 # print(total_efficiency, '% total efficiency')
#                 # print('\n')
#                 gep_powers.append(f'{expected_power:.3f}')
#             dframe = pd.DataFrame([gep_powers], columns=colnams)
#             results = pd.concat([results, dframe],axis=0)
#             print(gep_powers)
# use torque

# energy = 0
# counter = 0
# for wind in winds:
#     probability = test1.wind_profile(wind)[0]
#     if counter % 50 == 0:
#         #print(probability, wind)
#         Line1 = test1.plot_torque_rpm_at_speed(wind)
#     else:
#         Line1 = test1.plot_torque_rpm_at_speed(wind, plot=False)
#     if Line1.is_valid:
#         # model_gen_1 = model_generator(400)
#         intersection = Line1.intersection(Line2)
#         if intersection.type == 'MultiPoint':
#             biggest_value = 0
#             for i in range(len(intersection)):
#                 torquei = intersection[0].x
#                 omegai = intersection[0].y
#                 powertest = torquei * omegai
#                 if powertest > biggest_value:
#                     biggest_value = powertest
#             power = biggest_value
#         else:
#             try:
#                 torque = intersection.x
#             except AttributeError:
#                 torque = 0
#             try:
#                 omega = intersection.y
#             except AttributeError:
#                 omega = 0
#             # omega = rpm/60 * 2 * math.pi
#             power = omega * torque
#         #print(power)
#         energy += power * bucket_size * probability
#     counter += 1
    
# plt.show()
    
# print(energy,' Watts')
# energy_over_year = energy/1000 * 8760
# print(energy_over_year, ' kilo Watts')


        
        
        
        
        
        
            