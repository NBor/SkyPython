'''
// Copyright 2010 Google Inc.
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
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-06-03

@author: Neil Borle and Morgan Redshaw
'''

import sys
import math
import time
from PySide import QtCore
from PySide.QtGui import QApplication
from PySide.QtGui import QMainWindow, QGraphicsView, QGraphicsScene

from SharedPreferences import SharedPreferences
from src.views.PreferencesButton import PreferencesButton
from src.views.ZoomButton import ZoomButton
from src.views.WidgetFader import WidgetFader
from src.touch.MapMover import MapMover
from src.touch.DragRotateZoomGestureDetector import DragRotateZoomGestureDetector as DRZDetector
from src.layers.LayerManager import instantiate_layer_manager
from src.control.AstronomerModel import AstronomerModel
from src.control.ControllerGroup import create_controller_group
from src.renderer.SkyRenderer import SkyRenderer
from src.renderer.RendererController import RendererController
from src.control.ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator as ZMDC
from src.control.MagneticDeclinationCalculatorSwitcher import MagneticDeclinationCalculatorSwitcher as MDCS

def start_application(mode=None):
    
    if mode == None:
        worker()
    else:
        import multiprocessing
        
        for i in range(0, 6):
            p = multiprocessing.Process(target=worker, args=(i,))
            p.start()
            
            time.sleep(2)
            
def worker(index=None):
    app = QApplication(sys.argv)
    w = SkyPython(index)
    w.show()
    app.installEventFilter(w)
    r = app.exec_()
    sys.exit(r)


class SkyPython(QMainWindow):
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
    
    layer_manager = None
    model = None
    controller = None
    sky_renderer = None
    renderer_controller = None
    
    def pref_change(self, prefs, manager, layers, event):
        
        for layer in layers:
            prefs.PREFERENCES[layer] = not prefs.PREFERENCES[layer]
            manager.on_shared_preference_change(prefs, layer)
        
        return True
    
    def eventFilter(self, source, event):
        pref_pressed = self.pref_buttons.checkForButtonPress(source, event)
        zoom_pressed = self.zoom_button.checkForButtonPress(source, event, self.controller)
        
        if pref_pressed or zoom_pressed:
            self.show_menus_func()
            
            if pref_pressed:
                self.pref_change(self.shared_prefs, self.layer_manager, 
                                 pref_pressed, event)
        else:
            update = self.DRZ_detector.on_motion_event(event)
        
        if pref_pressed or zoom_pressed or update:
            self.update_rendering()
            return True
        
        return QMainWindow.eventFilter(self, source, event)
    
    def initialize_model_view_controller(self):
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        
        if self.DEBUG_MODE != None:
            self.sky_renderer = SkyRenderer(self.DEBUG_MODE)
        else:
            self.sky_renderer = SkyRenderer()
        
        self.sky_renderer.setAutoFillBackground(False)
        
        # set up the view with the glwidget inside
        self.view.setViewport(self.sky_renderer)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)
        
        self.renderer_controller = RendererController(self.sky_renderer, None)
        self.renderer_controller.add_update_closure(\
            self.RendererModelUpdateClosure(self.model, self.renderer_controller))
        
        self.layer_manager.register_with_renderer(self.renderer_controller)
        
        self.controller = create_controller_group()
        self.controller.set_model(self.model)
        
        # NOTE: THIS BOOLEAN WILL NEED TO BE REMOVED EVENTUALLY
        self.magnetic_switcher = MDCS(self.model, self.USE_AUTO_MODE)
        
        self.run_queue()
        
    def wire_up_screen_controls(self):
        '''
        Will also need to add the files mainWidget, buttons and probably the image information file
        '''
        screen_width = self.sky_renderer.render_state.screen_width
        screen_height = self.sky_renderer.render_state.screen_height
        
        self.pref_buttons = PreferencesButton(self.view)
        self.zoom_button = ZoomButton(self.view)
        
        position_y = ((screen_height - 336) / 2) + 1
        self.pref_buttons.setGeometry(QtCore.QRect(1, position_y, 55, 336))
        
        position_x = ((screen_width - 221) / 2) + 1
        position_y = ((screen_height - 31) * 9/10) + 1
        self.zoom_button.setGeometry(QtCore.QRect(position_x, position_y, 221, 31))
        
        self.pref_buttons_fader = WidgetFader(self.pref_buttons, 2500)
        self.zoom_button_fader = WidgetFader(self.zoom_button, 2500)
        
        self.map_mover = MapMover(self.model, self.controller, self.shared_prefs, 
                                  screen_height)
        self.DRZ_detector = DRZDetector(self.map_mover, self.show_menus_func)
        
    def show_menus_func(self):
        self.pref_buttons_fader.make_active()
        self.zoom_button_fader.make_active()
    
    def update_rendering(self):
        self.sky_renderer.updateGL()
        self.run_queue()
        self.sky_renderer.updateGL()
    
    def run_queue(self):
        num = len(list(self.renderer_controller.queuer.queue))
        while num > 0:
            runnable = self.renderer_controller.queuer.get()
            runnable.run()
            self.renderer_controller.queuer.task_done()
            num -= 1
    
    def __init__(self, debug_index=None):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_AcceptTouchEvents)
        
        self.DEBUG_MODE = debug_index
        self.USE_AUTO_MODE = False
        self.shared_prefs = SharedPreferences()
        
        self.magnetic_switcher = None
        self.model = AstronomerModel(ZMDC())
        self.layer_manager = instantiate_layer_manager(self.model, self.shared_prefs)
        self.initialize_model_view_controller()
        self.wire_up_screen_controls()
        self.controller.set_auto_mode(self.USE_AUTO_MODE)
        
        # put the window at the screen position (100, 30)
        # with size 480 by 800
        self.setGeometry(100, 30, 480, 800)
        self.show()
        
        self.update_rendering()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_rendering)
        self.timer.setInterval(5000)
        self.timer.start()
        
        
if __name__ == "__main__":
    import os
    os.chdir("../..")
    start_application()
