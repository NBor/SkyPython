'''
Created on 2013-05-28

@author: Neil
'''

from Queue import Queue
from RendererControllerBase import RendererControllerBase
from renderer.RendererControllerBase import command_type
from utils.Runnable import Runnable

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
            
            #Use lock to synchronize
            with self.lock:
                self.m_ID = self.NEXT_ID
                self.NEXT_ID += 1
    
    def to_string(self):
        return "RendererController"
    
    def create_atomic(self):
        return self.AtomicSection(self.renderer)
    
    def queue_atomic(self, atomic):
        def run_method():
            events = atomic.releaseEvents()
            for runnable in events:
                runnable.run()
        
        msg = "Applying " + atomic.toString()
        self.queue_runnable(msg, command_type.SYNCHRONIZATION, Runnable(run_method))

    def __init__(self, skyrenderer, gl_surface_view=None):
        '''
        Some OpenGLES componenets need to be addressed
        '''
        RendererControllerBase.__init__(self, skyrenderer)
        self.queuer = Queue()
        