'''
Created on 2013-08-19

@author: Neil
'''

from src.utils.Geometry import radians_to_degrees

class MapMover(object):
    '''
    classdocs
    '''
    
    def on_drag(self, x_pixels, y_pixels):
        pixels_to_rads = self.model.field_of_view / self.size_times_rads_to_degs
        self.control_group.change_up_down(-y_pixels * pixels_to_rads)
        self.control_group.change_right_left(-x_pixels * pixels_to_rads)
        return True
    
    def on_rotate(self, degrees):
        if self.allow_rotation:
            self.control_group.rotate(-degrees)
            return True
        else:
            return False
        
    def on_stretch(self, ratio):
        self.control_group.zoom_by(1.0/ratio)
        return True
    
    def on_shared_preference_change(self, prefs):
        self.allow_rotation = prefs.ALLOW_ROTATION

    def __init__(self, model, controller_group, shared_prefs, screen_height):
        '''
        Constructor
        '''
        
        self.model = model
        self.control_group = controller_group
        self.shared_prefs = shared_prefs
        self.size_times_rads_to_degs = radians_to_degrees(screen_height)
        self.allow_rotation = shared_prefs.ALLOW_ROTATION
        