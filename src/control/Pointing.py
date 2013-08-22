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
// Original Author: John Taylor
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-22

@author: Neil Borle
'''

from src.units.GeocentricCoordinates import GeocentricCoordinates as GC

class Pointing(object):
    '''
    This class is to be ONLY used with AstronomerModel.
    This class holds state on the user direction of view
    '''
    gc_line_of_sight = None
    gc_perpendicular = None

    def get_line_of_sight(self):
        return self.gc_line_of_sight.copy()
        
    def get_perpendicular(self):
        return self.gc_perpendicular.copy()

    #Only the AstronomerModel should change this.
    def update_perpendicular(self, new_perpendicular):
        self.gc_perpendicular.assign(vector3=new_perpendicular)
 
    #Only the AstronomerModel should change this.
    def update_line_of_sight(self, new_line_of_sight):
        self.gc_line_of_sight.assign(vector3=new_line_of_sight)

    def __init__(self, line_of_sight=GC(1.0, 0.0, 0.0), perp=GC(0.0, 1.0, 0.0)):
        '''
        Constructor
        '''
        self.gc_line_of_sight = line_of_sight.copy()
        self.gc_perpendicular = perp.copy()
        
if __name__ == "__main__":
    '''
    Do nothing
    '''
    