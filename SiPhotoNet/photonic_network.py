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
    def __init__(self, weights, wavelengths = [1550e-9], intensities = [1]):
        self.neurons = []
        self.waveguide = []
        for i,row in enumerate(weights):
            self.neurons.append(photoneuron.neuron(row, wavelengths[i]))
            self.waveguide.append({'wavelength': wavelengths[i], 'intensity': intensities[i]})
    
    def advance(self): #TODO
        new_waveguide = copy.deepcopy(self.waveguide)
        for i,neuron in enumerate(self.neurons):
            new_waveguide[i]['intensity'] = neuron.nextState(self.waveguide)
        self.waveguide = new_waveguide
            
    def simulate(self): #TODO
        done = False
        while not done:
            self.advance() # advance state of system
            # do any plotting/maniupulation of the data
            # done = True when done
            break
        return