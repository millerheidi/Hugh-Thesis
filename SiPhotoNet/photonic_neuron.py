#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Class file for neuron with MRR weight bank, and O/E/O transmission    
    
    @author: Hugh Morison

    --- WEIGHT MATRIX CONVENTION ---
    
    adopting the convention that the weight matrix is NxN (fully connected)
         _                    _
        | w11  w12  w13 .. w1m |
    W = | w21  ..          w2m |   where  W[n][m] is the weight of the mth
        | ..        ..         |          MRR in the nth neuron (modulating
        | wn1           .. wnm |          the mth signal from the waveguide)
         -                    -
         
    the nth neuron in the network modulates the nth output signal

"""
import numpy as np
 
class neuron:
    def __init__(self, weights, wavelength):
        self.L = 3e-5 # copy heidis length
        self.n = weights # function of weight value (maybe current supplied to heater)
        self.a = 0.9
        self.r1 = 0.85
        self.r2 = 0.85
        self.output_wavelength = wavelength
    
    def nextState(self, waveguide):
        tunedWaveguides = self.weightBank(waveguide)
        current = self.photodiode(tunedWaveguides['thru'], tunedWaveguides['drop'])
        intensity = self.modulate(current)
        return intensity
    
    def weightBank(self, waveguide):
        thrus = []
        drops = []
        for i,signal in enumerate(waveguide):
            mr = self.mrr(i, signal['wavelength'])
            thrus.append(signal['intensity'] * mr['thru'])
            drops.append(signal['intensity'] * mr['drop'])
        return {'thrus': thrus, 'drops': drops}
    
    def mrr(self, i, wavelength):
        # calculate phi from weight and wavelength
        k = 2 * np.pi * wavelength
        phi = self.n[i] * self.L * k
        numerator_t = (self.r2*self.a)**2 + self.r1**2 - 2*self.r1*self.r2*self.a*np.cos(phi)
        numerator_d = (1-self.r1**2)*(1-self.r2**2)*self.a
        denominator = 1 + (self.a*self.r1*self.r2)**2 - 2*self.r1*self.r2*self.a*np.cos(phi)
        return {'thru': numerator_t/denominator, 'drop': numerator_d/denominator}
    
    def photodiode(self, thru, drop):
        # calculate the current generated by the photodiode configuration
        # NOT IMPLEMENTED YET
        return -1
    
    def modulate(self, current):
        # modulate the neuron's signal based on the current
        # NOT IMPLEMENTED YET
        return -1