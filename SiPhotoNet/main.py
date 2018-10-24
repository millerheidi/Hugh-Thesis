#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Silicon Photonic Network Simulation
    
    @author: Hugh Morison

"""
import matplotlib.pyplot as plt
import network as net
import numpy as np

def main():
    W = np.linspace(-np.pi,np.pi,100)
    thrus = []
    drops = []
    for weight in W:
        system = net.network([[weight]])
        thrus.append(system.neurons[0].weightBank(system.waveguide)['thrus'])
        drops.append(system.neurons[0].weightBank(system.waveguide)['drops'])
    
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.plot(W, thrus)
    ax2.plot(W, drops)
    
if __name__ == '__main__': main()