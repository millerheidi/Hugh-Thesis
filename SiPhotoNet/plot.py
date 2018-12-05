#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 00:46:43 2018

@author: Hugh
"""
from photonic_network import network
import numpy as np
import matplotlib.pyplot as plt



"""
get modulator spectral response for:
    just bias (no light)
    light in both PDs
    light in each PD
    
    for each of two heater currents
        for each of 4 bias currents
"""
        
heaterCurrent = [0e-3, 0.5e-3]
biasCurrent = [-1e-3,0.0,.5e-3,1.25e-3,2e-3]
wavelengths = np.linspace(1549.0e-9,1553.0e-9,500)
set1 = np.zeros(shape = (5,2,len(wavelengths)))
set2 = np.zeros(shape = (5,2,len(wavelengths)))
set3 = np.zeros(shape = (5,2,len(wavelengths)))

for i,I_h in enumerate(heaterCurrent):
    for j,I_b in enumerate(biasCurrent):
        net = network([[1]])
        for k,w in enumerate(wavelengths):
            Ipd1 = net.neurons[0].photodiode(np.array([[w,0]])[:,1], np.array([[w,0]])[:,1])
            Ipd2 = net.neurons[0].photodiode(np.array([[w,25e-3]])[:,1], np.array([[w,25e-3]])[:,1])
            Ipd3 = net.neurons[0].photodiode(np.array([[w,0]])[:,1], np.array([[w,25e-3]])[:,1])
            net.neurons[0].output_wavelength = w
            set1[j,i,k]=net.neurons[0].modulatorTransmission(Ipd1+I_b, 9.5e-3+I_h)
            set2[j,i,k]=net.neurons[0].modulatorTransmission(Ipd2+I_b, 9.5e-3+I_h)
            set3[j,i,k]=net.neurons[0].modulatorTransmission(Ipd3+I_b, 9.5e-3+I_h)

fig, axes = plt.subplots(5,2)
for i,I_h in enumerate(heaterCurrent):
    for j,I_b in enumerate(biasCurrent):
        axes[j,i].plot(wavelengths*1e9-1551,set1[j,i,:])
        axes[j,i].plot(wavelengths*1e9-1551,set2[j,i,:])
        axes[j,i].plot(wavelengths*1e9-1551,set3[j,i,:])
fig.legend(['No input', 'Two inputs', 'One input'])
fig.show()
