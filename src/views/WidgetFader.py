'''
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


Created on 2013-08-12

@author: Neil Borle
'''

from PySide.QtCore import QTimer

class WidgetFader(object):
    '''
    For a given widget in the UI, this fader attaches a timer 
    that hides that widget after a specified interval
    '''
    
    def make_active(self):
        '''
        shows the widget then sets the hide timer
        '''
        self.controls.show()
        self.timer.start(self.time_out)
    
    def make_inactive(self):
        self.controls.hide()

    def __init__(self, controls, time_out=1500):
        '''
        Constructor
        '''
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_inactive)
        self.timer.setSingleShot(True)
        
        self.time_out = time_out
        self.controls = controls
        self.controls.hide()