'''
Created on 2013-05-25

@author: Neil
'''

import math
from numpy import array, float32
import numpy.random as rdn
from OpenGL.arrays import vbo

from units.Vector3 import Vector3
from RendererObjectManager import RendererObjectManager
from rendererUtil.SkyRegionMap import SkyRegionMap
from rendererUtil.IndexBuffer import IndexBuffer
from rendererUtil.VertexBuffer import VertexBuffer
from rendererUtil.ColorBuffer import ColorBuffer
from rendererUtil.TextCoordBuffer import TextCoordBuffer
from utils.VectorUtil import normalized, cross_product

class PointObjectManager(RendererObjectManager):
    '''
    classdocs
    '''

    class RegionData(object):
        '''
        classdocs
        '''
    
        def __init__(self):
            '''
            constructor
            '''
            self.sources = []
            self.vertex_buffer = VertexBuffer(0, True)
            self.index_buffer = IndexBuffer(0, True)
            self.text_coord_buffer = TextCoordBuffer(0, True)
            self.color_buffer = ColorBuffer(0, True)
       
    class RegionDataFactory(object):
        '''
        classdocs
        '''
        def construct(self):
            return PointObjectManager.RegionData()
        
        def __init__(self):
            '''
            constructor
            '''
            
    NUM_STARS_IN_TEXTURE = 2
    MINIMUM_NUM_POINTS_FOR_REGIONS = 200
    COMPUTE_REGIONS = True
    sky_regions = SkyRegionMap()
    texture_ref = None
    
    def update_objects(self, points, update_type):
        only_update_points = True
        # We only care about updates to positions, ignore any other updates.
#     if (updateType.contains(UpdateType.Reset)) {
#       only_update_points = false;
#     } else if (updateType.contains(UpdateType.UpdatePositions)) {
#       // Sanity check: make sure the number of points is unchanged.
#       if (points.size() != self.num_points) {
#         Log.e("PointObjectManager",
#               "Updating PointObjectManager a different number of points: update had " +
#               points.size() + " vs " + self.num_points + " before");
#         return;
#       }
#     } else {
#       return;
#     }
# 
        self.num_points = len(points)
        
        self.sky_regions.clear()
        
        region = SkyRegionMap.CATCHALL_REGION_ID
        if self.COMPUTE_REGIONS: 
            # Find the region for each point, and put it in a separate list
            # for that region.
            for point in points:
                if len(points) < self.MINIMUM_NUM_POINTS_FOR_REGIONS:
                    region = SkyRegionMap.CATCHALL_REGION_ID
                else:
                    region = self.sky_regions.get_object_region(point.geocentric_coords)
                # self.sky_regions.get_region_data(region) is a RegionData instance
                data_for_region = self.sky_regions.get_region_data(region)
                data_for_region.sources.append(point)
        else:
            self.sky_regions.get_region_data(region).sources = points

        # Generate the resources for all of the regions.
        for data in self.sky_regions.region_data.values():
            
            num_vertices = 4 * len(data.sources)
            num_indices = 6 * len(data.sources)
            
            data.vertex_buffer.reset(num_vertices)
            data.color_buffer.reset(num_vertices)
            data.text_coord_buffer.reset(num_vertices)
            data.index_buffer.reset(num_indices)
            
            up = Vector3(0, 1, 0)
            
            # By inspecting the perspective projection matrix, you can show that,
            # to have a quad at the center of the screen to be of size k by k
            # pixels, the width and height are both:
            # k * tan(fovy / 2) / screenHeight
            # This is not difficult to derive.  Look at the transformation matrix
            # in SkyRenderer if you're interested in seeing why this is true.
            # I'm arbitrarily deciding that at a 60 degree field of view, and 480
            # pixels high, a size of 1 means "1 pixel," so calculate size_factor
            # based on this.  These numbers mostly come from the fact that that's
            # what I think looks reasonable.
            fovy_in_radians = 60 * math.pi / 180.0
            size_factor = math.tan(fovy_in_radians * 0.5) / 480
            
            bottom_left_pos = Vector3(0, 0, 0)
            top_left_pos = Vector3(0, 0, 0)
            bottom_right_pos = Vector3(0, 0, 0)
            top_right_pos = Vector3(0, 0, 0)
            
            su = Vector3(0, 0, 0)
            sv = Vector3(0, 0, 0)
            
            index = 0
            
            star_width_in_texels = 1.0 / self.NUM_STARS_IN_TEXTURE
            
            for p_source in data.sources:
                color = 0xff000000 | int(p_source.color)  # Force alpha to 0xff
                bottom_left = index
                top_left = index + 1
                bottom_right = index + 2
                top_right = index + 3
                index += 4
                
                # First triangle
                data.index_buffer.add_index(bottom_left)
                data.index_buffer.add_index(top_left)
                data.index_buffer.add_index(bottom_right)
                
                # Second triangle
                data.index_buffer.add_index(top_right);
                data.index_buffer.add_index(bottom_right);
                data.index_buffer.add_index(top_left);
                
                # PointSource.getPointShape().getImageIndex(); is always 0
                star_index = 0
                
                tex_offset_u = star_width_in_texels * star_index
                
                data.text_coord_buffer.add_text_coord(tex_offset_u, 1);
                data.text_coord_buffer.add_text_coord(tex_offset_u, 0);
                data.text_coord_buffer.add_text_coord(tex_offset_u + star_width_in_texels, 1);
                data.text_coord_buffer.add_text_coord(tex_offset_u + star_width_in_texels, 0);
                
                pos = p_source.geocentric_coords
                u = normalized(cross_product(pos, up))
                v = cross_product(u, pos)
                
                s = p_source.size * size_factor
                
                su.assign(s*u.x, s*u.y, s*u.z)
                sv.assign(s*v.x, s*v.y, s*v.z)
                
                bottom_left_pos.assign(pos.x - su.x - sv.x, pos.y - su.y - sv.y, pos.z - su.z - sv.z)
                top_left_pos.assign(pos.x - su.x + sv.x, pos.y - su.y + sv.y, pos.z - su.z + sv.z)
                bottom_right_pos.assign(pos.x + su.x - sv.x, pos.y + su.y - sv.y, pos.z + su.z - sv.z)
                top_right_pos.assign(pos.x + su.x + sv.x, pos.y + su.y + sv.y, pos.z + su.z + sv.z)
                
                # Add the vertices
                data.vertex_buffer.add_point(bottom_left_pos)
                data.color_buffer.add_color(color)
                
                data.vertex_buffer.add_point(top_left_pos)
                data.color_buffer.add_color(color)
                
                data.vertex_buffer.add_point(bottom_right_pos)
                data.color_buffer.add_color(color)
                
                data.vertex_buffer.add_point(top_right_pos);
                data.color_buffer.add_color(color);
            #data.sources = None
    
    def reload(self, gl, bool_full_reload):
        print "Not implemented"
        #raise NotImplementedError("need OpenGL support")
    
    def draw_internal(self, gl):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        #gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        #gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glFrontFace(gl.GL_CW)
        gl.glCullFace(gl.GL_BACK)
        
        #gl.glEnable(gl.GL_ALPHA_TEST)
        #gl.glAlphaFunc(gl.GL_GREATER, 0.5)
        
        gl.glEnable(gl.GL_TEXTURE_2D)
        
        #self.texture_ref.bind(gl)
        
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
        
        # Render all of the active sky regions.
        active_regions = self.render_state.active_sky_region_set
        active_region_data = self.sky_regions.get_data_for_active_regions(active_regions)
        
        gl.glColor(1,1,1)
        coord_list = []
        for data in active_region_data:
