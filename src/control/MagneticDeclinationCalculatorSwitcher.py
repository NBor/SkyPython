'''
Created on 2013-06-28

@author: Neil
'''

from ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator
from RealMagneticDeclinationCalculator import RealMagneticDeclinationCalculator

class MagneticDeclinationCalculatorSwitcher(object):
    '''
    Aggregates the RealMagneticDeclinationCalculator and the
    ZeroMagneticDeclinationCalculator and switches them in the AstronomerModel.
    '''
    def set_the_models_calculator(self, use_real):
        if use_real:
            self.model.set_mag_dec_calc(self.real_calculator)
        else:
            self.model.set_mag_dec_calc(self.zero_calculator)

    def __init__(self, model, use_real=False):
        '''
        Constructor
        '''
        self.zero_calculator = ZeroMagneticDeclinationCalculator()
        self.real_calculator = RealMagneticDeclinationCalculator()
        self.model = model
        self.set_the_models_calculator(use_real)
        