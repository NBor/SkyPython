'''
Created on 2013-06-05

@author: Neil
'''

from ColorBuffer import ColorBuffer

class NightVisionBuffer(object):
    '''
    classdocs
    '''
    def reset(self, num_verts):
        self.normal_buffer.reset(num_verts)
        self.red_buffer.reset(num_verts)
            
    def reload(self):
        self.normal_buffer.reload()
        self.red_buffer.reload()
        
    def add_color(self, abgr=None, a=None, r=None, g=None, b=None):
        if abgr != None:
            a = int(abgr >> 24) & 0xff
            b = int(abgr >> 16) & 0xff
            g = int(abgr >> 8) & 0xff
            r = int(abgr) & 0xff
        
        self.normal_buffer.add_color(a, r, g, b)
        avg = (r + g + b) / 3
        self.red_buffer.add_color(a, avg, 0, 0)
    
    def set(self, gl, night_vision_mode):
        if night_vision_mode:
            self.red_buffer.set(gl)
        else:
            self.normal_buffer.set(gl)

    def __init__(self, num_verts=0, vbo_bool=False):
        '''
        Constructor
        '''
        self.normal_buffer = ColorBuffer(0, vbo_bool)
        self.red_buffer = ColorBuffer(0, vbo_bool)
        self.reset(num_verts)