#             for source in data.sources:
#                 coord_list.append([source.geocentric_coords.z, source.geocentric_coords.y])
#         
#         # generate random data points
#         data = array(coord_list, dtype=float32)
#         # initialize the GL widget
#         count = data.shape[0]
#         
#         # create a Vertex Buffer Object with the specified data
#         vertex_bo = vbo.VBO(data)
#         
#         #-----------------------------------------------------------------------
#         # set yellow color for subsequent drawing rendering calls
#         gl.glColor(1,1,1)            
#         # bind the VBO 
#         vertex_bo.bind()
#         #-----------------------------------------------------------------------
#         # tell OpenGL that the VBO contains an array of vertices
#         #gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
#         # these vertices contain 2 single precision coordinates
#         gl.glVertexPointer(2, gl.GL_FLOAT, 0, vertex_bo)
#         # draw "count" points from the VBO
#         gl.glDrawArrays(gl.GL_POINTS, 0, count)
            
            if data.vertex_buffer.num_vertices == 0:
                continue
            
            data.vertex_buffer.set(gl)
            #data.color_buffer.set(gl)#, self.render_state.night_vision_mode)
            #data.text_coord_buffer.set(gl)
            #print data.vertex_buffer.vertex_buffer#, data.color_buffer.color_buffer, data.index_buffer.index_buffer
            data.index_buffer.draw(gl, gl.GL_TRIANGLES)
            
        #gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisable(gl.GL_TEXTURE_2D)
        #gl.glDisable(gl.GL_ALPHA_TEST)
            
    def __init__(self, new_layer, new_texture_manager):
        '''
        change inputs to not be default
        '''
        RendererObjectManager.__init__(self, new_layer, new_texture_manager)
        self.sky_regions.region_data_factory = self.RegionDataFactory()
        self.num_points = 0
        