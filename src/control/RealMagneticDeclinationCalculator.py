'''
Created on 2013-05-23

@author: Neil
'''

class RealMagneticDeclinationCalculator(object):
    '''
    This class provides an interface to access data from
    phone hardware to obtain magnetic declination.
    
    This class in not functional
    '''
    geo_magnetic_field = None
    
    def get_declination(self):
        if self.geo_magnetic_field == None:
            return 0
        else:
            raise NotImplementedError("Not implemented")
    
    def set_location_and_time(self, lat_long, time_in_mills):
        self.geo_magnetic_field = None # change this
        raise NotImplementedError("Not implemented yet")
    
    def to_string(self):
        return "Real Magnetic Correction"

    def __init__(self):
        '''
        Constructor
        '''
        