#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Silicon Photonic Network Simulation
    
    @author: Hugh Morison

"""
import matplotlib.pyplot as plt
import photonic_network as net
import numpy as np

def main():
    N = 1e8
    W = np.linspace(-N,N,100000)

    thrus = []
    drops = []
    for weight in W:
        system = net.network([[weight]])
        thrus.append(system.neurons[0].weightBank(system.waveguide)['thrus'][0])
        drops.append(system.neurons[0].weightBank(system.waveguide)['drops'][0])
    
    plt.figure()
    plt.plot(W, thrus)
    plt.figure()
    plt.plot(W, drops)
    
if __name__ == '__main__': main()