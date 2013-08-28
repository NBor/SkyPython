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
// Original Author: John Taylor
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


Created on 2013-06-09

@author: Neil Borle
'''

from Controller import Controller

class ZoomController(Controller):
    '''
    This controller is responsible for setting the
    zoom factor for the night sky.
    '''
    ZOOM_FACTOR = pow(1.5, 0.0625)
    MAX_ZOOM_OUT = 90.0
    
    def zoom_in(self):
        '''
        Decreases the field of view by ZOOM_FACTOR
        '''
        self.zoom_by(1.0 / float(self.ZOOM_FACTOR))

    def zoom_out(self):
        '''
        Increases the field of view by ZOOM_FACTOR
        '''
        self.zoom_by(self.ZOOM_FACTOR)

    def __set_field_of_view(self, zoom_degrees):
        if not self.enabled:
            return
        self.model.field_of_view = zoom_degrees

    def start(self):
        pass

    def stop(self):
        pass
    
    def zoom_by(self, ratio):
        zoom_degrees = self.model.field_of_view
        zoom_degrees = min(zoom_degrees * ratio, self.MAX_ZOOM_OUT)
        self.__set_field_of_view(zoom_degrees)

    def __init__(self):
        '''
        Constructor
        '''
        Controller.__init__(self)
        