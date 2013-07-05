'''
Created on 2013-06-26

@author: Neil
'''

from SourceLayer import SourceLayer
from ..provider.PlanetSource import PlanetSource
from ..provider.Planet import Planet, res

class PlanetsLayer(SourceLayer):
    '''
    classdocs
    '''
    def initialize_astro_sources(self, sources):
        for key in res.keys():
            p = Planet(key, res[key][0], res[key][1], res[key][2])
            sources.append(PlanetSource(p, self.model))
    
    def get_layer_id(self):
        return -103
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.3"

    def __init__(self, model):
        '''
        Constructor
        '''
        SourceLayer.__init__(self, True)
        self.model = model