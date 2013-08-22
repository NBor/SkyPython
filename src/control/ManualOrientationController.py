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
Created on 2013-05-23

@author: Neil Borle
'''

from Controller import Controller
from src.utils import Geometry

class ManualOrientationController(Controller):
    '''
    This class is responsible for the manual rotation
    of the sky relative to the astronomer.
    '''
    def start(self):
        pass
    
    def stop(self):
        pass

    def change_right_left(self, radians):
        '''
        Moves the astronomer's pointing right or left
        @param radians the angular change in the pointing in radians (only
        accurate in the limit as radians tends to 0.)
        '''
        if not self.enabled: return
        
        pointing = self.model.pointing
        pointing_xyz = pointing.get_line_of_sight()
        top_xyz = pointing.get_perpendicular()
        
        horizontal_xyz = Geometry.vector_product(pointing_xyz, top_xyz)
        delta_xyz = Geometry.scale_vector(horizontal_xyz, radians)
        
        new_pointing_xyz = Geometry.add_vectors(pointing_xyz, delta_xyz)
        new_pointing_xyz.normalize()
        
        self.model.set_pointing(new_pointing_xyz, top_xyz)

    def change_up_down(self, radians):
        '''
        Moves the astronomer's pointing up or down.
        
        @param radians the angular change in the pointing in radians (only
        accurate in the limit as radians tends to 0.)
        '''
        if not self.enabled: return
        
        pointing = self.model.pointing
        pointing_xyz = pointing.get_line_of_sight()
        top_xyz = pointing.get_perpendicular()
        
        delta_xyz = Geometry.scale_vector(top_xyz, -radians)
        new_pointing_xyz = Geometry.add_vectors(pointing_xyz, delta_xyz)
        new_pointing_xyz.normalize()
        
        delta_up_xyz = Geometry.scale_vector(pointing_xyz, radians)
        new_up_xyz = Geometry.add_vectors(top_xyz, delta_up_xyz)
        new_up_xyz.normalize()
        
        self.model.set_pointing(new_pointing_xyz, new_up_xyz)
        
    def rotate(self, degrees):
        '''
        rotate astronomers view (clockwise/anti-clockwise)
        '''
        if not self.enabled: return 
        
        pointing = self.model.pointing
        pointing_xyz = pointing.get_line_of_sight()
        top_xyz = pointing.get_perpendicular()
        
        rotation = Geometry.calculate_rotation_matrix(degrees, pointing_xyz)
        
        new_up_xyz = Geometry.matrix_vector_multiply(rotation, top_xyz)
        new_up_xyz.normalize()
        
        self.model.set_pointing(pointing_xyz, new_up_xyz)

    def __init__(self):
        '''
        Constructor, initialize superclass
        '''
        Controller.__init__(self)
        
if __name__ == "__main__":
    '''
    Do nothing
    '''
    
    