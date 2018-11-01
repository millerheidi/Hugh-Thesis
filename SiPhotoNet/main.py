#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Silicon Photonic Network Simulation
    
    @author: Hugh Morison

"""
import matplotlib.pyplot as plt
import photonic_network as network
import numpy as np

def main():
    W = np.linspace(10,15,3)
    lambs = np.linspace(1500,1520,500) * 1e-9
    T = []
    D = []
    for w in W:
        thrus = []
        drops = []
        for l in lambs:
            system = net.network([[W]], wavelengths = [l])
            thrus.append(system.neurons[0].weightBank(system.waveguide)['thrus'][0])
            drops.append(system.neurons[0].weightBank(system.waveguide)['drops'][0])
        T.append(thrus)
        D.append(drops)
    
    plt.figure()
    for i,t in enumerate(T): 
        line = plt.plot(lambs*1e9, t)
        line[0].set_color('b')
        line[1].set_color('k')
        line[2].set_color('c')

    for i,d in enumerate(D): 
        line = plt.plot(lambs*1e9, d, '--')
        line[0].set_color('b')
        line[1].set_color('k')
        line[2].set_color('c')


    ax1 = plt.gca()
    ax1.legend(['I_h=' + str(w) for w in W])
    
if __name__ == '__main__': main()