'''
Created on 2013-06-03

@author: Neil
'''

import math
from PySide.QtGui import QMainWindow, QGraphicsView, QGraphicsScene
from PySide.QtGui import QGraphicsPixmapItem, QPixmap

from layers.LayerManager import instantiate_layer_manager
from control.AstronomerModel import AstronomerModel
from control.ControllerGroup import create_controller_group
from renderer.SkyRenderer import SkyRenderer
from renderer.RendererController import RendererController
from control.ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator as ZMDC

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
    
    def initialize_model_view_controller(self):
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
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
        
        for runnable in list(self.renderer_controller.queuer.queue):
            runnable.run()
    
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.layer_manager = instantiate_layer_manager()
        self.model = AstronomerModel(ZMDC())
        self.initialize_model_view_controller()
        
        # put the window at the screen position (100, 30)
        # with size 480 by 800
        self.setGeometry(100, 30, 480, 800)
        self.show()
        
        