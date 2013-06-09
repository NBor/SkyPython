'''
Created on 2013-06-03

@author: Neil
'''

import math
from OpenGL import GL
from PySide.QtOpenGL import QGLWidget
from PySide.QtGui import QMainWindow

from layers.LayerManager import instantiate_layer_manager
from control.AstronomerModel import AstronomerModel
from renderer.SkyRenderer import SkyRenderer
from renderer.RendererController import RendererController
from control.ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator as ZMDC
from renderer.RendererObjectManager import RendererObjectManager
from source.AstronomicalSource import AstronomicalSource
from renderer.PointObjectManager import PointObjectManager
from renderer.PolyLineObjectManager import PolyLineObjectManager

class SkyPython(QGLWidget, QMainWindow):
    '''
    classdocs
    '''
    class RendererModelUpdateClosure():
        '''
        classdocs
        '''
        def run(self):
            pointing = self.model.get_pointing()
            direction_x = pointing.gc_line_of_sight.x
            direction_y = pointing.gc_line_of_sight.y
            direction_z = pointing.gc_line_of_sight.z
            
            up_x = pointing.gc_perpendicular.x
            up_y = pointing.gc_perpendicular.y
            up_z = pointing.gc_perpendicular.z
     
            self.renderer_controller.queue_set_view_orientation(direction_x, direction_y, direction_z, \
                                                             up_x, up_y, up_z)
            
            acceleration = self.model.acceleration
            self.renderer_controller.queue_text_angle(math.atan2(-acceleration.x, -acceleration.y))
            self.renderer_controller.queue_viewer_up_direction(self.model.get_zenith().copy())
            
            field_of_view = self.model.field_of_view
            self.renderer_controller.queue_field_of_view(field_of_view)
        
        def __init__(self, m_model, controller):
            '''
            constructor
            '''
            self.model = m_model
            self.renderer_controller = controller
    
    # default window size
    width, height = 480, 800
    layer_manager = None
    model = None
    sky_renderer = None
    renderer_controller = None
    
    def initialize_model_view_controller(self):
        self.sky_renderer = SkyRenderer()
        self.renderer_controller = RendererController(self.sky_renderer, None)
        self.renderer_controller.add_update_closure(\
            self.RendererModelUpdateClosure(self.model, self.renderer_controller))
        
        self.layer_manager.register_with_renderer(self.renderer_controller)
    
    def __init__(self):
        QGLWidget.__init__(self)
        
        self.layer_manager = instantiate_layer_manager()
        self.model = AstronomerModel(ZMDC())
        self.initialize_model_view_controller()
        
        # put the window at the screen position (100, 100)
        self.setGeometry(100, 30, self.width, self.height)
        self.show()
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        self.sky_renderer.on_surfaced_created(GL)
        self.layer_manager.init_layers()
        
        POM = PointObjectManager(-100, None)
        PLOM = PolyLineObjectManager(-100, None)
        
        astro_source_list = []
        for x in self.layer_manager.layers:
            astro_source_list += x.astro_sources
    
        points = []
        lines = []
        for proto_source in astro_source_list:
            new_astro = AstronomicalSource()
            new_astro.names = proto_source.names
            new_astro.geocentric_coords = proto_source.get_geo_coords()
            new_astro.image_sources = proto_source.get_images()
            new_astro.point_sources = proto_source.get_points()
            new_astro.line_sources = proto_source.get_lines()
            new_astro.text_sources = proto_source.get_labels()
            points += new_astro.point_sources
            lines += new_astro.line_sources
        POM.update_objects(points, set([0]))
        PLOM.update_objects(lines, set([0]))
        
        self.sky_renderer.add_object_manager(POM)
        self.sky_renderer.add_object_manager(PLOM)
 
    def paintGL(self):
        """Paint the scene.
        """
        self.sky_renderer.on_draw_frame(GL)
 
    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size
        self.width, self.height = width, height
        self.sky_renderer.on_surface_changed(GL, width, height)
        # set orthographic projection (2D only)
        #GL.glMatrixMode(GL.GL_PROJECTION)
        #GL.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        #GL.glOrtho(-1, 1, -1, 1, -1, 1)
        