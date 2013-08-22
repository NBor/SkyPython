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
// Original Author: Brent Bryan
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-16

@author: Neil Borle
'''

from Source import Source
from src.utils.Colors import colors

class AstronomicalSource(Source):
    '''
    classdocs
    '''
            
    def add_image(self, image):
        self.image_sources.append(image)
        
    def add_line(self, line):
        self.line_sources.append(line)
        
    def add_point(self, point):
        self.point_sources.append(point)
        
    def add_label(self, label):
        self.text_sources.append(label)

    def __init__(self, new_color=colors.WHITE):
        '''
        Constructor
        '''
        Source.__init__(self, new_color)
        self.level = None
        self.names = []
        self.image_sources = []
        self.line_sources = []
        self.point_sources = []
        self.text_sources = []
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    new = AstronomicalSource()
    print new.point_sources