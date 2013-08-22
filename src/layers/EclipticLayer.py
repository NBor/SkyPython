'''
// Copyright 2009 Google Inc.
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
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-06-25

@author: Neil Borle
'''

from SourceLayer import SourceLayer
from src.source.AbstractAstronomicalSource import AbstractAstronomicalSource
from src.source.LineSource import LineSource
from src.source.TextSource import TextSource
from src.units.GeocentricCoordinates import get_instance

class EclipticLayer(SourceLayer):
    '''
    This class is the ecliptic, the apparent path of the sun
    relative to the earth. This appears with the background
    grid and is not parallel to the grid lines.
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