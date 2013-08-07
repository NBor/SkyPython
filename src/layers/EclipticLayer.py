'''
Created on 2013-06-25

@author: Neil
'''

from SourceLayer import SourceLayer
from src.source.AbstractAstronomicalSource import AbstractAstronomicalSource
from src.source.LineSource import LineSource
from src.source.TextSource import TextSource
from src.units.GeocentricCoordinates import get_instance

class EclipticLayer(SourceLayer):
    '''
    classdocs
    '''
    class EclipticSource(AbstractAstronomicalSource):
        '''
        classdocs
        '''
        EPSILON = 23.439281
        LINE_COLOR = 0x14BCEFF8
        
        #override(AbstractAstronomicalSource)
        def get_lines(self):
            return self.line_sources
            
        #override(AbstractAstronomicalSource)
        def get_labels(self):
            return self.text_sources
        
        def __init__(self):
            '''
            constructor
            '''
            AbstractAstronomicalSource.__init__(self)
            
            self.line_sources = []
            self.text_sources = []
            
            title = "Ecliptic"
            self.text_sources.append(TextSource(title, self.LINE_COLOR, 
                                                get_instance(90.0, self.EPSILON)))
            self.text_sources.append(TextSource(title, self.LINE_COLOR, 
                                                get_instance(270.0, -self.EPSILON)))
            
            # Create line source.
            ra = [0.0, 90.0, 180.0, 270.0, 0.0]
            dec = [0.0, self.EPSILON, 0.0, -self.EPSILON, 0.0]
            
            vertices = []
            for i in range(0, len(ra)):
                vertices.append(get_instance(ra[i], dec[i]))
            
            self.line_sources.append(LineSource(vertices, self.LINE_COLOR, 1.5))
    
    def initialize_astro_sources(self, sources):
        sources.append(self.EclipticSource())
        
    def get_layer_id(self):
        return -105
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.5"


    def __init__(self):
        '''
        Constructor
        '''
        SourceLayer.__init__(self, False)