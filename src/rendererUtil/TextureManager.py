'''
Created on 2013-06-11

@author: Neil
'''

import numpy as np
from PySide.QtGui import QImage
from PySide.QtOpenGL import QGLWidget

def construct_id_to_image_map(filename, id_map):
    with open(filename) as f_handle:
        for line in f_handle:
            [value, key] = line.strip().split("=")
            id_map[int(key, 0)] = value

class TextureManager(object):
    '''
    classdocs
    '''
    class TextureReference(object):
        '''
        classdocs
        '''
        def bind(self, gl):
            self.check_valid()
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
            
        def delete(self, gl):
            self.check_valid
            gl.glDeleteTextures(1, [self.texture_id], 0)
            self.invalidate()
            
        def invalidate(self):
            self.valid = False
            
        def check_valid(self):
            if not self.valid:
                raise Exception("This is not valid")
        
        def __init__(self, Id):
            '''
            constructor
            '''
            self.texture_id = Id
            self.valid = True
            
    class TextureData(object):
        '''
        classdocs
        '''
        
        def __init__(self):
            '''
            constructor
            '''
            self.texture_ref = None
            self.ref_count = 0
    
    images = {}
    id_to_texture_map = {}
    all_textures = []

    def create_texture(self, gl):
        return self.create_texture_internal(gl)
    
    def get_texture_from_resource(self, gl, resource_id):
        # If the texture already exists, return it.
        if resource_id in self.id_to_texture_map.keys():
            text_data = self.id_to_texture_map[resource_id]
            text_data.ref_count += 1
            return text_data.texture_ref
        
        text = self.create_texture_from_resource(gl, resource_id)
    
        # Add it to the map.
        data = self.TextureData()
        data.texture_ref = text
        data.ref_count = 1
        self.id_to_texture_map[resource_id] = data
     
        return text
    
    def reset(self):
        self.id_to_texture_map.clear()
        while len(self.all_textures) > 0:
            self.all_textures[0].invalidate()
            self.all_textures.pop(0)
            
    def create_texture_from_resource(self, gl, resource_id):
        '''
        Unlike the original java source, convertToGLFormat is used
        '''
        text = self.create_texture_internal(gl)
        img = QImage("assets/drawable/" + self.images[resource_id] + ".png")
#         img_data = np.frombuffer(img.bits(), dtype=np.uint8).reshape(\
#             [img.height(), img.width(), -1])
        img = QGLWidget.convertToGLFormat(img)
        
        text.bind(gl)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR);
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR);
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE);
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE);
        
#         gl.glTexImage2D(gl.GL_TEXTURE_2D,  0, gl.GL_RGB, img.width(), img.height(), 
#                       0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width(), img.height(), 0, gl.GL_RGBA, 
                        gl.GL_UNSIGNED_BYTE, str(img.bits()))
        
        return text
    
    def create_texture_internal(self, gl):
        text_id = gl.glGenTextures(1)
        text = TextureManager.TextureReference(text_id)
        self.all_textures.append(text)
        return text

    def __init__(self, testing=False):
        '''
        Constructor
        '''
        if not testing:
            construct_id_to_image_map("assets/RImages.txt", self.images)
        
if __name__ == "__main__":
    import OpenGL.GL as gl
    m_map = {}
    construct_id_to_image_map("../../assets/RImages.txt", m_map)
    for key in m_map.keys():
        print str(key) + ":" + m_map[key]    
        
    TM = TextureManager(True)
    TM.images = m_map
    TM.create_texture_from_resource(gl, 2130837609)