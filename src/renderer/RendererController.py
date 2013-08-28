'''
// Copyright 2009 Google Inc.
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


Created on 2013-05-28

@author: Neil Borle
'''

import threading
from Queue import Queue
from RendererControllerBase import RendererControllerBase
from src.renderer.RendererControllerBase import command_type
from src.utils.Runnable import Runnable

class RendererController(RendererControllerBase):
    '''
    The class for controlling atomic rendering
    events. Runnable atomic sections are created and then
    placed on the queue of runnable objects.
    '''
    class AtomicSection(RendererControllerBase):
        '''
        classdocs
        '''
        NEXT_ID = 0
        lock = threading.Lock()
        
        def to_string(self):
            return "AtomicSection " + str(self.m_ID)
        
        def release_events(self):
            temp = self.queuer
            self.queuer = Queue()
            return temp
        
        def __init__(self, skyrenderer):
            '''
            constructor
            '''
            RendererControllerBase.__init__(self, skyrenderer)
            self.queuer = Queue()
            
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
            events = atomic.release_events()
            for runnable in list(events.queue):
                runnable.run()
        
        msg = "Applying " + atomic.to_string()
        self.queue_runnable(msg, command_type.SYNCHRONIZATION, Runnable(run_method))

    def __init__(self, skyrenderer, gl_surface_view=None):
        '''
        Some OpenGLES componenets need to be addressed
        '''
        RendererControllerBase.__init__(self, skyrenderer)
        self.queuer = Queue()
        