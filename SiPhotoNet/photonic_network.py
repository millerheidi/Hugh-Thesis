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
import copy

class network:
    def __init__(self, weights, wavelengths = [1550e-9], powers = [1]):
        self.N = len(wavelengths)
        self.neurons = []
        self.waveguide = []
        for i,weightbank in enumerate(weights):
            self.neurons.append(photoneuron.neuron(weightbank, wavelengths[i], output_power = powers[i]))
            self.waveguide.append({'wavelength': wavelengths[i], 'power': powers[i]})
    
    def advance(self):
        split_waveguide = copy.deepcopy(self.waveguide)
        for signal in split_waveguide:
            signal['power'] = signal['power']/self.N
        for i,neuron in enumerate(self.neurons):
            self.waveguide[i]['power'] = neuron.act(split_waveguide)
         
    def simulate(self, input_signal = None): # generator will yield new values infinitely*
        while True:
            self.advance() 
            yield
            