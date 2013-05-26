'''
Created on 2013-05-26

@author: Neil
'''

import math
from units.GeocentricCoordinates import GeocentricCoordinates

class RenderState(object):
    '''
    classdocs
    '''
    camera_pos = GeocentricCoordinates(0, 0, 0)
    look_dir = GeocentricCoordinates(1, 0, 0)
    up_dir = GeocentricCoordinates(0, 1, 0)
    radius_of_view = 45  # in degrees
    up_angle = 0
    cos_up_angle = 1
    sin_up_angle = 0
    screen_width = 100
    screen_height = 100
    #transform_to_device = Matrix4x4.createIdentity()
    #transform_to_screen = Matrix4x4.createIdentity()
    night_vision_mode = False
    active_sky_region_set = None
    
    def set_camera_pos(self, pos):
        self.camera_pos = pos.copy()
        
    def set_look_dir(self, new_dir):
        self.look_dir = new_dir.copy()
        
    def set_up_dir(self, new_dir):
        self.up_dir = new_dir.copy()
        
    def set_up_angle(self, angle):
        self.up_angle = angle
        self.cos_up_angle = math.cos(angle)
        self.sin_up_angle = math.sin(angle)
        
    def set_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
        
    def set_tranformation_matrices(self, to_device, to_screen):
        raise NotImplementedError("no 4x4 matrices")
    
    def __init__(self):
        '''
        Constructor
        '''
        