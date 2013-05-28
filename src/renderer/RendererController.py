'''
Created on 2013-05-28

@author: Neil
'''

from Queue import Queue
from RendererControllerBase import RendererControllerBase

class RendererController(RendererControllerBase):
    '''
    classdocs
    '''
    class AtomicSection(RendererControllerBase):
        '''
        classdocs
        '''
        queuer = Queue()
        NEXT_ID = 0
        m_ID = None
        
        def to_string(self):
            return "AtomicSection" + self.m_ID
        
        def release_events(self):
            temp = self.queuer
            self.queuer = Queue()
            return temp
        
        def __init__(self, skyrenderer):
            '''
            constructor
            '''
            RendererControllerBase.__init__(self, skyrenderer)
            #synchronize this next line
            self.m_ID = self.NEXT_ID + 1
    
    queuer = Queue()
    
    def to_string(self):
        return "RendererController"
    
    def create_atomic(self):
        return self.AtomicSection(self.renderer)
    
    def queue_atomic(self, atomic):
        raise NotImplementedError("need queue runnable")

    def __init__(self, skyrenderer, gl_surface_view=None):
        '''
        Some OpenGLES componenets need to be addressed
        '''
        RendererControllerBase.__init__(self, skyrenderer)
        