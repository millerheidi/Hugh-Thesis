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
    def __init__(self, weights, wavelength, mrr_radius = 3e-5 , a = 0.99, r1 = 0.9, r2 = 0.9):
        self.output_wavelength = wavelength
        self.weights = weights
        self.mrr_radius = mrr_radius
        self.a = a
        self.r1 = r1
        self.r2 = r2
    
    def __str__(self):
        return 'Photoneuron instance. Channel: ' + str(self.output_wavelength) + ' Weights:' + str(self.weights)
    
    def act(self, incident):
        incidentWaveguide = copy.deepcopy(incident)
        thru, drop = self.weightBankTransmission(incidentWaveguide[:,0])
        current = self.photodiode(incidentWaveguide[:,1]*thru, incidentWaveguide[:,1]*drop)
        transmission = self.modulatorTransmission(current)
        return transmission    
    
    def weightBankTransmission(self, wavelengths):
        thru = 1.0
        drop = 1.0
        for weight in self.weights:
            MRR = self.mrr(weight, wavelengths)
            thru *= MRR[:,0]
            drop *= MRR[:,1]    
        return thru, drop
    
    def detuneByWavelength(self, wavelength, n_0 = np.sqrt(12), i_mod = 0.0, coeff_mod = 5e2, i_heater = 0.0, coeff = 5e2):
        return (2*np.pi*self.mrr_radius/wavelength) * (n_0 + i_mod*coeff_mod + coeff*i_heater**2) 
    
    def mrr(self, weight, wavelengths):
        a = self.a
        r1 = self.r1
        r2 = self.r2
        heater = self.weightToHeaterCurrent(weight)
        phis = self.detuneByWavelength(wavelengths, i_heater=heater)
        numerator_t = (r2*a)**2 - 2*r1*r2*a*np.cos(phis) + r1**2 
        numerator_d = (1-r1**2)*(1-r2**2)*a
        denominator = 1 + (a*r1*r2)**2 - 2*r1*r2*a*np.cos(phis)
        return np.array([numerator_t/denominator, numerator_d/denominator]).transpose()
    
    def photodiode(self, thru, drop):
        # calculate the current generated by the photodiode configuration
        responsivity = 1 #need real val
        current_bias = 0.0
        current_thru = sum(responsivity*thru)
        current_drop = sum(responsivity*drop)
        return current_thru - current_bias - current_drop
    
    def modulatorTransmission(self, current):
        a = self.a
        r = self.r1
        phi = self.detuneByWavelength(self.output_wavelength, i_mod=current)
        numerator = a**2 + r**2 - 2*r*a*np.cos(phi)
        denominator = 1 + (a*r)**2 - 2*r*a*np.cos(phi)
        return numerator/denominator
    
    def weightToHeaterCurrent(self, weight):
        return weight*1e-3 # this isn't correct
    
    def plotWeightBank(self):
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        fig, ax = plt.subplots()
        weight = 1.0
        
        lambdas = np.linspace(1500e-9,1525e-9,500)
        plt.figure()
        plt.plot(lambdas*1e9, self.mrr(weight, lambdas)[:,0])
        for i in range(50):
            yield
            plt.figure()
            plt.plot(lambdas*1e9, self.mrr(weight+(i/2.0), lambdas)[:,0])  # update the data.
            plt.show()
            
#        legend = []
#        for w in self.weights:
#            legend.append('Pass:' + str(w))
#            legend.append('Drop:' + str(w))
#        plt.legend(legend)
        