'''
Created on 2013-06-06

@author: Neil
'''

import math
from RendererObjectManager import RendererObjectManager
from rendererUtil.VertexBuffer import VertexBuffer
from rendererUtil.TextCoordBuffer import TextCoordBuffer
from rendererUtil.NightVisionColorBuffer import NightVisionBuffer
from rendererUtil.IndexBuffer import IndexBuffer
from rendererUtil.TextureManager import TextureManager
from utils.VectorUtil import difference, sum_vectors, normalized, cross_product

DRAWABLE_LINE = int("0x7f02003a", 0)

class PolyLineObjectManager(RendererObjectManager):
    '''
    classdocs
    '''
    def update_objects(self, lines, update_type):
        # We only care about updates to positions, ignore any other updates.
        if not (self.update_type.Reset in update_type) and \
                not (self.update_type.UpdatePositions in update_type):
            return

        num_line_segments = 0;
        for l_source in lines:
            num_line_segments += len(l_source.gc_vertices) - 1
            
        # To render everything in one call, we render everything as a line list
        # rather than a series of line strips.
        num_vertices = 4 * num_line_segments
        num_indices = 6 * num_line_segments
        
        vb = self.vertex_buffer
        vb.reset(4 * num_line_segments)
        cb = self.color_buffer
        cb.reset(4 * num_line_segments)
        tb = self.text_coord_buffer
        tb.reset(num_vertices)
        ib = self.index_buffer
        ib.reset(num_indices)
        
        # See comment in PointObjectManager for justification of this calculation.
        fovy_in_radians = 60 * math.pi / 180.0 
        size_factor = math.tan(fovy_in_radians * 0.5) / 480.0
        
        bool_opaque = True
        
        vertex_index = 0
        
        for l_source in lines:
            coords_list = l_source.gc_vertices
            if len(coords_list) < 2:
                continue
                
            # If the color isn't fully opaque, set opaque to false.
            color = l_source.color
            bool_opaque &= int(color & 0xff000000) == 0xff000000
            
            # Add the vertices.
            for i in range(0, len(coords_list) - 1):
                p1 = coords_list[i]
                p2 = coords_list[i+1]
                u = difference(p2, p1)
                # The normal to the quad should face the origin at its midpoint.
                avg = sum_vectors(p1, p2)
                avg.scale(0.5)
                # I'm assum_vectorsing that the points will already be on a unit sphere.  If this is not the case,
                # then we should normalize it here.
                v = normalized(cross_product(u, avg))
                v.scale(size_factor * l_source.line_width)
                
                
                # Add the vertices
                
                # Lower left corner
                vb.add_point(difference(p1, v))
                cb.add_color(color)
                tb.add_text_coord(0, 1)
                
                # Upper left corner
                vb.add_point(sum_vectors(p1, v))
                cb.add_color(color)
                tb.add_text_coord(0, 0)
                
                # Lower left corner
                vb.add_point(difference(p2, v))
                cb.add_color(color)
                tb.add_text_coord(1, 1)
                
                # Upper left corner
                vb.add_point(sum_vectors(p2, v))
                cb.add_color(color)
                tb.add_text_coord(1, 0)
                
                
                # Add the indices
                bottom_left = vertex_index
                top_left = vertex_index + 1
                bottom_right = vertex_index +2
                top_right = vertex_index + 3
                vertex_index += 4
                
                # First triangle
                ib.add_index(bottom_left)
                ib.add_index(top_left)
                ib.add_index(bottom_right)
                
                # Second triangle
                ib.add_index(bottom_right)
                ib.add_index(top_left)
                ib.add_index(top_right)
        self.opaque = bool_opaque

    def reload(self, gl, full_reload=False):
        TM = TextureManager()
        self.texture_ref = TM.get_texture_from_resource(gl, DRAWABLE_LINE)
        self.vertex_buffer.reload()
        self.color_buffer.reload()
        self.text_coord_buffer.reload()
        self.index_buffer.reload()
        
    def draw_internal(self, gl):
        if self.index_buffer.num_indices == 0:
            return
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
            
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.texture_ref.bind(gl)
        
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glFrontFace(gl.GL_CW)
        gl.glCullFace(gl.GL_BACK)
        
        if not self.opaque:
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE);
        
        self.vertex_buffer.set(gl)
        self.color_buffer.set(gl, self.render_state.night_vision_mode)
        self.text_coord_buffer.set(gl)
        self.index_buffer.draw(gl, gl.GL_TRIANGLES)
        
        if not self.opaque:
            gl.glDisable(gl.GL_BLEND)
            
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)

    def __init__(self, new_layer, new_texture_manager):
        '''
        Constructor
        '''
        RendererObjectManager.__init__(self, new_layer, new_texture_manager)
        self.vertex_buffer = VertexBuffer(True)
        self.color_buffer = NightVisionBuffer(True)
        self.text_coord_buffer = TextCoordBuffer(True)
        self.index_buffer = IndexBuffer(True)
        self.texture_ref = None
        self.opaque = True