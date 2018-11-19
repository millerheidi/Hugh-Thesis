#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Class file for neuron with MRR weight bank, and O/E/O transmission    
    
    @author: Hugh Morison

"""
import numpy as np
import copy
import matplotlib.pyplot as plt

class neuron:

    def __init__(self, weights, wavelength, net_wavelengths = [], mrr_radius = 6e-5, a = 1, r1 = 0.92, r2 = 0.92):
        """
            Neuron takes a list of weights and an output wavelength.
            
            The radius of the ring (mrr_radius), the loss in the ring (a), and the
            self-coupling coefficients (r1 and r2) can be changed.
        """
        self.output_wavelength = wavelength
        self.weights = self.weightToHeaterCurrent(weights, net_wavelengths)
        self.mrr_radius = mrr_radius
        self.a = a
        self.r1 = r1
        self.r2 = r2
    
    def __str__(self):
        """
            Neuron string representation.
        """
        return 'Photoneuron instance. Channel: ' + str(self.output_wavelength) + ' Weights:' + str(self.weights)
    
    def act(self, incident):
        """
            Apply neuron transfer function to incident waveguide and return the 
            modulator transmission.
        """
        incidentWaveguide = copy.deepcopy(incident)
        thru, drop = self.weightBankTransmission(incidentWaveguide[:,0])
        current = self.photodiode(incidentWaveguide[:,1]*thru, incidentWaveguide[:,1]*drop)
        transmission = self.modulatorTransmission(current)
        return transmission    
    
    def weightBankTransmission(self, wavelengths):
        """
            Get through and drop port transmissions for each incident wavelength.
        """
        thru = 1.0
        drop = 1.0
        for current in self.weights:
            MRR = self.mrr(current, wavelengths)
            drop = thru * MRR[:,1]
            thru *= MRR[:,0]
                
        return thru, drop
    
    def detuneByWavelength(self, wavelength, n_0 = np.sqrt(12), i_mod = 0.0, coeff_mod = 5e2, i_heater = 0.0, coeff = 5e2):
        """
            Get phase shift induced by MRR w/ thermo-optic effect (weight bank) or 
            electro-optic efffect (modulator).
        """
        return (2*np.pi*self.mrr_radius/wavelength) * (n_0 + i_mod*coeff_mod + coeff*i_heater**2) 
    
    def mrr(self, heater, wavelengths):
        """
        """
        a = self.a
        r1 = self.r1
        r2 = self.r2
        phis = self.detuneByWavelength(wavelengths, i_heater=heater) # [rad]
        numerator_t = (r2*a)**2 - 2*r1*r2*a*np.cos(phis) + r1**2 
        numerator_d = (1-r1**2)*(1-r2**2)*a
        denominator = 1 + (a*r1*r2)**2 - 2*r1*r2*a*np.cos(phis)
        return np.array([numerator_t/denominator, numerator_d/denominator]).transpose()
    
    def photodiode(self, p_thru, p_drop):
        """
            Calculate the current generated by the photodiode configuration.
        """
        wavelength = 1550e-9 # [m] could add wavelength dependance
        eta = 0.75 # [%] complete guess
        responsivity = eta * (wavelength / (1.23985e-6)) # [A/W]
        current_bias = 0.0 # [A]
        current_thru = sum(responsivity*p_thru) # [A]
        current_drop = sum(responsivity*p_drop) # [A]
        return - current_thru + current_bias + current_drop # [A]
    
    def modulatorTransmission(self, current):
        """
        """
        a = self.a
        r = self.r1
        phi = self.detuneByWavelength(self.output_wavelength, i_mod=current)
        numerator = a**2 + r**2 - 2*r*a*np.cos(phi)
        denominator = 1 + (a*r)**2 - 2*r*a*np.cos(phi)
        return numerator/denominator
    
    def weightToHeaterCurrent(self, weights, wavelengths):
        """
        """
        wavelengths = np.array(wavelengths)
        weights = np.array(weights)
        
        return weights*1e-3 # [A]
    
    def plotWeightBank(self):
        """
            Visual representation of weight bank transfer functions
        """
        lambdas = np.linspace(self.output_wavelength - 5e-9,self.output_wavelength + 5e-9,500)
        plt.figure()
        for i,weight in enumerate(self.weights):
            plt.plot(lambdas*1e9, self.mrr(weight, lambdas)[:,0], color="C" + str(i))
            plt.plot(lambdas*1e9, self.mrr(weight, lambdas)[:,1], "--C" + str(i))
            plt.plot(lambdas*1e9, self.mrr(weight, lambdas)[:,0]+self.mrr(weight, lambdas)[:,1])
        plt.legend(['Weight: ' + str(w) for i in range(2) for w in self.weights])
        plt.vlines(self.output_wavelength*1e9, 0, 1)
        plt.show()
            
#        legend = []
#        for w in self.weights:
#            legend.append('Pass:' + str(w))
#            legend.append('Drop:' + str(w))
#        plt.legend(legend)
        