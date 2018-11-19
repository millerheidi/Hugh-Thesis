#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Class file for network simulator.
    
    @author: Hugh Morison
    
    --- SIMULATION STRUCTURE ---
    
    Waveguide structure will contain different lights from laser pumps, which 
    each have wavelengths and power.
    
    Collection of neurons in the network will be initialized with a weight bank
    and a list of wavelengths each neuron modulates.
    
    
    Simulation is started specifying weight matrices, output wavelengths, and
    inital pump powers. Optionally, add a list of input weights, an input 
    wavelength, and the time varying input signal (this will limit the 
    duration of the simulation)
    After initializing the network, call instance.simulate() to obatin the
    generator. With no input signal defined, the generator will generate new 
    network states infinitely. 
    
    TODO:
        - Add network state accessors.

    
    --- WEIGHT MATRIX CONVENTION ---
    
    Adopting the convention that the weight matrix is NxN (fully connected)
    with an extra column of weights when the network has external input.
         _                    _  _   _
        | w11  w12  w13 .. w1m || w1i |
    W = | w21  ..          w2m || w2i | where  W[n][m] is the weight of the mth
        | ..        ..         || ..  |        MRR in the nth neuron (modulating
        | wn1           .. wnm || wni |        the mth signal from the waveguide)
         -                    -  -   -         and W[n][N+1] weights the input 
                                               signal to the nth waveguide 
         
    the nth neuron in the network modulates the nth output signal

"""
from photonic_neuron import neuron
import numpy as np
import copy

class network:

    def __init__(self, weights, wavelengths = [1551.1e-9], powers = [25e-3], weightsIn = [], wavelengthIn = None, signalIn = []):
        """
            A network instance has a list of neurons, and a waveguide (a list
            of signals). Need to provide a square matrix of weights to the network.
            
            An input signal can also be provided to the simulation, but the 
            wavelength of the signal needs to be provided as well as the input 
            weights.
            
        """
        
        self.N = len(weights) # number of neurons (network size)
        self.external = len(weightsIn) > 0 # external input to network (no dedicated neuron)
        for i,weight in enumerate(weightsIn): weights[i].append(weight)
        
        wavelengths = [wavelengths[0] + 2*i*1e-9 for i in range(self.N)] # spectral spacing of signal
        self.powers = [powers[0] for i in range(self.N)] # inital power of pumps
        
        self.neurons = [neuron(weights[i], wavelengths[i]) for i in range(self.N)]
        waveguide = [[wavelengths[i], self.powers[i]] for i in range(self.N)]
        
        if self.external:
            waveguide.append([wavelengthIn, signalIn.pop(0)])
            self.signalIn = signalIn
        self.waveguide = np.array(waveguide) # waveguide[wavelength, power]
        self.testConstraints()
        
    
    
    def getState(self, i):
        """
            Get state of ith waveguide signal.
        """
        assert(i > 0 and i <= self.N +1)
        return self.waveguide[i-1,1]
    
    def simulate(self): 
        """
            Generator will yield new values infinitely* (bounded by the calling 
            loop) or over the length of the input signal if there is one
            
            Future note: maybe account for input signal going infinitely according 
            to periodic function e.g. always is sin() f'n
            
        """
        done = False
        while not done:
            yield
            split_waveguide = copy.deepcopy(self.waveguide)
            split_waveguide[:,1] /= self.N
            for i,node in enumerate(self.neurons):
                self.waveguide[i,1] = self.powers[i] * node.act(split_waveguide)
            
            if self.external: 
                self.waveguide[self.N,1] = self.signalIn.pop(0)
                if len(self.signalIn) == 0:
                    done = True
            
        yield
    

    def testConstraints(self):
        """
            This function uses assert to ensure initialization worked properly
        """
        assert(len(self.neurons) == self.N) # network rank is number of neurons
        if self.external: # waveguide has N signals (+1 external signal)
            assert(len(self.waveguide) == self.N + 1) 
        else:
            assert(len(self.waveguide) == self.N)
            