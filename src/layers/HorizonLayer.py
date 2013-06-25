'''
Created on 2013-06-24

@author: Neil
'''

from SourceLayer import SourceLayer
from source.AbstractAstronomicalSource import AbstractAstronomicalSource
from source.LineSource import LineSource
from source.TextSource import TextSource
from renderer.RendererObjectManager import RendererObjectManager
from units.GeocentricCoordinates import GeocentricCoordinates
from base.TimeConstants import MILLISECONDS_PER_SECOND

class HorizonLayer(SourceLayer):
    '''
    classdocs
    '''
    class HorizonSource(AbstractAstronomicalSource):
        '''
        classdocs
        '''
        # Due to a bug in the G1 rendering code text and lines render in different
        # colors.
        LINE_COLOR = 0x78F5B056
        LABEL_COLOR = 0x7856B0F5
        UPDATE_FREQ_MS = 1 * MILLISECONDS_PER_SECOND
        
        def update_coords(self):
            self.last_update_time_Ms = self.model.get_time()
            
            self.zenith.assign(vector3=self.model.get_zenith())
            self.nadir.assign(vector3=self.model.get_nadir())
            self.north.assign(vector3=self.model.get_north())
            self.south.assign(vector3=self.model.get_south())
            self.east.assign(vector3=self.model.get_east())
            self.west.assign(vector3=self.model.get_west())
            
        def initialize(self):
            self.update_coords()
            return self
        
        def update(self):
            update_types = set()
            
            if abs(self.model.get_time() - self.last_update_time_Ms > self.UPDATE_FREQ_MS):
                self.update_coords()
                update = RendererObjectManager().update_type.UpdatePositions
                update_types = set([update])
                
            return update_types
        
        #override(AbstractAstronomicalSource)
        def get_labels(self):
            return self.text_sources
        
        #override(AbstractAstronomicalSource)
        def get_lines(self):
            return self.line_sources
        
        def __init__(self, model):
            '''
            constructor
            '''
            AbstractAstronomicalSource.__init__(self)
            self.zenith = GeocentricCoordinates(0, 0, 0)
            self.nadir = GeocentricCoordinates(0, 0, 0)
            self.north = GeocentricCoordinates(0, 0, 0)
            self.south = GeocentricCoordinates(0, 0, 0)
            self.east = GeocentricCoordinates(0, 0, 0)
            self.west = GeocentricCoordinates(0, 0, 0)
        
            self.line_sources = []
            self.text_sources = []
        
            self.lastUpdateTimeMs = 0
            
            self.model = model
            
            vertices = [self.north, self.east, self.south, self.west, self.north]
            self.line_sources.append(LineSource(vertices, self.LINE_COLOR, 1.5))
            
            self.text_sources.append(TextSource("ZENITH", self.LABEL_COLOR, self.zenith))
            self.text_sources.append(TextSource("NADIR", self.LABEL_COLOR, self.nadir))
            self.text_sources.append(TextSource("NORTH", self.LABEL_COLOR, self.north))
            self.text_sources.append(TextSource("SOUTH", self.LABEL_COLOR, self.south))
            self.text_sources.append(TextSource("EAST", self.LABEL_COLOR, self.east))
            self.text_sources.append(TextSource("WEST", self.LABEL_COLOR, self.west))
    
    def initialize_astro_sources(self, sources):
        sources.append(self.HorizonSource(self.model))
    
    def get_layer_id(self):
        return -106
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.6"
    
    def get_layer_name(self):
        return "Horizon"


    def __init__(self, model):
        '''
        Constructor
        '''
        SourceLayer.__init__(self, True)
        self.model = model
        