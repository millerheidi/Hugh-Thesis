#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Class file for neuron with MRR weight bank, and O/E/O transmission    
    
    @author: Hugh Morison

    --- WEIGHT MATRIX CONVENTION ---
    
    adopting the convention that the weight matrix is NxN (fully connected)
         _                    _  _   _
        | w11  w12  w13 .. w1m || w1i |
    W = | w21  ..          w2m || w2i | where  W[n][m] is the weight of the mth
        | ..        ..         || ..  |        MRR in the nth neuron (modulating
        | wn1           .. wnm || wni |        the mth signal from the waveguide)
         -                    -  -   -         and W[n][N+1] weights the input 
                                               signal to the nth waveguide 
         
    the nth neuron in the network modulates the nth output signal

"""
import numpy as np
import copy
 
class neuron:
    """
        Neurons take a list of weights
    """
    def __init__(self, weights, wavelength, mrr_radius = 3e-5 , a = 0.99, r1 = 0.9, r2 = 0.9, output_power = 1.0):
        self.currents = neuron.weightToHeaterCurrent(weights)
        self.output_wavelength = wavelength
        self.output_power = output_power
        
        self.mrr_radius = mrr_radius
        self.a = a
        self.r1 = r1
        self.r2 = r2
    
    def __str__(self):
        return str(self.output_wavelength) + 'm wavelength neuron with weights:' + str(self.weights)
    
    def act(self, incident):
        waveguide = copy.deepcopy(incident)
        tunedWaveguides = self.weightBank(waveguide)
        current = self.photodiode(tunedWaveguides['thrus'], tunedWaveguides['drops'])
        power = self.output_power * self.modulate(current)
        return power    
    
    def weightBank(self, waveguide):
        thrus = []
        drops = []
        for heater in self.currents:
            MRR = self.mrr(weight, waveguide)
            thru *= MRR['thru']
            drop *= MRR['drop']
        thrus.append(thru)
        drops.append(drop)
        return {'thrus': thrus, 'drops': drops} 
    
    def detuneByWavelength(self, wavelength, n_0 = np.sqrt(12), i_mod = 0.0, coeff_mod = 5e2, i_heater = 0.0, coeff = 5e2):
        return (2*np.pi*self.mrr_radius/wavelength) * (n_0 + i_mod*coeff_mod + coeff*i_heater**2) 
    
    def mrr(self, weight, wavelength):
        a = self.a
        r1 = self.r1
        r2 = self.r2
        heater = weight*1.0e-3
        phi = self.detuneByWavelength(wavelength, i_heater=heater)
        numerator_t = (r2*a)**2 - 2*r1*r2*a*np.cos(phi) + r1**2 
        numerator_d = (1-r1**2)*(1-r2**2)*a
        denominator = 1 + (a*r1*r2)**2 - 2*r1*r2*a*np.cos(phi)
        return {'thru': numerator_t/denominator, 'drop': numerator_d/denominator}
  
    def photodiode(self, thru, drop):
        # calculate the current generated by the photodiode configuration
        # NOT IMPLEMENTED YET
        thru_power = sum(thru)
        drop_power = sum(drop)
        current = drop_power - thru_power # this is all random garbage
        return current
    
    def modulate(self, current):
        a = self.a
        r = self.r1
        # modulate the neuron's signal based on the current
        phi = self.detuneByWavelength(self.output_wavelength, i_mod=current)
        numerator = a**2 + r**2 - 2*r*a*np.cos(phi)
        denominator = 1 + (a*r)**2 - 2*r*a*np.cos(phi)
        return numerator/denominator
    
    @staticmethod
    def weightToHeaterCurrent(weights):
        return 1e-3 * weights

