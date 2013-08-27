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
Created on 2013-08-19

@author: Neil Borle
'''

import math
from PySide import QtCore
from src.utils.Enumeration import enum

class DragRotateZoomGestureDetector(object):
    '''
    Handles events such as key presses and mouse button
    presses, which allows for dragging and zooming
    '''
    STATES = enum(READY=0, DRAGGING=1, DRAGGING2=2)
    
    def on_motion_event(self, event):
        '''
        The state changes are as follows.
        READY -> DRAGGING -> DRAGGING2 -> READY
        
        ACTION_DOWN: READY->DRAGGING
           last position = current position
        
        ACTION_MOVE: no state change
           calculate move = current position - last position
           last position = current position
        
        ACTION_UP: DRAGGING->READY
           last position = null
           ...or...from DRAGGING
        
        ACTION_POINTER_DOWN: DRAGGING->DRAGGING2
           we're in multitouch mode
           last position1 = current position1
           last poisiton2 = current position2
        
         ACTION_MOVE:
           calculate move
           last position1 = current position1
           
        NOTE: MULTITOUCH (DRAGGING2) IS NOT IMPLEMENTED YET
        '''
        ACTION_DOWN = QtCore.QEvent.MouseButtonPress
        ACTION_UP = QtCore.QEvent.MouseButtonRelease
        ACTION_MOVE = QtCore.QEvent.MouseMove
        
        if event.type() == QtCore.QEvent.KeyPress:
            self.key_press_event(event)
            return True
        
        if event.type() == ACTION_DOWN and self.state == self.STATES.READY:
            self.show_menu_bool = True
            self.state = self.STATES.DRAGGING
            self.last_x1, self.last_y1 = event.x(), event.y()
            return True
        
        if event.type() == ACTION_MOVE and self.state == self.STATES.DRAGGING:
            self.show_menu_bool = False
            current_x, current_y = event.x(), event.y()
            self.map_mover.on_drag(current_x - self.last_x1, current_y - self.last_y1)
            self.last_x1, self.last_y1 = current_x, current_y
            return True
        
        if event.type() == ACTION_UP and self.state != self.STATES.READY:
            
            if self.show_menu_bool:
                self.show_menus()
                self.show_menu_bool = False
                
            self.state = self.STATES.READY
            return True
                
        return False
        
    def key_press_event(self, event):
        if event.key() == 16777235: # up key, zoom in
            self.map_mover.control_group.zoom_in()
        elif event.key() == 16777237: # down key, zoom out
            self.map_mover.control_group.zoom_out()
        elif event.key() == 65: # "a" key, rotate left
            self.map_mover.control_group.change_right_left(-math.pi/64.0)
        elif event.key() == 68: # "d" key, rotate right
            self.map_mover.control_group.change_right_left(math.pi/64.0)
        elif event.key() == 87: # "w" key, rotate up
            self.map_mover.control_group.change_up_down(-math.pi/64.0)
        elif event.key() == 83: # "s" key, rotate down
            self.map_mover.control_group.change_up_down(math.pi/64.0)
    
    def norm_squared(self, x, y):
        return (x*x + y*y)

    def show_menus(self):
        # This function should be assigned upon instantiation
        raise Exception

    def __init__(self, map_mover, show_menus_func):
        '''
        Constructor
        '''
        self.map_mover = map_mover
        self.state = self.STATES.READY
        self.last_x1, self.last_y1 = 0, 0
        self.last_x2, self.last_y2 = 0, 0
        
        self.show_menu_bool = False
        self.show_menus = show_menus_func
        