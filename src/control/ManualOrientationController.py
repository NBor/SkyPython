'''
Created on 2013-05-23

@author: Neil
'''

from Controller import Controller
from ..utils import Geometry

class ManualOrientationController(Controller):
    '''
    classdocs
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
        rotate astronomers view
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
        Constructor
        '''
        Controller.__init__(self)
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    
    