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
// Original Author: James Powell
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


Created on 2013-06-11

@author: Neil Borle
'''

from PySide.QtGui import QImage
from PySide.QtOpenGL import QGLWidget

def construct_id_to_image_map(filename, id_map):
    with open(filename) as f_handle:
        for line in f_handle:
            [value, key] = line.strip().split("=")
            id_map[int(key, 0)] = value

class TextureManager(object):
    '''
    Manages the creation and organization of
    textures. 
    '''
    class TextureReference(object):
        '''
        Contains a reference to a texture, it's id, and
        allows for invalidation of that texture
        '''
        def bind(self, gl):
            self.check_valid()
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
            
        def delete(self, gl):
            self.check_valid()
            # based on examples this single arg should be correct
            gl.glDeleteTextures(self.texture_id)
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
        State on the number of times a 
        texture has been referenced
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
        img = QGLWidget.convertToGLFormat(img)
        
        text.bind(gl)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR);
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR);
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE);
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE);
        
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