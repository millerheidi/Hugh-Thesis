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
from photonic_neuron import neuron
import numpy as np
import copy

class network:
    """
        A network instance has a list of neurons, and a waveguide (a list
        of signals). Need to provide a square matrix of weights to the network.
        
        An input signal can also be provided to the simulation, but the 
        wavelength of the signal needs to be provided as well as the input 
        weights.
        
    """
    def __init__(self, weights, wavelengths = [1550e-9], powers = [1.], weightsIn = [], wavelengthIn = None, signalIn = []):
        self.N = len(weights) # number of neurons (network size)
        self.external = len(weightsIn) > 0 # external input to network (no dedicated neuron)
        for i,weight in enumerate(weightsIn): weights[i].append(weight)
        
        wavelengths = [wavelengths[0] + i*1e-9 for i in range(self.N)] # spectral spacing of signal
        powers = [powers[0] for i in range(self.N)] # inital power of pumps
        
        self.neurons = [neuron(weights[i], wavelengths[i]) for i in range(self.N)]
        waveguide = [[wavelengths[i], powers[i]] for i in range(self.N)]
        
        if self.external:
            waveguide.append([wavelengthIn, signalIn.pop(0)])
            self.signalIn = signalIn
        self.waveguide = np.array(waveguide) # waveguide[wavelength, power]
        self.testConstraints()
    
    """
        Generator will yield new values infinitely* (bounded by the calling 
        loop) or over the length of the input signal if there is one
        
        Future note: maybe account for input signal going infinitely according 
        to periodic function e.g. always is sin() f'n
    """
    def simulate(self): 
        done = False
        while not done:
            yield
            split_waveguide = copy.deepcopy(self.waveguide)
            split_waveguide[:,1] /= self.N
            for i,node in enumerate(self.neurons):
                self.waveguide[i,1] *= node.act(split_waveguide)
            if self.external: 
                self.waveguide[self.N,1] = self.signalIn.pop(0)
                if len(self.signalIn) == 0:
                    done = True
        yield
    
    """
        This function uses assert to ensure initialization worked properly
    """
    def testConstraints(self):
        assert(len(self.neurons) == self.N) # network rank is number of neurons
        if self.external: # waveguide has N signals (+1 external signal)
            assert(len(self.waveguide) == self.N + 1) 
        else:
            assert(len(self.waveguide) == self.N)
            