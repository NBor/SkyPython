'''
// Copyright 2008 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 
// Original Author: John Taylor, Brent Bryan
// 
// Notification of Change: The original java source code has been
// modified in that it has been rewritten in the python programming
// language and additionally, may contain components and ideas that are 
// not found in the original source code.


   Copyright 2013 Neil Borle and Paul Lu

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


Created on 2013-06-16

@author: Neil Borle
'''

from SourceLayer import SourceLayer
from src.source.AbstractAstronomicalSource import AbstractAstronomicalSource
from src.source.LineSource import LineSource
from src.source.TextSource import TextSource
from src.units.RaDec import RaDec
from src.units.GeocentricCoordinates import get_instance

class GridLayer(SourceLayer):
    '''
    creates a Layer which returns Sources which correspond to grid lines parallel
    to the celestial equator and the hour angle. That is, returns a set of lines
    with constant right ascension, and another set with constant declination.
    '''
    class GridSource(AbstractAstronomicalSource):
        '''
        Grid elements as astronomical sources so that they
        can be rendered just like any other astronomical object.
        '''
        def create_ra_line(self, index, num_ra_sources):
            '''
            Constructs a single longitude line. These lines run from the north pole to
            the south pole at fixed Right Ascensions.
            '''
            line = LineSource([], self.LINE_COLOR)
            ra = index * 360.0 / num_ra_sources
            for i in range(0, self.NUM_DEC_VERTICES - 1):
                dec = 90.0 - i * 180.0 / (self.NUM_DEC_VERTICES - 1)
                ra_dec = RaDec(ra, dec)
                line.ra_decs.append(ra_dec)
                line.gc_vertices.append(get_instance(ra, dec))
            ra_dec = RaDec(0.0, -90.0)
            line.ra_decs.append(ra_dec)
            line.gc_vertices.append(get_instance(0.0, -90.0))
            return line
        
        def create_dec_line(self, index, num_dec_sources):
            '''
            Creates a single latitudinal line.
            '''
            line = LineSource([], self.LINE_COLOR)
            dec = 90.0 - (index + 1.0) * 180.0 / (num_dec_sources + 1.0)
            for i in range(0, self.NUM_RA_VERTICES):
                ra = i * 360.0 / self.NUM_RA_VERTICES
                ra_dec = RaDec(ra, dec)
                line.ra_decs.append(ra_dec)
                line.gc_vertices.append(get_instance(ra, dec))
            ra_dec = RaDec(0.0, dec)
            line.ra_decs.append(ra_dec)
            line.gc_vertices.append(get_instance(0.0, dec))
            return line
            
        #override(AbstractAstronomicalSource)
        def get_lines(self):
            return self.line_sources
        
        #override(AbstractAstronomicalSource)
        def get_labels(self):
            return self.text_sources
        
        def __init__(self, num_RA_sources, num_De_sources):
            '''
            constructor
            '''
            AbstractAstronomicalSource.__init__(self)
            
            self.LINE_COLOR = 0x14F8EFBC
            # These are great (semi)circles, so only need 3 points.
            self.NUM_DEC_VERTICES = 3
            # every 10 degrees
            self.NUM_RA_VERTICES = 36

            self.line_sources = []
            self.text_sources = []
            
            for r in range(0, num_RA_sources):
                self.line_sources.append(self.create_ra_line(r, num_RA_sources))
            for d in range(0, num_De_sources):
                self.line_sources.append(self.create_dec_line(d, num_De_sources))
                
            # North & South pole, hour markers every 2hrs.
            self.text_sources.append(TextSource("NP", self.LINE_COLOR, 
                                                get_instance(0.0, 90.0)))
            self.text_sources.append(TextSource("SP", self.LINE_COLOR, 
                                                get_instance(0.0, -90.0)))
            
            for index in range(0, 12):
                ra = index * 30.0
                title = str(index * 2) + "h"
                self.text_sources.append(TextSource(title, self.LINE_COLOR, 
                                                    get_instance(ra, 0.0)))
    
    def initialize_astro_sources(self, sources):
        sources.append(self.GridSource(self.num_RA_sources, self.num_De_sources))
        
    def get_layer_id(self):
        return -104
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.4"

    def __init__(self, num_right_asc_lines, num_dec_lines):
        '''
        Constructor
        '''
        SourceLayer.__init__(self, False)
        self.num_RA_sources = num_right_asc_lines
        self.num_De_sources = num_dec_lines
        