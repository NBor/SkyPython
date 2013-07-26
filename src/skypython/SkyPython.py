'''
Created on 2013-06-03

@author: Neil
'''

import sys
import math
from PySide.QtGui import QApplication
from PySide import QtCore
from PySide.QtGui import QMainWindow, QGraphicsView, QGraphicsScene
from PySide.QtGui import QGraphicsPixmapItem, QPixmap, QTouchEvent

from ..layers.LayerManager import instantiate_layer_manager
from ..control.AstronomerModel import AstronomerModel
from ..control.ControllerGroup import create_controller_group
from ..renderer.SkyRenderer import SkyRenderer
from ..renderer.RendererController import RendererController
from ..control.ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator as ZMDC
from ..control.MagneticDeclinationCalculatorSwitcher import MagneticDeclinationCalculatorSwitcher as MDCS

def start_application(mode=None):
    
    if mode == None:
        worker()
    else:
        import multiprocessing, time
        
        for i in range(0, 6):
            p = multiprocessing.Process(target=worker, args=(i,))
            p.start()
            
            time.sleep(2)
            
def worker(index=None):
    app = QApplication(sys.argv)
    w = SkyPython(index)
    w.show()
    app.installEventFilter(w)
    app.exec_()

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
    
    pos_x, pos_y = 0, 0
    def eventFilter(self, source, event):
        
        update = False
        
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.pos_x, self.pos_y = event.x(), event.y()
            return True
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if (event.x() - self.pos_x) > 30: 
                # rotate left on drag left to right
                self.controller.change_right_left(-math.pi/8.0)
            elif (event.x() - self.pos_x) < -30: 
                # rotate right on drag right to left
                self.controller.change_right_left(math.pi/8.0)
                
            if (event.y() - self.pos_y) > 30: 
                # rotate up on drag up to down
                self.controller.change_up_down(-math.pi/8.0)
            elif (event.y() - self.pos_y) < -30: 
                # rotate down on drag down to up
                self.controller.change_up_down(math.pi/8.0)
                
            update = True
                
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == 16777235: # up key, zoom in
                self.controller.zoom_in()
            elif event.key() == 16777237: # down key, zoom out
                self.controller.zoom_out()
            elif event.key() == 65: # "a" key, rotate left
                self.controller.change_right_left(-math.pi/64.0)
            elif event.key() == 68: # "d" key, rotate right
                self.controller.change_right_left(math.pi/64.0)
            elif event.key() == 87: # "w" key, rotate up
                self.controller.change_up_down(-math.pi/64.0)
            elif event.key() == 83: # "s" key, rotate down
                self.controller.change_up_down(math.pi/64.0)
            
            update = True
            
        if update:
            self.sky_renderer.updateGL()
                
            num = len(list(self.renderer_controller.queuer.queue))
            while num > 0:
                runnable = self.renderer_controller.queuer.get()
                runnable.run()
                self.renderer_controller.queuer.task_done()
                num -= 1
            
            self.sky_renderer.updateGL()
            return True
        
        return QMainWindow.eventFilter(self, source, event)
    
    def initialize_model_view_controller(self):
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        if self.DEBUG_MODE != None:
            self.sky_renderer = SkyRenderer(self.DEBUG_MODE)
        else:
            self.sky_renderer = SkyRenderer()
        
        #self.view.setViewport(self.sky_renderer)
        #self.view.setScene(self.scene)
        self.setCentralWidget(self.sky_renderer)
        
#         pixmap = QPixmap("assets/drawable/stardroid_big_image.png")
#         pixItem = QGraphicsPixmapItem(pixmap)
#         self.scene.addItem(pixItem)
#         self.view.fitInView(pixItem)
        
        self.renderer_controller = RendererController(self.sky_renderer, None)
        self.renderer_controller.add_update_closure(\
            self.RendererModelUpdateClosure(self.model, self.renderer_controller))
        
        self.layer_manager.register_with_renderer(self.renderer_controller)
        
        self.controller = create_controller_group()
        self.controller.set_model(self.model)
        
        # NOTE: THIS BOOLEAN WILL NEED TO BE REMOVED EVENTUALLY
        self.magnetic_switcher = MDCS(self.model, self.USE_AUTO_MODE)
        
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
        
        self.magnetic_switcher = None
        self.model = AstronomerModel(ZMDC())
        self.layer_manager = instantiate_layer_manager(self.model)
        self.initialize_model_view_controller()
        self.controller.set_auto_mode(self.USE_AUTO_MODE)
        
        # put the window at the screen position (100, 30)
        # with size 480 by 800
        self.setGeometry(100, 30, 480, 800)
        self.show()
        
        if self.DEBUG_MODE != None:
            self.sky_renderer.updateGL()
                
            num = len(list(self.renderer_controller.queuer.queue))
            while num > 0:
                runnable = self.renderer_controller.queuer.get()
                runnable.run()
                self.renderer_controller.queuer.task_done()
                num -= 1
            
            self.sky_renderer.updateGL()
        
if __name__ == "__main__":
    import os
    os.chdir("../..")
    start_application()