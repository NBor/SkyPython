'''
Created on 2013-06-26

@author: Neil
'''

import time
from renderer.RendererObjectManager import RendererObjectManager
from Planet import Planet, planet_enum, res
from source.AbstractAstronomicalSource import AbstractAstronomicalSource
from source.PointSource import PointSource
from source.TextSource import TextSource
from source.ImageSource import ImageSource
from units.Vector3 import Vector3
from units.GeocentricCoordinates import GeocentricCoordinates
from units.HeliocentricCoordinates import get_instance
from units.RaDec import get_instance as radec_get_instance

USE_PLANETARY_IMAGES = True

class PlanetSource(AbstractAstronomicalSource):
    '''
    classdocs
    '''
    PLANET_SIZE = 3
    PLANET_COLOR = 0x14817EF6
    PLANET_LABEL_COLOR = 0xf67e81
    SHOW_PLANETARY_IMAGES = "show_planetary_images"
    UP = Vector3(0.0, 1.0, 0.0)
    
    def get_names(self):
        return self.names.append(self.name)
    
    def update_coords(self, t_struct):
        self.last_update_time_Ms = time.mktime(t_struct)
        self.sun_coords = get_instance(t_struct=t_struct,
                                         planet=Planet(planet_enum.SUN, 
                                                       res[planet_enum.SUN][0], 
                                                       res[planet_enum.SUN][1], 
                                                       res[planet_enum.SUN][2]))
        ra_dec = radec_get_instance(earth_coord=self.sun_coords, planet=self.planet, time=t_struct)
        self.current_coords.update_from_ra_dec(ra_dec.ra, ra_dec.dec)
        for imgsrc in self.image_sources:
            imgsrc.set_up_vector(self.sun_coords)
            
    def initialize(self):
        time = self.model.get_time()
        self.update_coords(time)
        self.image_id = self.planet.get_image_resource_id(time)
        
        if self.planet.id == planet_enum.MOON:
            self.image_sources.append(ImageSource(self.current_coords, self.image_id, self.sun_coords, 
                                                  self.planet.get_planetary_image_size()))
        else:
            if USE_PLANETARY_IMAGES or self.planet.id == planet_enum.SUN:
                self.image_sources.append(ImageSource(self.current_coords, self.image_id, self.UP, 
                                                  self.planet.get_planetary_image_size()))
            else:
                self.point_sources.append(PointSource(self.PLANET_COLOR, self.PLANET_SIZE, 
                                                      self.current_coords))
        self.label_sources.append(TextSource(self.name, self.PLANET_LABEL_COLOR, self.current_coords))
        
        return self
    
    #override(AbstractAstronomicalSource)
    def update(self):
        updates = set()
        
        model_time = self.model.get_time()
        if abs(time.mktime(model_time) - self.last_update_time_Ms) > self.planet.get_update_frequency_Ms:
            updates = updates | set([RendererObjectManager().update_type.UpdatePositions])
            # update location
            self.update_coords(model_time)
            
            # For moon only:
            if self.planet.id == planet_enum.MOON and self.image_sources != []:
                # Update up vector.
                self.image_sources[0].set_up_vector(self.sun_coords)
                
                # update image:
                new_image_id = self.planet.get_image_resource_id(model_time)
                if new_image_id != self.image_id:
                    self.image_id = new_image_id
                    self.image_sources[0].image_id = new_image_id
                    updates = updates | set([RendererObjectManager().update_type.UpdateImages])
                    
        return updates
    
    #override(AbstractAstronomicalSource)
    def get_points(self):
        return self.point_sources
    
    #override(AbstractAstronomicalSource)
    def get_labels(self):
        return self.label_sources
    
    #override(AbstractAstronomicalSource)
    def get_images(self):
        return self.image_sources
    
    def __init__(self, planet, model):
        '''
        Constructor
        '''
        AbstractAstronomicalSource.__init__(self)
        
        self.point_sources = []
        self.image_sources = []
        self.label_sources = []
        self.planet = planet
        self.model = model
        self.name = planet.name_resource_id
        self.current_coords = GeocentricCoordinates(0, 0, 0)
        self.sun_coords = None
        self.image_id = -1
        
        self.last_update_time_Ms  = 0
        