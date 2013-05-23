'''
Created on 2013-05-23

@author: Neil
'''

class ZeroMagneticDeclinationCalculator(object):
    '''
    classdocs
    '''
    def get_declination(self):
        return 0
    
    def set_location_and_time(self, lat_long, time_in_mills):
        pass #Do Nothing
    
    def to_string(self):
        return "Zero Magnetic Correction"    

    def __init__(self):
        '''
        Constructor
        '''
        