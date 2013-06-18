'''
Created on 2013-06-16

@author: Neil
'''

class AbstractAstronomicalSource(object):
    '''
    classdocs
    '''
    def initialize(self):
        return self
    
    def update(self):
        return set()
    
    def get_images(self):
        return []
    
    def get_labels(self):
        return []
        
    def get_lines(self):
        return []
        
    def get_points(self):
        return []

    def __init__(self):
        '''
        Constructor
        '''
        self.names = []