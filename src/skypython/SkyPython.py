'''
Created on 2013-06-03

@author: Neil
'''

from OpenGL import GL
from PySide.QtOpenGL import QGLWidget
from PySide.QtGui import QMainWindow

class SkyPython(QGLWidget, QMainWindow):
    '''
    classdocs
    '''
    # default window size
    width, height = 480, 800
    sky_renderer = None
    
    def __init__(self, sky_rend):
        QGLWidget.__init__(self)
        self.sky_renderer = sky_rend
        
        # put the window at the screen position (100, 100)
        self.setGeometry(100, 25, self.width, self.height)
        self.show()
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        GL.glClearColor(0,0,0,0)
 
    def paintGL(self):
        """Paint the scene.
        """
        self.sky_renderer.on_draw_frame(GL)
 
    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size
        self.width, self.height = width, height
        # paint within the whole window
        GL.glViewport(0, 0, width, height)
        # set orthographic projection (2D only)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        GL.glOrtho(-1, 1, -1, 1, -1, 1)
        