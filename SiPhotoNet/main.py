#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Silicon Photonic Network Simulation
    
    @author: Hugh Morison

"""
import matplotlib.pyplot as plt
from photonic_network import network
import numpy as np

def main():
    sys = network([[0]])
    i = np.linspace(0,5e-3,50000)
    o = sys.neurons[0].modulatorTransmission(i)
    plt.plot(i,o)
    sys.neurons[0].plotWeightBank()




if __name__ == '__main__': main()