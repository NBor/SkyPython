'''
Created on 2013-06-25

@author: Neil
'''

import datetime as dt
from time import mktime
from datetime import datetime
from SourceLayer import SourceLayer
from ..base.TimeConstants import MILLISECONDS_PER_DAY
from ..source.AbstractAstronomicalSource import AbstractAstronomicalSource
from ..source.TextSource import TextSource
from ..source.ImageSource import ImageSource
from ..renderer.RendererObjectManager import RendererObjectManager
from ..units.Vector3 import Vector3
from ..units.GeocentricCoordinates import get_instance

class MeteorShowerLayer(SourceLayer):
    '''
    classdocs
    '''
    class Shower(object):
        def __init__(self, name_id, radiant, start, peak, end, peak_meteors_per_hour):
            self.name_id = name_id
            self.radiant = radiant
            self.start = start
            self.peak = peak
            self.end = end
            self.peak_meteors_per_hour = peak_meteors_per_hour
            
    class MeteorRadiantSource(AbstractAstronomicalSource):
        '''
        classdocs
        '''
#         LABEL_COLOR = 0xf67e81
        LABEL_COLOR = 0x817ef6
        UP = Vector3(0.0, 1.0, 0.0)
        UPDATE_FREQ_MS = 1 * MILLISECONDS_PER_DAY
        SCALE_FACTOR = 0.03
        
        def get_names(self):
            return self.search_names
        
        def get_search_location(self):
            return self.shower.radiant
        
        def update_shower(self):
            self.last_update_time_Ms = mktime(self.model.get_time())
            # We will only show the shower if it's the right time of year.
            now = self.model.get_time()
            # Standardize on the same year as we stored for the showers.
            now = dt.datetime(MeteorShowerLayer.ANY_OLD_YEAR,
                              now.tm_mon,now.tm_mday,0,0,0).timetuple()
            
            self.the_image.set_up_vector(self.UP)
            if mktime(self.shower.start) < mktime(now) and \
                    mktime(self.shower.end) > mktime(now):
                self.label.label = self.name
                percent_to_peak = 0
                if (mktime(now) < mktime(self.shower.peak)):
                    percent_to_peak = (mktime(now) - mktime(self.shower.start)) / \
                        (mktime(self.shower.peak) - mktime(self.shower.start))
                else:
                    percent_to_peak = (mktime(self.shower.end) - mktime(now)) / \
                        (mktime(self.shower.end) - mktime(self.shower.peak))
                      
                # Not sure how best to calculate number of meteors - use linear interpolation for now.
                number_of_meteors_per_hour = self.shower.peak_meteors_per_hour * percent_to_peak
                
                if number_of_meteors_per_hour > MeteorShowerLayer.METEOR_THRESHOLD_PER_HR:
                    self.the_image.set_image_id("meteor2_screen")
                else:
                    self.the_image.set_image_id("meteor1_screen")
                  
            else:
                self.label.label = " "
                self.the_image.set_image_id("blank")
                
        def initialize(self):
            self.update_shower()
            return self
        
        #override(AbstractAstronomicalSource)        
        def update(self):
            update_types = set()
            if abs(mktime(self.model.get_time()) - self.last_update_time_Ms) > self.UPDATE_FREQ_MS:
                self.update_shower()
                update_types = set([RendererObjectManager().update_type.Reset])
                
            return update_types
        
        #override(AbstractAstronomicalSource)
        def get_images(self):
            return self.image_sources
        
        #override(AbstractAstronomicalSource)
        def get_labels(self):
            return self.label_sources
        
        def __init__(self, model, shower):
            '''
            constructor
            '''
            AbstractAstronomicalSource.__init__(self)
            self.image_sources = []
            self.label_sources = []
            
            self.lastUpdateTimeMs = 0
            self.search_names = []
            
            self.model = model
            self.shower = shower
            self.name = shower.name_id
            
            start_date = datetime.fromtimestamp(mktime(shower.start)).strftime('%m/%d')
            end_date = datetime.fromtimestamp(mktime(shower.end)).strftime('%m/%d')
            self.search_names.append(self.name + " (" + start_date + "-" + end_date + ")")
            
            # blank is a 1pxX1px image that should be invisible.
            # We'd prefer not to show any image except on the shower dates, but there
            # appears to be a bug in the renderer/layer interface in that Update values are not
            # respected.  Ditto the label.
            
            self.the_image = ImageSource(shower.radiant, "blank", self.UP, self.SCALE_FACTOR)
            self.image_sources.append(self.the_image)
            self.label = TextSource(self.name, self.LABEL_COLOR, shower.radiant)
            self.label_sources.append(self.label)
    
    ANY_OLD_YEAR = 2000
    # Number of meteors per hour for the larger graphic
    METEOR_THRESHOLD_PER_HR = 10
    
    def initialize_showers(self):
        # A list of all the meteor showers with > 10 per hour
        # Source: http://www.imo.net/calendar/2011#table5
        # Note the zero-based month. 10=November
        # Actual start for Quadrantids is December 28 - but we can't cross a year boundary.
        self.showers.append(self.Shower("Quadrantids", get_instance(230, 49),
                                        dt.datetime(self.ANY_OLD_YEAR,1,1,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,1,4,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,1,12,0,0,0).timetuple(),
                                        120))
        self.showers.append(self.Shower("Lyrids", get_instance(271, 34),
                                        dt.datetime(self.ANY_OLD_YEAR,4,16,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,4,22,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,4,25,0,0,0).timetuple(),
                                        18))
        self.showers.append(self.Shower("Eta Aquariids", get_instance(338, -1),
                                        dt.datetime(self.ANY_OLD_YEAR,4,19,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,5,6,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,5,28,0,0,0).timetuple(),
                                        70))
        self.showers.append(self.Shower("Delta Aquariids", get_instance(340, -16),
                                        dt.datetime(self.ANY_OLD_YEAR,7,12,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,7,30,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,8,23,0,0,0).timetuple(),
                                        16))
        self.showers.append(self.Shower("Perseids", get_instance(48, 58),
                                        dt.datetime(self.ANY_OLD_YEAR,7,17,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,8,13,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,8,24,0,0,0).timetuple(),
                                        100))
        self.showers.append(self.Shower("Orionids", get_instance(95, 16),
                                        dt.datetime(self.ANY_OLD_YEAR,10,2,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,10,21,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,11,7,0,0,0).timetuple(),
                                        25))
        self.showers.append(self.Shower("Leonids", get_instance(152, 22),
                                        dt.datetime(self.ANY_OLD_YEAR,11,6,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,11,18,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,11,30,0,0,0).timetuple(),
                                        20))
        self.showers.append(self.Shower("Puppid-Velids", get_instance(123, -45),
                                        dt.datetime(self.ANY_OLD_YEAR,12,1,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,12,7,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,12,15,0,0,0).timetuple(),
                                        10))
        self.showers.append(self.Shower("Geminids", get_instance(112, 33),
                                        dt.datetime(self.ANY_OLD_YEAR,12,7,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,12,14,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,12,17,0,0,0).timetuple(),
                                        120))
        self.showers.append(self.Shower("Ursids", get_instance(217, 76),
                                        dt.datetime(self.ANY_OLD_YEAR,12,17,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,12,23,0,0,0).timetuple(),
                                        dt.datetime(self.ANY_OLD_YEAR,12,26,0,0,0).timetuple(),
                                        10))
    
    def initialize_astro_sources(self, sources):
        for shower in self.showers:
            sources.append(self.MeteorRadiantSource(self.model, shower))
    
    def get_layer_id(self):
        return -107
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.7"
    
    def get_layer_name(self):
        return "Meteor Showers"

    def __init__(self, model):
        '''
        Constructor
        '''
        SourceLayer.__init__(self, True)
        
        self.showers = []
        self.model = model
        self.initialize_showers()
        