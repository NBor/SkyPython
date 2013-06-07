'''
Created on 2013-06-03

@author: Neil
'''

from OpenGL import GL
from PySide.QtOpenGL import QGLWidget
from PySide.QtGui import QMainWindow

from source.AstronomicalSource import AstronomicalSource
from renderer.PointObjectManager import PointObjectManager
from renderer.PolyLineObjectManager import PolyLineObjectManager

class SkyPython(QGLWidget, QMainWindow):
    '''
    classdocs
    '''
    # default window size
    width, height = 480, 800
    sky_renderer = None
    
    def __init__(self, m_sky_rend, m_manager, m_model):
        QGLWidget.__init__(self)
        self.sky_renderer = m_sky_rend
        self.layer_manager = m_manager
        self.model = m_model
        
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
            print proto_source
            new_astro = AstronomicalSource()
            new_astro.names = proto_source.names
            new_astro.geocentric_coords = proto_source.get_geo_coords()
            new_astro.image_sources = proto_source.get_images()
            new_astro.point_sources = proto_source.get_points()
            new_astro.line_sources = proto_source.get_lines()
            new_astro.text_sources = proto_source.get_labels()
            points += new_astro.point_sources
            lines += new_astro.line_sources
        POM.update_objects(points, None)
        PLOM.update_objects(lines, None)
        
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
        