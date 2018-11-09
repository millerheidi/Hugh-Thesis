#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Class file for network 
    
    @author: Hugh Morison
    
    --- SIMULATION STRUCTURE ---
    
    Waveguide structure will contain different lights
    Lights will have wavelengths and intensity/power
    Network has a waveguide and a list of neurons
    Each neuron has a bank of MRRs 
    Number of resonators in a neuron = Number of wavelengths in waveguide = Number of neurons in network
    
    
    Simulation is started specifying number of neurons and weight matrices
    Instanstiate waveguide, add number of signals with 0 power initially
    Instantitate list of neurons, each neuron with N tuning params

"""
import photonic_neuron as photoneuron
import numpy as np
import copy

class network:
    """
        A network instance has a list of neurons, and a waveguide (a list
        of signals). Need to provide a square matrix of weights to the network.
    """
    def __init__(self, weights, wavelengths = [1550e-9], powers = [1]):
        self.N = len(weights)
        wavelengths = [wavelengths[0] + i*50e-9 for i in range(self.N)] # define wavelength spacing (FSR dependant)
        powers = [1 for i in range(self.N)] # inital power is 1, investigate laser pump specs
        self.neurons = [photoneuron.neuron(weights[i], wavelengths[i], output_power = powers[i]) for i in range(self.N)]
        self.waveguide = np.array([[wavelengths[i], powers[i]] for i in range(self.N)]) # waveguide[wavelength, power]
    
         
    def simulate(self, input_signal = None): # generator will yield new values infinitely*
        while True:
            split_waveguide = copy.deepcopy(self.waveguide)
            split_waveguide[:,1]/self.N
            for i,neuron in enumerate(self.neurons):
                self.waveguide[i,1] = neuron.act(split_waveguide)
            yield
            