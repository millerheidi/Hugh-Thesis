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
    sys = network([[5,-1,0.05],[-1,5,0.05]])
    print(sys.N)
    print(sys.waveguide)
    for neuron in sys.neurons:
        print(neuron)
if __name__ == '__main__': main()