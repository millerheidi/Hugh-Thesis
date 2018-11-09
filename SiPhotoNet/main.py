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
    net = network.network([[5,-1,0.05],[-1,5,0.05]])
    print(net.N)
    print(net.waveguide)
    for neuron in net.neurons:
        print(neuron)
if __name__ == '__main__': main()